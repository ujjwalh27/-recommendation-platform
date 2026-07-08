from typing import Dict, Any


class RecommendationExplainer:
    """Generates natural language explanations for recommended videos based on retrieval channels and interest profiles."""

    def generate_explanation(self, candidate: Dict[str, Any], user_profile: Dict[str, Any]) -> str:
        """Determines the most relevant explanation for a recommendation candidate."""
        sources = candidate.get("retrieval_sources", [])
        category = candidate.get("matched_category", "Entertainment")
        creator = candidate.get("metadata", {}).get("creator", "")
        
        # User interests
        interests = user_profile.get("interests", {})
        top_user_category = max(interests, key=interests.get) if interests else None
        
        # 1. Creator Affinity (highest priority personalization)
        if "creator_affinity" in sources or candidate.get("creator_affinity_score", 0.0) > 10.0:
            if creator:
                return f"Based on your preference for @{creator}."
            return "From a creator you frequently watch."

        # 2. Collaborative Filtering (taste similarity)
        if "collaborative_filtering" in sources:
            return "Recommended because users with similar tastes enjoyed this."

        # 3. Similarity explanation (vector seed match)
        if "similarity" in sources:
            seed_id = candidate.get("similarity_seed")
            if seed_id:
                return "Similar to a clip you recently watched."
            return "Similar to content you recently enjoyed."

        # 4. Category explanation (interests-based)
        if "category" in sources:
            # If it matches the user's primary interest
            if category == top_user_category:
                return f"Based on your strong interest in {category}."
            # General category match
            interest_score = interests.get(category, 0)
            if interest_score > 30:
                return f"Because you watch a lot of {category} clips."
            return f"Popular in {category}."

        # 5. Trending explanation
        if "trending" in sources:
            return "Trending on Daiv Clips."

        # Fallback explanation
        return "Recommended for you."
