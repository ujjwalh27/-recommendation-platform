from typing import List, Dict, Any


class DiversityFilter:
    """Applies re-ranking / spacing rules to ensure category and creator diversity in the recommendation feed."""

    def __init__(self, max_consecutive_category: int = 1, max_consecutive_creator: int = 1):
        self.max_consecutive_category = max_consecutive_category
        self.max_consecutive_creator = max_consecutive_creator

    def filter(self, ranked_candidates: List[Dict[str, Any]], limit: int = 20) -> List[Dict[str, Any]]:
        """Re-ranks candidates to avoid clustering the same category or creator consecutively."""
        if not ranked_candidates:
            return []

        selected: List[Dict[str, Any]] = []
        remaining = list(ranked_candidates)

        # Track consecutive counts of categories and creators
        consecutive_categories: List[str] = []
        consecutive_creators: List[str] = []

        while len(selected) < limit and remaining:
            candidate_index_to_pick = -1

            # Look for the first candidate that doesn't violate consecutive limits
            for idx, cand in enumerate(remaining):
                meta = cand.get("metadata", {})
                category = cand.get("matched_category", "Entertainment")
                creator = meta.get("creator", "")
                
                # Check category violation
                category_violates = False
                if len(consecutive_categories) >= self.max_consecutive_category:
                    last_categories = consecutive_categories[-self.max_consecutive_category:]
                    if all(c == category for c in last_categories):
                        category_violates = True

                # Check creator violation
                creator_violates = False
                if creator and len(consecutive_creators) >= self.max_consecutive_creator:
                    last_creators = consecutive_creators[-self.max_consecutive_creator:]
                    if all(cr == creator for cr in last_creators):
                        creator_violates = True

                if not category_violates and not creator_violates:
                    candidate_index_to_pick = idx
                    break

            # If all candidates violate the limit (e.g. only one category/creator left),
            # fall back and pick the highest ranked candidate
            if candidate_index_to_pick == -1:
                candidate_index_to_pick = 0

            # Pick the candidate, append to selected, remove from remaining
            chosen_candidate = remaining.pop(candidate_index_to_pick)
            selected.append(chosen_candidate)

            # Update history trackers
            consecutive_categories.append(chosen_candidate.get("matched_category", "Entertainment"))
            consecutive_creators.append(chosen_candidate.get("metadata", {}).get("creator", ""))

        return selected
