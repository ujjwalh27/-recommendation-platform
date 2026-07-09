import json
from typing import List, Dict, Any
from src.utils.paths import get_path
from src.candidate_generation.candidate_generator import CandidateGenerator
from src.ranking.scorer import RuleBasedScorer
from src.recommender.diversity import DiversityFilter
from src.recommender.explainer import RecommendationExplainer

BASE_URL = "http://127.0.0.1:8000"


class RecommenderService:
    """Orchestrates the entire recommendation pipeline for serving personalized feeds."""

    def __init__(self):
        # Paths
        self.users_path = get_path("datasets/processed/users.json")
        self.watch_history_path = get_path("datasets/processed/watch_history.json")
        self.interest_profiles_path = get_path("datasets/processed/interest_profiles.json")

        # Load users and mapping
        with open(self.users_path, "r", encoding="utf-8") as f:
            self.users = json.load(f)
        self.user_lookup = {u["user_id"]: u for u in self.users}

        # Load watch histories
        with open(self.watch_history_path, "r", encoding="utf-8") as f:
            self.watch_history = json.load(f)
        
        # Group watch history by user for fast lookup
        self.user_watch_histories: Dict[str, List[Dict[str, Any]]] = {}
        for event in self.watch_history:
            uid = event["user_id"]
            self.user_watch_histories.setdefault(uid, []).append(event)

        # Load interest profiles
        with open(self.interest_profiles_path, "r", encoding="utf-8") as f:
            self.interest_profiles = json.load(f)

        # Pipeline components - initialize CandidateGenerator first
        self.candidate_generator = CandidateGenerator()
        
        # Helper lookups to map video metadata
        self.video_to_creator = {str(v["video_id"]): v.get("creator", "") for v in self.candidate_generator.videos}
        self.video_to_category = {str(v["video_id"]): v.get("category", "") for v in self.candidate_generator.videos}

        # Calculate initial creator affinities from historical watch history
        self.user_creator_affinities: Dict[str, Dict[str, float]] = {}
        for uid, events in self.user_watch_histories.items():
            affinities = {}
            for event in events:
                vid = str(event["video_id"])
                creator = self.video_to_creator.get(vid)
                if creator:
                    score = event.get("engagement_score", 0.0)
                    affinities[creator] = affinities.get(creator, 0.0) + score
            # Clamp to positive values
            self.user_creator_affinities[uid] = {c: max(0.0, s) for c, s in affinities.items()}

        # Other pipeline components
        self.scorer = RuleBasedScorer()
        self.diversity_filter = DiversityFilter(max_consecutive_category=1, max_category_ratio=0.3)
        self.explainer = RecommendationExplainer()

    def find_user_by_id_or_persona(self, query: str) -> Dict[str, Any]:
        """Resolves user_id or persona name to a valid user profile.
        
        If a persona name is supplied, it finds the first user belonging to that persona.
        """
        # Clean query
        query = query.strip()
        
        # 1. Direct user_id match
        if query in self.user_lookup:
            return self.user_lookup[query]

        # 2. Check if query is a persona name
        for user in self.users:
            if user["persona"].lower() == query.lower() or user["persona"].replace(" ", "").lower() == query.replace(" ", "").lower():
                return user

        # 3. Fallback to first user in list
        return self.users[0]

    def get_recommendations(self, user_query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Executes the full candidate retrieval, ranking, diversity filtering, and explanation generation pipeline."""
        # 1. Resolve user profile
        user = self.find_user_by_id_or_persona(user_query)
        user_id = user["user_id"]
        
        # Fetch user's interest profile and watch history
        interest_profile = self.interest_profiles.get(user_id, {
            "user_id": user_id,
            "persona": user["persona"],
            "interests": {}
        })
        watch_history = self.user_watch_histories.get(user_id, [])
        creator_affinities = self.user_creator_affinities.get(user_id, {})

        # 2. Candidate Generation
        candidates = self.candidate_generator.generate_candidates(interest_profile, watch_history, creator_affinities)

        # 3. Rule-Based Scoring & Ranking
        ranked_candidates = self.scorer.rank(candidates, interest_profile, creator_affinities)

        # 4. Diversity Filtering (Re-ranking)
        diverse_candidates = self.diversity_filter.filter(ranked_candidates, limit=limit)

        # 5. Format response and generate explanations
        feed = []
        for item in diverse_candidates:
            vid = item["video_id"]
            meta = item["metadata"]
            
            # Generate explanation
            explanation = self.explainer.generate_explanation(item, interest_profile)

            # Build production response payload
            feed.append({
                "video_id": vid,
                "title": meta.get("caption") or f"Clip {vid}",
                "duration": float(meta.get("duration", 0.0)),
                "category": meta.get("category", "Entertainment"),
                "thumbnail_url": f"{BASE_URL}/thumbnails/{vid}.jpg",
                "video_url": f"{BASE_URL}/videos/{vid}.mp4",
                "score": float(item["final_score"]),
                "explanation": explanation,
                "score_breakdown": item["score_breakdown"],
                "retrieval_sources": item["retrieval_sources"]
            })

        return feed

    def submit_feedback(self, user_id: str, video_id: str, engagement: Dict[str, Any]) -> Dict[str, Any]:
        """Receives real-time feedback for a video, updates user history, interest profile, and creator affinity."""
        user_id = str(user_id)
        video_id = str(video_id)
        
        # 1. Resolve user profile
        user = self.find_user_by_id_or_persona(user_id)
        resolved_uid = user["user_id"]
        
        # 2. Get video metadata
        video_meta = self.candidate_generator.video_lookup.get(video_id)
        if not video_meta:
            return {"status": "error", "message": f"Video {video_id} not found"}
            
        category = video_meta.get("category", "Entertainment")
        creator = video_meta.get("creator", "")
        
        # Extract engagement signals
        watch_completion_rate = float(engagement.get("watch_completion_rate", 0.0))
        replay_count = int(engagement.get("replay_count", 0))
        is_liked = bool(engagement.get("is_liked", False))
        is_saved = bool(engagement.get("is_saved", False))
        is_shared = bool(engagement.get("is_shared", False))
        is_commented = bool(engagement.get("is_commented", False))
        
        # Engagement event weights – tuned down to reduce their impact on the interest profile
        WATCH_COMPLETE_WEIGHT = 6   # previously +10
        SKIP_WEIGHT = -5            # previously -8
        REPLAY_WEIGHT = 5           # previously +8 per replay
        LIKE_WEIGHT = 3             # previously +7
        SAVE_WEIGHT = 4             # previously +9
        SHARE_WEIGHT = 5            # previously +10
        COMMENT_WEIGHT = 4          # previously +8
        
        # Score engagement events using the new weights
        event_score = 0
        if watch_completion_rate >= 0.85:
            event_score += WATCH_COMPLETE_WEIGHT
        elif watch_completion_rate < 0.2:
            event_score += SKIP_WEIGHT
        
        event_score += replay_count * REPLAY_WEIGHT
        if is_liked:
            event_score += LIKE_WEIGHT
        if is_saved:
            event_score += SAVE_WEIGHT
        if is_shared:
            event_score += SHARE_WEIGHT
        if is_commented:
            event_score += COMMENT_WEIGHT
            
        # 3. Append to watch history
        new_event = {
            "user_id": resolved_uid,
            "video_id": video_id,
            "category": category,
            "watch_completion_rate": watch_completion_rate,
            "watch_time_seconds": float(engagement.get("watch_time_seconds", 0.0)),
            "replay_count": replay_count,
            "is_liked": is_liked,
            "is_saved": is_saved,
            "is_shared": is_shared,
            "is_commented": is_commented,
            "engagement_score": event_score
        }
        self.user_watch_histories.setdefault(resolved_uid, []).append(new_event)
        
        # 4. Update Interest Profile raw score
        profile = self.interest_profiles.setdefault(resolved_uid, {
            "user_id": resolved_uid,
            "persona": user["persona"],
            "raw_scores": {},
            "interests": {}
        })
        
        raw_scores = profile.setdefault("raw_scores", {})
        # If raw_scores is empty, initialize it from current interests or defaults
        if not raw_scores and profile.get("interests"):
            raw_scores.update({cat: float(pct) for cat, pct in profile["interests"].items()})
            
        # Decay all raw scores slightly toward the baseline of 15.0 to prevent draining to zero
        for cat in raw_scores:
            raw_scores[cat] = max(0.0, 15.0 + (raw_scores[cat] - 15.0) * 0.95)
            
        raw_scores[category] = max(0.0, raw_scores.get(category, 0.0) + event_score)
        
        # Normalize interests to sum to 100
        total_score = sum(raw_scores.values())
        if total_score > 0:
            profile["interests"] = {cat: round((score / total_score) * 100, 2) for cat, score in raw_scores.items()}
        else:
            profile["interests"] = {cat: 0.0 for cat in raw_scores}
            
        # 5. Update Creator Affinity
        affinities = self.user_creator_affinities.setdefault(resolved_uid, {})
        if creator:
            affinities[creator] = max(0.0, affinities.get(creator, 0.0) + event_score)
            
        # 6. Persist updated watch history and interest profiles to disk
        try:
            with open(self.interest_profiles_path, "w", encoding="utf-8") as f:
                json.dump(self.interest_profiles, f, indent=4)
            
            # Flatten user watch histories back into a list to save to watch_history.json
            all_history_events = []
            for uid, events in self.user_watch_histories.items():
                all_history_events.extend(events)
            with open(self.watch_history_path, "w", encoding="utf-8") as f:
                json.dump(all_history_events, f, indent=4)
        except Exception as e:
            print(f"Error persisting updated profile state to disk: {e}")
            
        return {
            "status": "success",
            "user_id": resolved_uid,
            "interests": profile["interests"],
            "creator_affinities": affinities,
            "added_event": new_event
        }
