import json
import random
from typing import List, Dict, Any, Set
import numpy as np
from src.utils.paths import get_path
from src.indexing.faiss_service import FaissSearchService


class CandidateGenerator:
    """Generates a candidate pool of videos for a user using multiple channels."""

    def __init__(self):
        # Load enriched video metadata
        videos_json_path = get_path("datasets/processed/enriched_videos.json")
        with open(videos_json_path, "r", encoding="utf-8") as f:
            self.videos = json.load(f)

        # Index videos by ID for fast lookup
        self.video_lookup = {v["video_id"]: v for v in self.videos}

        # Index videos by category for category candidate retrieval
        self.videos_by_category: Dict[str, List[Dict[str, Any]]] = {}
        self.videos_by_creator: Dict[str, List[Dict[str, Any]]] = {}
        self.videos_by_deity: Dict[str, List[Dict[str, Any]]] = {}
        self.videos_by_ritual_family: Dict[str, List[Dict[str, Any]]] = {}
        self.videos_by_ritual: Dict[str, List[Dict[str, Any]]] = {}

        for video in self.videos:
            cat = video.get("category") or video.get("primary_category", "Entertainment")
            self.videos_by_category.setdefault(cat, []).append(video)

            creator = video.get("creator", "")
            if creator:
                self.videos_by_creator.setdefault(creator, []).append(video)

            deity = video.get("primary_deity")
            if deity:
                self.videos_by_deity.setdefault(deity, []).append(video)

            family = video.get("ritual_family")
            if family:
                self.videos_by_ritual_family.setdefault(family, []).append(video)

            ritual = video.get("primary_ritual")
            if ritual:
                self.videos_by_ritual.setdefault(ritual, []).append(video)

        self.categories = list(self.videos_by_category.keys())

        # Initialize vector similarity search and retrieval logger
        self.faiss_search = FaissSearchService()
        try:
            from semantic_indexing.logging.retrieval_logger import CandidateRetrievalLogger
            self.retrieval_logger = CandidateRetrievalLogger()
        except ImportError:
            self.retrieval_logger = None

    def retrieve_trending(self, limit: int = 30) -> List[Dict[str, Any]]:
        """Retrieves top overall trending/high-engagement videos."""
        # Sort by engagement score descending, then by views descending
        sorted_videos = sorted(
            self.videos, 
            key=lambda x: (x.get("engagement_score", 0), x.get("views", 0)), 
            reverse=True
        )
        return sorted_videos[:limit]

    def retrieve_by_categories(self, interest_profile: Dict[str, Any], limit_per_category: int = 15) -> List[Dict[str, Any]]:
        """Retrieves top videos from the user's preferred categories, rituals, and deities based on interest scores."""
        interests = interest_profile.get("interests", {})
        deity_interests = interest_profile.get("deity_interests", {})
        
        # Filter and sort categories with positive interest score (> 0)
        sorted_categories = [
            cat for cat, score in sorted(interests.items(), key=lambda x: x[1], reverse=True)
            if score > 0
        ]
        sorted_deities = [
            deity for deity, score in sorted(deity_interests.items(), key=lambda x: x[1], reverse=True)
            if score > 0
        ]

        candidates = []
        for cat in sorted_categories:
            # Aggregate across category, ritual family, and primary ritual indexes
            cat_videos = list({
                v["video_id"]: v for v in (
                    self.videos_by_category.get(cat, []) +
                    self.videos_by_ritual_family.get(cat, []) +
                    self.videos_by_ritual.get(cat, [])
                )
            }.values())
            
            if not cat_videos:
                continue

            sorted_cat_videos = sorted(
                cat_videos, 
                key=lambda x: (x.get("engagement_score", 0), x.get("views", 0)), 
                reverse=True
            )
            candidates.extend(sorted_cat_videos[:limit_per_category])
            
        for deity in sorted_deities[:3]:
            deity_vids = self.videos_by_deity.get(deity, [])
            if deity_vids:
                candidates.extend(deity_vids[:limit_per_category])

        return candidates

    def retrieve_similar_to_watch_history(self, watch_history: List[Dict[str, Any]], limit_per_video: int = 10, max_seed_videos: int = 3) -> List[Dict[str, Any]]:
        """Retrieves similar videos using FAISS search based on recent high-engagement seed videos."""
        # Filter for videos with high engagement (liked, saved, shared, or completed >= 75%)
        positive_interactions = [
            event for event in watch_history
            if event.get("is_liked") or event.get("is_saved") or event.get("watch_completion_rate", 0.0) >= 0.75
        ]

        if not positive_interactions:
            return []

        # Take the most recent positive seed videos (up to max_seed_videos)
        # Note: assuming watch_history list is chronological
        seed_events = positive_interactions[-max_seed_videos:]

        candidates = []
        for event in seed_events:
            video_id = str(event["video_id"])
            similar_results = self.faiss_search.search_by_id(video_id, top_k=limit_per_video)
            
            for res in similar_results:
                sim_vid = res["video_id"]
                if sim_vid in self.video_lookup:
                    video_meta = self.video_lookup[sim_vid]
                    # Attach vector similarity score for scoring/explanations
                    candidate_meta = video_meta.copy()
                    candidate_meta["_similarity_score"] = res["score"]
                    candidate_meta["_similarity_seed"] = video_id
                    candidates.append(candidate_meta)

        return candidates

    def retrieve_collaborative_filtering(self, interest_profile: Dict[str, Any], all_profiles: Dict[str, Any], all_histories: Dict[str, List[Dict[str, Any]]], current_watch_history: List[Dict[str, Any]], limit: int = 20) -> List[Dict[str, Any]]:
        """Retrieves videos liked/watched by users with similar category interests."""
        current_uid = interest_profile.get("user_id")
        current_interests = interest_profile.get("interests", {})
        if not current_interests or not all_profiles or not all_histories:
            return []
            
        categories = sorted(self.categories)
        
        # Build vector for current user
        vec_cur = np.array([current_interests.get(cat, 0.0) for cat in categories])
        norm_cur = np.linalg.norm(vec_cur)
        if norm_cur == 0:
            return []
            
        similarities = []
        for uid, prof in all_profiles.items():
            if uid == current_uid:
                continue
            other_interests = prof.get("interests", {})
            vec_other = np.array([other_interests.get(cat, 0.0) for cat in categories])
            norm_other = np.linalg.norm(vec_other)
            if norm_other == 0:
                continue
            sim = np.dot(vec_cur, vec_other) / (norm_cur * norm_other)
            similarities.append((uid, sim))
            
        # Sort and take top 3 similar users
        similarities.sort(key=lambda x: x[1], reverse=True)
        top_similar_users = similarities[:3]
        
        cf_candidates = []
        watched_vids = {str(event["video_id"]) for event in current_watch_history}
        
        for sim_uid, sim_score in top_similar_users:
            sim_user_history = all_histories.get(sim_uid, [])
            pos_history = [
                event for event in sim_user_history
                if event.get("is_liked") or event.get("is_saved") or event.get("watch_completion_rate", 0.0) >= 0.75
            ]
            for event in pos_history:
                vid = str(event["video_id"])
                if vid not in watched_vids and vid in self.video_lookup:
                    video_meta = self.video_lookup[vid]
                    candidate_meta = video_meta.copy()
                    candidate_meta["_cf_score"] = float(sim_score)
                    candidate_meta["_cf_source_user"] = sim_uid
                    cf_candidates.append(candidate_meta)
                    
        return cf_candidates[:limit]

    def retrieve_by_creator_affinity(self, creator_affinities: Dict[str, float], limit_per_creator: int = 10, max_creators: int = 3) -> List[Dict[str, Any]]:
        """Retrieves videos from creators that the user has a high affinity with."""
        if not creator_affinities:
            return []
            
        # Sort creators by affinity score descending and select top creators
        top_creators = [
            creator for creator, score in sorted(creator_affinities.items(), key=lambda x: x[1], reverse=True)
            if score > 0
        ][:max_creators]
        
        candidates = []
        for creator in top_creators:
            creator_videos = self.videos_by_creator.get(creator, [])
            if not creator_videos:
                continue
            sorted_creator_videos = sorted(
                creator_videos,
                key=lambda x: (x.get("engagement_score", 0), x.get("views", 0)),
                reverse=True
            )
            for vid in sorted_creator_videos[:limit_per_creator]:
                cand = vid.copy()
                cand["_creator_affinity_score"] = creator_affinities[creator]
                candidates.append(cand)
                
        return candidates

    def retrieve_by_deity(self, preferred_deities: List[str], limit_per_deity: int = 15) -> List[Dict[str, Any]]:
        """Retrieves videos matching the user's preferred deities."""
        candidates = []
        for deity in preferred_deities:
            deity_vids = self.videos_by_deity.get(deity, [])
            for v in deity_vids[:limit_per_deity]:
                c = v.copy()
                c["_retrieval_channel"] = "same_primary_deity"
                candidates.append(c)
        return candidates

    def retrieve_by_ritual_family(self, preferred_families: List[str], limit_per_family: int = 15) -> List[Dict[str, Any]]:
        """Retrieves videos matching the user's preferred ritual families."""
        candidates = []
        for family in preferred_families:
            family_vids = self.videos_by_ritual_family.get(family, [])
            for v in family_vids[:limit_per_family]:
                c = v.copy()
                c["_retrieval_channel"] = "same_ritual_family"
                candidates.append(c)
        return candidates

    def retrieve_exploration(self, limit: int = 30) -> List[Dict[str, Any]]:
        """Retrieves random videos from across the entire catalog to ensure variety."""
        return random.sample(self.videos, min(limit, len(self.videos)))

    def retrieve_fresh(self, limit: int = 150) -> List[Dict[str, Any]]:
        """Retrieves the most recently uploaded videos from the catalog."""
        # Sort videos by created_time descending
        sorted_videos = sorted(self.videos, key=lambda x: x.get("created_time", 0), reverse=True)
        return sorted_videos[:limit]

    def generate_candidates(self, interest_profile: Dict[str, Any], watch_history: List[Dict[str, Any]], creator_affinities: Dict[str, float] = None, all_interest_profiles: Dict[str, Any] = None, all_watch_histories: Dict[str, List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
        """Generates and merges candidates from all channels."""
        t_start = time.time() if 'time' in globals() else 0.0

        # 1. Retrieve candidates from each channel
        trending_pool = self.retrieve_trending(limit=100)
        category_pool = self.retrieve_by_categories(interest_profile, limit_per_category=15)
        similarity_pool = self.retrieve_similar_to_watch_history(watch_history, limit_per_video=10)

        # 2. Retrieve from CMREE Semantic Channels
        preferred_deities = interest_profile.get("preferred_deities", ["Lord Shiva", "Shirdi Sai Baba", "Lord Ganesha"])
        preferred_families = interest_profile.get("preferred_ritual_families", ["Abhishekam", "Aarti", "Archana"])
        
        deity_pool = self.retrieve_by_deity(preferred_deities, limit_per_deity=15)
        family_pool = self.retrieve_by_ritual_family(preferred_families, limit_per_family=15)
        
        # Dynamic collaborative filtering pool
        cf_pool = self.retrieve_collaborative_filtering(
            interest_profile, 
            all_interest_profiles, 
            all_watch_histories, 
            watch_history,
            limit=20
        )
        
        # Creator affinity pool
        creator_affinity_pool = self.retrieve_by_creator_affinity(creator_affinities, limit_per_creator=10)

        # Exploration variety pool
        exploration_pool = self.retrieve_exploration(limit=100)

        # Freshness pool
        fresh_pool = self.retrieve_fresh(limit=150)

        # 2. Merge candidates and tag with their retrieval channels (deduplication)
        merged_candidates: Dict[str, Dict[str, Any]] = {}
        
        # User's recently watched video IDs (to avoid recommending already watched videos in the same session)
        # Relax watched filter if catalog total size is small to prevent zero candidates
        unwatched_count = len([v for v in self.videos if str(v["video_id"]) not in {str(e["video_id"]) for e in watch_history}])
        watched_video_ids = {str(event["video_id"]) for event in watch_history} if unwatched_count >= 5 else set()

        # Helper to insert and track source
        def add_candidate(video: Dict[str, Any], source: str):
            video_id = str(video["video_id"])
            if video_id in watched_video_ids:
                return  # Filter out already watched videos

            if video_id not in merged_candidates:
                merged_candidates[video_id] = {
                    "video_id": video_id,
                    "metadata": video.copy(),
                    "retrieval_sources": [source],
                    "matched_category": video.get("category", "Entertainment"),
                    "similarity_score": video.get("_similarity_score", 0.0),
                    "similarity_seed": video.get("_similarity_seed", None),
                    "cf_score": video.get("_cf_score", 0.0),
                    "cf_source_user": video.get("_cf_source_user", None),
                    "creator_affinity_score": video.get("_creator_affinity_score", 0.0)
                }
            else:
                # Add to retrieval sources list if not already present
                if source not in merged_candidates[video_id]["retrieval_sources"]:
                    merged_candidates[video_id]["retrieval_sources"].append(source)
                
                # Keep the highest similarity score if matched in similarity multiple times
                if "_similarity_score" in video:
                    curr_sim = merged_candidates[video_id]["similarity_score"]
                    new_sim = video["_similarity_score"]
                    if new_sim > curr_sim:
                        merged_candidates[video_id]["similarity_score"] = new_sim
                        merged_candidates[video_id]["similarity_seed"] = video["_similarity_seed"]
                if "_cf_score" in video:
                    merged_candidates[video_id]["cf_score"] = max(merged_candidates[video_id]["cf_score"], video["_cf_score"])
                if "_creator_affinity_score" in video:
                    merged_candidates[video_id]["creator_affinity_score"] = max(merged_candidates[video_id]["creator_affinity_score"], video["_creator_affinity_score"])

        # Run through channels (creator affinity and CF first to preserve score details)
        for video in creator_affinity_pool:
            add_candidate(video, "creator_affinity")
        for video in cf_pool:
            add_candidate(video, "collaborative_filtering")
        for video in similarity_pool:
            add_candidate(video, "similarity")
        for video in deity_pool:
            add_candidate(video, "same_primary_deity")
        for video in family_pool:
            add_candidate(video, "same_ritual_family")
        for video in category_pool:
            add_candidate(video, "category")
        for video in trending_pool:
            add_candidate(video, "trending")
        for video in exploration_pool:
            add_candidate(video, "exploration")
        for video in fresh_pool:
            add_candidate(video, "freshness")

        return list(merged_candidates.values())
