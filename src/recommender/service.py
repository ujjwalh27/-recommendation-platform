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

        # Initialize UserInterestProfileStore as the SINGLE SOURCE OF TRUTH
        from src.recommender.profile_store import UserInterestProfileStore
        self.profile_store = UserInterestProfileStore()

        from src.users.personas import get_persona_preferred_categories

        # Canonical Mapping Dictionary to merge subcategories into main categories
        self.CATEGORY_CANONICAL_MAP = {
            "Aarti": "Aarti",
            "Devotional Aarti": "Aarti",
            "Flame Worship & Lamp Ritual": "Aarti",
            "Flame Worship": "Aarti",
            
            "Abhishekam": "Abhishekam",
            "Milk / Panchamrutha / Water Abhishekam": "Abhishekam",
            "Panchamrutha Abhishekam": "Abhishekam",
            "Water Abhishekam": "Abhishekam",
            
            "Pooja": "Pooja",
            "Devotional Ritual & Worship": "Pooja",
            "Shrine Worship": "Pooja",
            "Temple Worship": "Pooja",
            
            "Bhajan": "Bhajan",
            "Devotional Hymns & Songs": "Bhajan",
            "Kirtan / Nama Sankeerthana": "Bhajan",
            "Kirtan": "Bhajan",
            "Devotional Singing": "Bhajan",
            
            "Festival Processions": "Festival Processions",
            "Sacred Chariot & Street Procession": "Festival Processions",
            "Procession": "Festival Processions",
            "Chariot Procession": "Festival Processions",
            
            "Meditation / Chanting": "Meditation / Chanting",
            "Silent Reflection & Mantra Japa": "Meditation / Chanting",
            "Chanting": "Meditation / Chanting",
            "Meditation": "Meditation / Chanting",
            
            "Homa / Yajna": "Homa / Yajna",
            "Sacred Fire Altar Ritual": "Homa / Yajna",
            "Havan": "Homa / Yajna",
            
            "Annadanam": "Annadanam",
            "Sacred Food Service & Prasad": "Annadanam",
            
            "Pravachan / Spiritual Discourses": "Pravachan / Spiritual Discourses",
            "Spiritual Discourses": "Pravachan / Spiritual Discourses",
            
            "Temple Darshan": "Temple Darshan",
            "Temple Darshan & Deity Viewing": "Temple Darshan",
            "Temple Darshan & Monumental Statues": "Temple Darshan",
            "Temple Darshan & Sanctum View": "Temple Darshan",
        }

        self.LEGACY_KEYS = {"Pooja & Aarti", "Temple Ritual", "Devotion", "Lifestyle & Culture", "Bhajan & Kirtan", "Archana & Mantras", "Entertainment"}
        for uid, prof in self.interest_profiles.items():
            raw_scores = prof.setdefault("raw_scores", {})
            consolidated = {}
            for key, val in raw_scores.items():
                if not key.startswith("Any other") and key not in self.LEGACY_KEYS:
                    c_key = self.CATEGORY_CANONICAL_MAP.get(key, key)
                    consolidated[c_key] = consolidated.get(c_key, 0.0) + val
            
            prof["raw_scores"] = consolidated

            # L1 Proportional Normalization (interests sum to 100.0%)
            total_score = sum(consolidated.values())
            interests = {}
            if total_score > 0:
                for k, v in consolidated.items():
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

    @property
    def interest_profiles(self) -> Dict[str, Any]:
        return self.profile_store.profiles

    def find_user_by_id_or_persona(self, query: str) -> Dict[str, Any]:
        """Resolves user_id or persona name to a valid user profile."""
        query = query.strip()
        if query in self.user_lookup:
            return self.user_lookup[query]

        for user in self.users:
            if user["persona"].lower() == query.lower() or user["persona"].replace(" ", "").lower() == query.replace(" ", "").lower():
                return user

        return self.users[0]

    def get_recommendations(self, user_query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Executes the full candidate retrieval, ranking, diversity filtering, and explanation generation pipeline.
        READ-ONLY operation: Never mutates user profile.
        """
        # 1. Resolve user profile
        user = self.find_user_by_id_or_persona(user_query)
        user_id = user["user_id"]
        
        # READ-ONLY: Get profile snapshot from single source of truth
        interest_profile = self.profile_store.get_profile(user_id, persona=user["persona"])
        watch_history = self.user_watch_histories.get(user_id, [])
        creator_affinities = interest_profile.get("creator_affinities", {})

        # 2. Candidate Generation (Read Only)
        candidates = self.candidate_generator.generate_candidates(interest_profile, watch_history, creator_affinities)

        # 3. Rule-Based Scoring & Ranking (Read Only)
        ranked_candidates = self.scorer.rank(candidates, interest_profile, creator_affinities)

        # 4. Diversity Filtering (Re-ranking)
        diverse_candidates = self.diversity_filter.filter(ranked_candidates, limit=limit)

        # Build production response payload
        feed = []
        for item in diverse_candidates:
            vid = item["video_id"]
            meta = item["metadata"]
            
            explanation = self.explainer.generate_explanation(item, interest_profile)
            semantic_explanation = self.explainer.generate_semantic_explanation(item, interest_profile)

            raw_final = float(item["final_score"])
            calibrated_match_score = round(min(0.99, max(0.65, 0.58 + raw_final * 0.45)), 4)

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
                "is_liked": False,
                "is_saved": False,
                "is_commented": False
            })

        return feed

    def submit_feedback(self, user_id: str, video_id: str, engagement: Dict[str, Any]) -> Dict[str, Any]:
        """Receives real-time interaction feedback and delegates atomic update to UserInterestProfileStore."""
        user_id = str(user_id)
        video_id = str(video_id)
        
        user = self.find_user_by_id_or_persona(user_id)
        resolved_uid = user["user_id"]
        
        video_meta = self.candidate_generator.video_lookup.get(video_id, {})
        if not video_meta:
            # Fallback metadata dictionary
            video_meta = {"video_id": video_id, "category": "Entertainment"}

        # Construct explicit event_id for idempotency if not provided
        is_liked = bool(engagement.get("is_liked", False))
        is_saved = bool(engagement.get("is_saved", False))
        w_comp = float(engagement.get("watch_completion_rate", 0.0))
        
        event_id = engagement.get("event_id")
        if not event_id:
            event_id = f"evt_{resolved_uid}_{video_id}_{is_liked}_{is_saved}_{round(w_comp, 1)}"

        event_type = "feedback"
        if is_liked:
            event_type = "like"
        elif is_saved:
            event_type = "save"
        elif w_comp >= 0.85:
            event_type = "watch_complete"
        elif w_comp < 0.20 and engagement.get("is_final"):
            event_type = "skip"

        # Delegate event processing to UserInterestProfileStore (Single Source of Truth)
        res = self.profile_store.process_event(
            user_id=resolved_uid,
            event_id=event_id,
            event_type=event_type,
            video_id=video_id,
            engagement_payload=engagement,
            video_meta=video_meta,
            persona=user["persona"]
        )

        updated_profile = res["profile"]
        return {
            "status": "success",
            "user_id": resolved_uid,
            "version": updated_profile["version"],
            "interests": updated_profile["interests"],
            "category_interests": updated_profile.get("category_interests", {}),
            "deity_interests": updated_profile.get("deity_interests", {}),
            "ritual_interests": updated_profile.get("ritual_interests", {}),
            "creator_affinities": updated_profile.get("creator_affinities", {}),
            "last_event_id": updated_profile["last_event_id"]
        }
            
    def reset_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Resets interest vector, raw scores, watch history, and creator affinities to 0 for a specific user."""
        user = self.find_user_by_id_or_persona(user_id)
        resolved_uid = user["user_id"]
        return self.profile_store.reset_profile(resolved_uid)

    def reset_all_user_profiles(self) -> Dict[str, Any]:
        """Resets all user profile vectors and watch histories across the system."""
        for uid in list(self.profile_store.profiles.keys()):
            self.profile_store.reset_profile(uid)
        return {"status": "success", "message": "All user profiles reset"}
