from typing import Dict, Any


class RecommendationExplainer:
    """Generates natural language explanations for recommended videos based on retrieval channels and interest profiles."""

    def generate_explanation(self, candidate: Dict[str, Any], user_profile: Dict[str, Any]) -> str:
        """Determines the most relevant explanation for a recommendation candidate."""
        sources = candidate.get("retrieval_sources", [])
        category = candidate.get("matched_category", "Pooja & Aarti")
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

    def generate_semantic_explanation(self, candidate: Dict[str, Any], user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Generates deterministic, structured semantic explanations highlighting ritual and category classification."""
        meta = candidate.get("metadata", candidate)
        canonical = meta.get("canonical_metadata") or meta

        video_id = candidate.get("video_id", meta.get("video_id", "unknown"))
        sources = candidate.get("retrieval_sources", [])

        # Map candidate_sources for display
        mapped_sources = []
        for s in sources:
            if s in ["faiss_similarity", "similarity"]: mapped_sources.append("FAISS Semantic Search")
            elif s == "same_ritual_family": mapped_sources.append("Same Ritual Family")
            elif s == "same_primary_deity": mapped_sources.append("Spiritual Theme")
            elif s == "category_retrieval" or s == "category": mapped_sources.append("Category Match")
            elif s == "freshness": mapped_sources.append("Fresh Content")
            elif s == "exploration": mapped_sources.append("Content Discovery")
            else: mapped_sources.append(s.replace("_", " ").title())

        if not mapped_sources:
            mapped_sources = ["Content Discovery"]

        sim_score = round(float(candidate.get("similarity_score", candidate.get("_similarity_score", 0.92))), 2)

        category = meta.get("category") or canonical.get("category") or "Pooja"
        subcategory = meta.get("subcategory") or canonical.get("subcategory") or ""
        family = canonical.get("ritual_family") or meta.get("ritual_family")
        ritual = canonical.get("primary_ritual") or meta.get("primary_ritual")

        # Resolve offering from top-level metadata or canonical metadata
        raw_offerings = meta.get("offering") or meta.get("offerings") or canonical.get("offerings") or canonical.get("offering") or []
        if isinstance(raw_offerings, str):
            raw_offerings = [raw_offerings]

        # Sanity Guardrail: Milk is ONLY offered during Abhishekam (liquid pouring).
        # Remove Milk false positives from Aarti, Bhajan, Pooja, etc.
        offerings = []
        for o in raw_offerings:
            if not o:
                continue
            if "milk" in str(o).lower() and category != "Abhishekam":
                # Replace with appropriate ritual offering
                if category == "Aarti":
                    offerings.append("Camphor & Flame")
                elif category in ["Bhajan", "Kirtan / Nama Sankeerthana"]:
                    offerings.append("Music & Hymns")
                elif category == "Pooja":
                    offerings.append("Flowers & Incense")
                else:
                    offerings.append("Devotional Offering")
            else:
                offerings.append(o)

        # Deduplicate offerings preserving order
        seen_off = set()
        clean_offerings = []
        for o in offerings:
            if o.lower() not in seen_off:
                seen_off.add(o.lower())
                clean_offerings.append(o)

        reasoning = []
        reasoning.append(f"Category: {category}")
        if subcategory and str(subcategory).strip() not in ["None", "N/A", "null", ""]:
            reasoning.append(f"Type: {subcategory}")
        if ritual and str(ritual).strip() not in ["None", "N/A", "null", ""]:
            reasoning.append(f"Primary Ritual: {ritual}")
        elif family and str(family).strip() not in ["None", "N/A", "null", ""]:
            reasoning.append(f"Ritual Family: {family}")
            
        if clean_offerings:
            offering_str = ", ".join([str(o) for o in clean_offerings if o])
            if offering_str:
                reasoning.append(f"Offering: {offering_str}")

        return {
            "recommended_video": video_id,
            "candidate_sources": mapped_sources,
            "semantic_similarity": sim_score,
            "reasoning": reasoning
        }
