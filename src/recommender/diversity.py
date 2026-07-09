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
        
        # Dedicated slots to inject fresh candidates to guarantee impressions (Index 2 and 6)
        fresh_slots = {2, 6}

        while len(selected) < limit and remaining:
            candidate_index_to_pick = -1
            current_slot = len(selected)

            # If this is a dedicated freshness slot, prioritize picking a fresh candidate first
            if current_slot in fresh_slots:
                for idx, cand in enumerate(remaining):
                    if "freshness" in cand.get("retrieval_sources", []):
                        category = cand.get("matched_category", "Entertainment")
                        category_violates = False
                        if len(consecutive_categories) >= self.max_consecutive_category:
                            last_categories = consecutive_categories[-self.max_consecutive_category:]
                            if all(c == category for c in last_categories):
                                category_violates = True
                        
                        # Enforce category ratio cap inside freshness slots
                        category_count = sum(1 for v in selected if v.get("matched_category") == category)
                        ratio_violates = category_count >= max_allowed_per_category
                        
                        if not category_violates and not ratio_violates:
                            candidate_index_to_pick = idx
                            break

            # If not a fresh slot, or no valid fresh candidate was found, perform normal scoring select
            if candidate_index_to_pick == -1:
                # Look for the first candidate that doesn't violate consecutive limits or ratio limits
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
