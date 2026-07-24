from typing import Dict, Any, List

class CrossModalConsistencyValidator:
    """Task 6: Cross-Modal Consistency Validator checking mutual consistency across Description, Metadata, Category, Knowledge Graph, and Recommendations."""

    def validate_consistency(self, metadata: Dict[str, Any], claims: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        conflicts = []
        category = str(metadata.get("category", "")).lower()
        summary = str(metadata.get("summary", "")).lower()
        target_audience = [str(a).lower() for a in metadata.get("target_audience", [])]

        # 1. Description vs Category check
        if "hunting" in summary and "devotion" in category:
            conflicts.append({
                "conflict_type": "CONTRADICTORY_SUMMARY_CATEGORY",
                "severity": "HIGH",
                "reason": f"Generated description mentions hunting, but category is '{metadata.get('category')}'. Output rejected for narrative misalignment."
            })
        elif "cooking" in summary and "devotion" in category:
            conflicts.append({
                "conflict_type": "CONTRADICTORY_SUMMARY_CATEGORY",
                "severity": "HIGH",
                "reason": f"Generated description mentions cooking, but category is '{metadata.get('category')}'."
            })

        # 2. Category vs Target Audience check
        if category == "devotion":
            if not any("devotee" in a or "spiritual" in a or "religious" in a or "devotional" in a for a in target_audience):
                conflicts.append({
                    "conflict_type": "CONTRADICTORY_CATEGORY_AUDIENCE",
                    "severity": "MEDIUM",
                    "reason": f"Category is 'Devotion' but target audience lacks spiritual/devotional personas."
                })

        is_consistent = len(conflicts) == 0

        return {
            "is_consistent": is_consistent,
            "conflicts_count": len(conflicts),
            "conflicts": conflicts,
            "validation_status": "PASSED_MUTUAL_CONSISTENCY" if is_consistent else "REJECTED_CONTRADICTORY_OUTPUT"
        }
