from typing import List, Dict, Any


class DiversityFilter:
    """Applies re-ranking / spacing rules to ensure category and creator diversity in the recommendation feed."""

    def __init__(self, max_consecutive_category: int = 1, max_consecutive_creator: int = 1, max_category_ratio: float = 0.3):
        self.max_consecutive_category = max_consecutive_category
        self.max_consecutive_creator = max_consecutive_creator
        self.max_category_ratio = max_category_ratio

    def filter(self, ranked_candidates: List[Dict[str, Any]], limit: int = 20) -> List[Dict[str, Any]]:
        """Re-ranks candidates to avoid consecutive category repetition and category frequency flooding."""
        if not ranked_candidates:
            return []

        selected: List[Dict[str, Any]] = []
        remaining = list(ranked_candidates)

        # Track consecutive counts and global counts of categories and creators
        consecutive_categories: List[str] = []
        consecutive_creators: List[str] = []
        
        # Calculate maximum allowed videos per category globally based on the requested feed limit
        max_allowed_per_category = max(1, int(limit * self.max_category_ratio))
        
        # Strict slot pattern to guarantee a perfect interleaving mix of feed types
        slot_pattern = [
            "personal",      # Slot 0
            "freshness",     # Slot 1
            "exploration",   # Slot 2
            "personal",      # Slot 3
            "freshness",     # Slot 4
            "exploration",   # Slot 5
            "personal",      # Slot 6
            "freshness",     # Slot 7
            "exploration",   # Slot 8
            "trending"       # Slot 9
        ]

        while len(selected) < limit and remaining:
            candidate_index_to_pick = -1
            current_slot = len(selected)
            pattern_source = slot_pattern[current_slot % len(slot_pattern)]

            # 1. Prioritize picking a candidate matching the slot pattern source
            for idx, cand in enumerate(remaining):
                sources = cand.get("retrieval_sources", [])
                
                # Check if candidate matches the target pattern source
                matches = False
                if pattern_source == "personal":
                    matches = any(s in ["similarity", "collaborative_filtering", "creator_affinity", "category"] for s in sources)
                elif pattern_source == "freshness":
                    matches = "freshness" in sources
                elif pattern_source == "exploration":
                    matches = "exploration" in sources
                elif pattern_source == "trending":
                    matches = "trending" in sources
                
                if matches:
                    category = cand.get("matched_category", "Entertainment")
                    category_violates = False
                    if len(consecutive_categories) >= self.max_consecutive_category:
                        last_categories = consecutive_categories[-self.max_consecutive_category:]
                        if all(c == category for c in last_categories):
                            category_violates = True
                    
                    # Check ratio limit
                    category_count = sum(1 for v in selected if v.get("matched_category") == category)
                    ratio_violates = category_count >= max_allowed_per_category
                    
                    if not category_violates and not ratio_violates:
                        candidate_index_to_pick = idx
                        break

            # 2. Fallback to normal scoring selection if no valid candidate matches the slot pattern source
            if candidate_index_to_pick == -1:
                for idx, cand in enumerate(remaining):
                    meta = cand.get("metadata", {})
                    category = cand.get("matched_category", "Entertainment")
                    creator = meta.get("creator", "")
                    
                    # Check consecutive category violation
                    category_violates = False
                    if len(consecutive_categories) >= self.max_consecutive_category:
                        last_categories = consecutive_categories[-self.max_consecutive_category:]
                        if all(c == category for c in last_categories):
                            category_violates = True

                    # Check consecutive creator violation
                    creator_violates = False
                    if creator and len(consecutive_creators) >= self.max_consecutive_creator:
                        last_creators = consecutive_creators[-self.max_consecutive_creator:]
                        if all(cr == creator for cr in last_creators):
                            creator_violates = True

                    # Check global category frequency ratio violation
                    category_count = sum(1 for v in selected if v.get("matched_category") == category)
                    ratio_violates = category_count >= max_allowed_per_category

                    # A candidate is valid if it doesn't violate consecutive limits AND doesn't flood the feed
                    if not category_violates and not creator_violates and not ratio_violates:
                        candidate_index_to_pick = idx
                        break

            # Fallback 1: If all candidates violate ratio limit or consecutive rules,
            # relax the ratio limit check first to find a candidate that at least doesn't violate consecutive limits
            if candidate_index_to_pick == -1:
                for idx, cand in enumerate(remaining):
                    meta = cand.get("metadata", {})
                    category = cand.get("matched_category", "Entertainment")
                    creator = meta.get("creator", "")

                    category_violates = False
                    if len(consecutive_categories) >= self.max_consecutive_category:
                        last_categories = consecutive_categories[-self.max_consecutive_category:]
                        if all(c == category for c in last_categories):
                            category_violates = True

                    creator_violates = False
                    if creator and len(consecutive_creators) >= self.max_consecutive_creator:
                        last_creators = consecutive_creators[-self.max_consecutive_creator:]
                        if all(cr == creator for cr in last_creators):
                            creator_violates = True

                    if not category_violates and not creator_violates:
                        candidate_index_to_pick = idx
                        break

            # Fallback 2: If everything is blocked, just pick the top ranked item
            if candidate_index_to_pick == -1:
                candidate_index_to_pick = 0

            # Pick the candidate, append to selected, remove from remaining
            chosen_candidate = remaining.pop(candidate_index_to_pick)
            selected.append(chosen_candidate)

            # Update history trackers
            consecutive_categories.append(chosen_candidate.get("matched_category", "Entertainment"))
            consecutive_creators.append(chosen_candidate.get("metadata", {}).get("creator", ""))

        return selected
