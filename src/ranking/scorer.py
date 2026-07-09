import math
import random
from typing import List, Dict, Any, Tuple


class RankingSignal:
    """Base class for all ranking signals. Subclasses must implement calculate_score."""

    def calculate_score(self, candidate: Dict[str, Any], user_profile: Dict[str, Any], creator_affinities: Dict[str, float] = None) -> float:
        """Returns a normalized score between 0.0 and 1.0 for the candidate video."""
        raise NotImplementedError


class InterestSignal(RankingSignal):
    """Scores how well the video category matches the user's interest profile."""

    def calculate_score(self, candidate: Dict[str, Any], user_profile: Dict[str, Any], creator_affinities: Dict[str, float] = None) -> float:
        category = candidate.get("matched_category", "Entertainment")
        interests = user_profile.get("interests", {})
        
        # Interest score is stored as a percentage (0.0 to 100.0)
        interest_pct = interests.get(category, 0.0)
        
        # Normalize to 0.0 - 1.0 range
        return min(1.0, max(0.0, interest_pct / 100.0))


class CreatorAffinitySignal(RankingSignal):
    """Scores candidate based on user's affinity with the video creator."""

    def calculate_score(self, candidate: Dict[str, Any], user_profile: Dict[str, Any], creator_affinities: Dict[str, float] = None) -> float:
        metadata = candidate.get("metadata", {})
        creator = metadata.get("creator", "")
        if not creator or not creator_affinities:
            return 0.0
            
        affinity_score = creator_affinities.get(creator, 0.0)
        # Normalize to 0.0 - 1.0 range, where an affinity of 100+ is a perfect score
        return min(1.0, affinity_score / 100.0)


class PopularitySignal(RankingSignal):
    """Scores the video based on its engagement rate and historical popularity."""

    def calculate_score(self, candidate: Dict[str, Any], user_profile: Dict[str, Any], creator_affinities: Dict[str, float] = None) -> float:
        metadata = candidate.get("metadata", {})
        
        # Cold-start boost: if the video is fresh (less than 30 days old),
        # give it a high baseline popularity score so it doesn't get out-ranked
        created_time = metadata.get("created_time", 0)
        reference_time = 2205577600
        age_days = (reference_time - created_time) / (3600.0 * 24.0)
        if age_days < 30:
            return 0.8  # High baseline popularity for fresh/cold-start videos
            
        engagement_rate = metadata.get("engagement_rate", 0.0)
        
        # Normalize engagement rate: typically between 0.0 and 0.2
        er_score = min(1.0, engagement_rate / 0.15)
        
        # Include a log-scaled views component
        views = metadata.get("views", 0)
        views_score = min(1.0, math.log1p(views) / 18.0)  # log1p(1e7) ~= 16.1
        
        # Combine er_score (70%) and views_score (30%)
        return round(0.7 * er_score + 0.3 * views_score, 4)


class SimilaritySignal(RankingSignal):
    """Scores the candidate based on FAISS semantic vector similarity."""

    def calculate_score(self, candidate: Dict[str, Any], user_profile: Dict[str, Any], creator_affinities: Dict[str, float] = None) -> float:
        # Cosine similarity score from FAISS search
        return float(candidate.get("similarity_score", 0.0))


class CollaborativeFilteringSignal(RankingSignal):
    """Scores candidate based on user-based collaborative filtering similarity."""

    def calculate_score(self, candidate: Dict[str, Any], user_profile: Dict[str, Any], creator_affinities: Dict[str, float] = None) -> float:
        # Collaborative filtering similarity score
        return float(candidate.get("cf_score", 0.0))


class FreshnessSignal(RankingSignal):
    """Scores candidate based on upload time using exponential decay."""

    def calculate_score(self, candidate: Dict[str, Any], user_profile: Dict[str, Any], creator_affinities: Dict[str, float] = None) -> float:
        metadata = candidate.get("metadata", {})
        created_time = metadata.get("created_time", 0)
        if created_time == 0:
            return 0.5 # Default middle score
            
        # The maximum created_time for 7010 videos is 1600000000 + 7009 * 86400 = 2205577600
        # We can calculate freshness relative to 2205577600.
        reference_time = 2205577600
        age_seconds = max(0, reference_time - created_time)
        age_days = age_seconds / (3600.0 * 24.0)
        
        # Slower decay factor (half-life of 30 days, lambda = 0.0231) to prioritize fresh videos.
        decay_factor = math.exp(-0.0231 * age_days)
        return round(decay_factor, 4)


class RandomExplorationSignal(RankingSignal):
    """Adds a small randomized score to encourage content discovery (exploration)."""

    def calculate_score(self, candidate: Dict[str, Any], user_profile: Dict[str, Any], creator_affinities: Dict[str, float] = None) -> float:
        return random.random()


class RuleBasedScorer:
    """Combines multiple ranking signals using configurable weights to score candidates."""

    def __init__(self, weights: Dict[str, float] = None):
        # Default weights: sum is 1.0
        self.weights = weights or {
            "interest": 0.10,
            "creator_affinity": 0.05,
            "similarity": 0.05,
            "collaborative_filtering": 0.05,
            "popularity": 0.15,
            "freshness": 0.30,
            "exploration": 0.30
        }

        # Registered signals
        self.signals = {
            "interest": InterestSignal(),
            "creator_affinity": CreatorAffinitySignal(),
            "similarity": SimilaritySignal(),
            "collaborative_filtering": CollaborativeFilteringSignal(),
            "popularity": PopularitySignal(),
            "freshness": FreshnessSignal(),
            "exploration": RandomExplorationSignal()
        }

    def add_signal(self, name: str, signal: RankingSignal, weight: float) -> None:
        """Dynamically plugs in a new signal."""
        self.signals[name] = signal
        self.weights[name] = weight

    def update_weight(self, name: str, weight: float) -> None:
        """Updates weight for an existing signal."""
        if name in self.weights:
            self.weights[name] = weight

    def score_candidate(self, candidate: Dict[str, Any], user_profile: Dict[str, Any], creator_affinities: Dict[str, float] = None) -> Tuple[float, Dict[str, float]]:
        """Calculates final score and returns it along with individual signal breakdown."""
        scores_breakdown = {}
        total_score = 0.0
        
        # Sum of active weights for normalization in case they don't add up to 1.0
        total_weight = sum(self.weights.values())
        if total_weight == 0:
            total_weight = 1.0

        for name, signal in self.signals.items():
            weight = self.weights.get(name, 0.0)
            if weight == 0.0:
                scores_breakdown[name] = 0.0
                continue
                
            sig_score = signal.calculate_score(candidate, user_profile, creator_affinities)
            scores_breakdown[name] = sig_score
            total_score += weight * sig_score

        normalized_score = round(total_score / total_weight, 4)
        
        # Category Interest Gate: Completely suppress category if user's interest score is <= 1.5%
        # (Strictly explore items are exempt to allow discovery and building of new interests)
        category = candidate.get("matched_category", "Entertainment")
        interests = user_profile.get("interests", {})
        interest_pct = interests.get(category, 0.0)
        
        retrieval_sources = candidate.get("retrieval_sources", [])
        is_strictly_explore = (retrieval_sources == ["exploration"])
        
        if not is_strictly_explore and interest_pct <= 1.5:
            normalized_score = 0.0

        return normalized_score, scores_breakdown

    def rank(self, candidates: List[Dict[str, Any]], user_profile: Dict[str, Any], creator_affinities: Dict[str, float] = None) -> List[Dict[str, Any]]:
        """Scores and ranks all candidates, attaching scores and breakdown to each candidate."""
        ranked_candidates = []
        
        for cand in candidates:
            score, breakdown = self.score_candidate(cand, user_profile, creator_affinities)
            
            # Enrich candidate metadata with scoring info
            cand_copy = cand.copy()
            cand_copy["final_score"] = score
            cand_copy["score_breakdown"] = breakdown
            ranked_candidates.append(cand_copy)

        # Sort by final score descending
        ranked_candidates.sort(key=lambda x: x["final_score"], reverse=True)
        return ranked_candidates
