import json
import time
import hashlib
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

        # Load and sanitize interest profiles with persona baseline preferences
        with open(self.interest_profiles_path, "r", encoding="utf-8") as f:
            self.interest_profiles = json.load(f)

        from src.users.personas import get_persona_preferred_categories

        LEGACY_KEYS = {"Pooja & Aarti", "Temple Ritual", "Devotion", "Lifestyle & Culture", "Bhajan & Kirtan", "Archana & Mantras", "Entertainment"}
        for uid, prof in self.interest_profiles.items():
            user = self.user_lookup.get(uid, {})
            persona_name = user.get("persona", prof.get("persona", "Devotional Practitioner"))
            preferred_cats = get_persona_preferred_categories(persona_name)

            raw_scores = prof.setdefault("raw_scores", {})
            for key in list(raw_scores.keys()):
                if key.startswith("Any other") or key in LEGACY_KEYS:
                    del raw_scores[key]
            
            # Ensure persona baseline scores exist (15.0 raw points each)
            if not raw_scores:
                for pcat in preferred_cats:
                    raw_scores[pcat] = 15.0
            
            # L1 Proportional Normalization (interests sum to 100.0%)
            total_score = sum(raw_scores.values())
            interests = {}
            if total_score > 0:
                for k, v in raw_scores.items():
                    if v > 0:
                        interests[k] = round((v / total_score) * 100.0, 1)
            prof["interests"] = dict(sorted(interests.items(), key=lambda x: x[1], reverse=True))

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
        # Create a mapping of video_id to user interaction states
        user_interactions = {}
        for ev in watch_history:
            vid = ev["video_id"]
            user_interactions[vid] = {
                "is_liked": ev.get("is_liked", False),
                "is_saved": ev.get("is_saved", False),
                "is_commented": ev.get("is_commented", False)
            }

        # 5. Format response and generate explanations
        feed = []
        for item in diverse_candidates:
            vid = item["video_id"]
            meta = item["metadata"]
            
            # Generate explanations
            explanation = self.explainer.generate_explanation(item, interest_profile)
            semantic_explanation = self.explainer.generate_semantic_explanation(item, interest_profile)

            # Retrieve user's historical interaction state
            interaction = user_interactions.get(vid, {"is_liked": False, "is_saved": False, "is_commented": False})

            raw_final = float(item["final_score"])
            # Calibrate score to 0.65 - 0.99 match range for UI percentage display
            calibrated_match_score = round(min(0.99, max(0.65, 0.58 + raw_final * 0.45)), 4)

            # Build production response payload
            feed.append({
                "video_id": vid,
                "title": meta.get("caption") or f"Clip {vid}",
                "duration": float(meta.get("duration", 0.0)),
                "category": meta.get("category", "Entertainment"),
                "ritual_family": meta.get("ritual_family") or meta.get("category", "Entertainment"),
                "primary_ritual": meta.get("primary_ritual") or meta.get("subcategory", "Devotional Ritual"),
                "primary_deity": meta.get("primary_deity", "Unassigned / General"),
                "offering": meta.get("offering") or meta.get("offerings", ["Devotional Offering"]),
                "thumbnail_url": f"{BASE_URL}/thumbnails/{vid}.jpg",
                "video_url": f"{BASE_URL}/videos/{vid}.mp4",
                "score": calibrated_match_score,
                "raw_score": raw_final,
                "explanation": explanation,
                "semantic_explanation": semantic_explanation,
                "score_breakdown": item["score_breakdown"],
                "retrieval_sources": item["retrieval_sources"],
                "is_liked": interaction["is_liked"],
                "is_saved": interaction["is_saved"],
                "is_commented": interaction["is_commented"]
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
        is_final = bool(engagement.get("is_final", False))
        
        # MSR-VTT Calibrated Event Weights (adapted for DAIV scenario)
        WATCH_COMPLETE_WEIGHT = 6
        SKIP_WEIGHT = -5
        REPLAY_WEIGHT = 5
        LIKE_WEIGHT = 3
        SAVE_WEIGHT = 4
        SHARE_WEIGHT = 5
        COMMENT_WEIGHT = 4
        
        event_score = 0.0
        if is_final:
            if watch_completion_rate >= 0.85:
                event_score += WATCH_COMPLETE_WEIGHT
            elif watch_completion_rate < 0.2 and not (is_liked or is_saved or is_shared or is_commented):
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
            
        # 3. Resolve previous event for delta calculation and update watch history
        history = self.user_watch_histories.setdefault(resolved_uid, [])
        prev_event = None
        for ev in history:
            if ev["video_id"] == video_id:
                prev_event = ev
                break
                
        # Idempotency check: Skip duplicate processing if exact same engagement score & interaction state was already recorded
        if (prev_event and 
            prev_event.get("engagement_score") == event_score and 
            prev_event.get("is_liked") == is_liked and 
            prev_event.get("is_saved") == is_saved and
            prev_event.get("is_commented") == is_commented and
            abs(prev_event.get("watch_completion_rate", 0.0) - watch_completion_rate) < 0.05):
            
            ts = time.strftime('%Y-%m-%d %H:%M:%S')
            prof = self.interest_profiles.get(resolved_uid, {})
            aff = self.user_creator_affinities.get(resolved_uid, {})
            print(f"[DEBUG_LOG] [{ts}] Duplicate Feedback Event Ignored (Idempotent) | User ID: {resolved_uid} | Video ID: {video_id}")
            return {
                "status": "success",
                "user_id": resolved_uid,
                "interests": prof.get("interests", {}),
                "creator_affinities": aff,
                "added_event": prev_event
            }

        # Profile state before update (for logging audit)
        profile = self.interest_profiles.setdefault(resolved_uid, {
            "user_id": resolved_uid,
            "persona": user["persona"],
            "raw_scores": {},
            "interests": {}
        })
        vector_before = dict(profile.get("interests", {}))
                
        if prev_event:
            score_delta = event_score - prev_event["engagement_score"]
            prev_event.update({
                "watch_completion_rate": watch_completion_rate,
                "watch_time_seconds": float(engagement.get("watch_time_seconds", 0.0)),
                "replay_count": replay_count,
                "is_liked": is_liked,
                "is_saved": is_saved,
                "is_shared": is_shared,
                "is_commented": is_commented,
                "engagement_score": event_score
            })
        else:
            score_delta = event_score
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
            history.append(new_event)
        
        # 4. Update Interest Profile raw score
        raw_scores = profile.setdefault("raw_scores", {})
        
        family = video_meta.get("ritual_family")
        ritual = video_meta.get("primary_ritual")

        CANONICAL_CATEGORIES = {
            "Abhishekam", "Milk / Panchamrutha / Water Abhishekam", "Aarti", "Flame Worship & Lamp Ritual",
            "Festival Processions", "Sacred Chariot & Street Procession", "Pooja", "Devotional Ritual & Worship",
            "Bhajan", "Devotional Hymns & Songs", "Meditation / Chanting", "Silent Reflection & Mantra Japa",
            "Homa / Yajna", "Sacred Fire Altar Ritual", "Annadanam", "Sacred Food Service & Prasad",
            "Kirtan / Nama Sankeerthana", "Pravachan / Spiritual Discourses", "Temple Darshan"
        }

        interacted_keys = set(filter(None, [category, family, ritual]))
        
        # Apply 0.95 decay factor to non-interacted categories on a new video event
        if not prev_event:
            for cat in raw_scores:
                if cat not in interacted_keys:
                    raw_scores[cat] = max(5.0, raw_scores[cat] * 0.95)

        for key in interacted_keys:
            if key in CANONICAL_CATEGORIES or not key.startswith("Any other"):
                raw_scores[key] = max(0.0, raw_scores.get(key, 0.0) + score_delta)
        
        # Purge legacy non-canonical keys
        for legacy_key in list(raw_scores.keys()):
            if legacy_key.startswith("Any other") or legacy_key in ["Pooja & Aarti", "Temple Ritual", "Devotion", "Lifestyle & Culture", "Bhajan & Kirtan", "Archana & Mantras", "Entertainment"]:
                del raw_scores[legacy_key]

        # Ensure baseline persona categories maintain minimum baseline (10.0 pts each)
        from src.users.personas import get_persona_preferred_categories
        preferred_cats = get_persona_preferred_categories(user.get("persona", ""))
        for pcat in preferred_cats:
            raw_scores[pcat] = max(10.0, raw_scores.get(pcat, 10.0))

        # L1 Softmax Normalization: Percentages sum to 100.0%
        total_score = sum(raw_scores.values())
        interests = profile.setdefault("interests", {})
        interests.clear()
        
        if total_score > 0:
            for key, score in raw_scores.items():
                if score > 0:
                    interests[key] = round((score / total_score) * 100.0, 1)

        # Sort interests descending for UI display
        profile["interests"] = dict(sorted(interests.items(), key=lambda x: x[1], reverse=True))
            
        # 5. Update Creator Affinity
        affinities = self.user_creator_affinities.setdefault(resolved_uid, {})
        if creator:
            affinities[creator] = max(0.0, affinities.get(creator, 0.0) + score_delta)
            
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
            
        # Debug audit log as requested
        vector_after = dict(profile.get("interests", {}))
        prof_bytes = json.dumps(vector_after, sort_keys=True).encode("utf-8")
        prof_hash = hashlib.md5(prof_bytes).hexdigest()[:8]
        ts_now = time.strftime('%Y-%m-%d %H:%M:%S')

        print(f"[DEBUG_LOG] [{ts_now}] Profile State Update Audit:")
        print(f"   ├── Current User ID: {resolved_uid}")
        print(f"   ├── Interest Vector Before Update: {vector_before}")
        print(f"   ├── Feedback Event: video_id={video_id}, liked={is_liked}, saved={is_saved}, final={is_final}")
        print(f"   ├── Applied Delta: {score_delta} (Event Score: {event_score})")
        print(f"   ├── Interest Vector After Update: {vector_after}")
        print(f"   ├── Profile Saved: {self.interest_profiles_path}")
        print(f"   └── Profile Hash: {prof_hash}")
            
        return {
            "status": "success",
            "user_id": resolved_uid,
            "interests": profile["interests"],
            "creator_affinities": affinities,
            "added_event": prev_event if prev_event else new_event
        }
