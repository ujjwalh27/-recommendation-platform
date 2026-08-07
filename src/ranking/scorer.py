import math
import random
from typing import List, Dict, Any, Tuple


class RankingSignal:
    """Base class for all ranking signals. Subclasses must implement calculate_score."""

    def calculate_score(self, candidate: Dict[str, Any], user_profile: Dict[str, Any], creator_affinities: Dict[str, float] = None) -> float:
        """Returns a normalized score between 0.0 and 1.0 for the candidate video."""
        raise NotImplementedError


class InterestSignal(RankingSignal):
    """Scores how well the video category, ritual family, and primary ritual match the user's interest profile."""

    def calculate_score(self, candidate: Dict[str, Any], user_profile: Dict[str, Any], creator_affinities: Dict[str, float] = None) -> float:
        metadata = candidate.get("metadata", candidate)
        category = candidate.get("matched_category") or metadata.get("category") or metadata.get("primary_category")
        family = metadata.get("ritual_family")
        ritual = metadata.get("primary_ritual")
        deity = metadata.get("primary_deity")

        interests = user_profile.get("interests", {})
        
        # Interest score stored as percentage (0.0 to 100.0)
        cat_score = interests.get(category, 0.0) if category else 0.0
        family_score = interests.get(family, 0.0) if family else 0.0
        ritual_score = interests.get(ritual, 0.0) if ritual else 0.0

        best_interest = max(cat_score, family_score, ritual_score)

        # Deity & Ritual Family preferences bonus
        pref_deities = user_profile.get("preferred_deities", [])
        pref_families = user_profile.get("preferred_ritual_families", [])

        deity_boost = 15.0 if deity and deity in pref_deities else 0.0
        family_boost = 15.0 if family and family in pref_families else 0.0

        total_score = min(100.0, best_interest + deity_boost + family_boost)
        return round(min(1.0, max(0.0, total_score / 100.0)), 4)


class CreatorAffinitySignal(RankingSignal):
    """Scores candidate based on user's affinity with the video creator."""

    def calculate_score(self, candidate: Dict[str, Any], user_profile: Dict[str, Any], creator_affinities: Dict[str, float] = None) -> float:
        metadata = candidate.get("metadata", {})
        creator = metadata.get("creator", "")
        if not creator or not creator_affinities:
            return 0.0
            
        affinity_score = creator_affinities.get(creator, 0.0)
        # Normalize to 0.0 - 1.0 range, where an affinity of 10+ is a perfect score
        return min(1.0, affinity_score / 10.0)


class PopularitySignal(RankingSignal):
    """Scores the video based on its engagement rate and historical popularity."""

    def calculate_score(self, candidate: Dict[str, Any], user_profile: Dict[str, Any], creator_affinities: Dict[str, float] = None) -> float:
        metadata = candidate.get("metadata", {})
        created_time = metadata.get("created_time", 0)
        reference_time = 2205577600
        age_days = (reference_time - created_time) / (3600.0 * 24.0)
        if age_days < 30:
            return 0.8  # High baseline popularity for fresh/cold-start videos
            
        engagement_rate = metadata.get("engagement_rate", 0.0)
        er_score = min(1.0, engagement_rate / 0.15)
        views = metadata.get("views", 0)
        views_score = min(1.0, math.log1p(views) / 18.0)
        return round(0.7 * er_score + 0.3 * views_score, 4)


class SimilaritySignal(RankingSignal):
    """Scores the candidate based on FAISS semantic vector similarity."""

    def calculate_score(self, candidate: Dict[str, Any], user_profile: Dict[str, Any], creator_affinities: Dict[str, float] = None) -> float:
        return float(candidate.get("similarity_score", 0.0))


class CollaborativeFilteringSignal(RankingSignal):
    """Scores candidate based on user-based collaborative filtering similarity."""

    def calculate_score(self, candidate: Dict[str, Any], user_profile: Dict[str, Any], creator_affinities: Dict[str, float] = None) -> float:
        return float(candidate.get("cf_score", 0.0))


class FreshnessSignal(RankingSignal):
    """Scores candidate based on upload time using exponential decay."""

    def calculate_score(self, candidate: Dict[str, Any], user_profile: Dict[str, Any], creator_affinities: Dict[str, float] = None) -> float:
        metadata = candidate.get("metadata", {})
        created_time = metadata.get("created_time", 0)
        if created_time == 0:
            return 0.5
        reference_time = 2205577600
        age_seconds = max(0, reference_time - created_time)
        age_days = age_seconds / (3600.0 * 24.0)
        decay_factor = math.exp(-0.0231 * age_days)
        return round(decay_factor, 4)


class RandomExplorationSignal(RankingSignal):
    """Adds a small randomized score to encourage content discovery (exploration)."""

    def calculate_score(self, candidate: Dict[str, Any], user_profile: Dict[str, Any], creator_affinities: Dict[str, float] = None) -> float:
        return random.random() * 0.1  # Micro exploration factor


class RuleBasedScorer:
    """Combines multiple ranking signals using configurable weights to score candidates."""

    def __init__(self, weights: Dict[str, float] = None):
        # Stable MSR-VTT Personalization Weights
        self.weights = weights or {
            "interest": 0.35,
            "creator_affinity": 0.20,
            "similarity": 0.15,
            "collaborative_filtering": 0.10,
            "popularity": 0.10,
            "freshness": 0.05,
            "exploration": 0.05
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
        
        # Category Interest Gate: Suppress category ONLY if user explicitly has a near-zero interest score (<= 1.5%)
        metadata = candidate.get("metadata", candidate)
        category = candidate.get("matched_category") or metadata.get("category") or metadata.get("primary_category")
        family = metadata.get("ritual_family")
        ritual = metadata.get("primary_ritual")

        interests = user_profile.get("interests", {})
        cat_interest = interests.get(category, 50.0) if category else 50.0
        fam_interest = interests.get(family, 50.0) if family else 50.0
        rit_interest = interests.get(ritual, 50.0) if ritual else 50.0
        best_interest_pct = max(cat_interest, fam_interest, rit_interest)
        
        retrieval_sources = candidate.get("retrieval_sources", [])
        is_strictly_explore = (retrieval_sources == ["exploration"])
        
        if not is_strictly_explore and best_interest_pct <= 1.5 and len(interests) > 0 and (category in interests or family in interests):
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
