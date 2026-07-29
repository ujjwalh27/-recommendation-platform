"""
Task 9 – Validation Suite
Audits generated canonical metadata documents for missing required fields,
conflicting inferences, low-confidence predictions, duplicate keywords, and invalid canonical values.
"""

from typing import Dict, Any, List, Tuple


class MetadataValidator:
    """Audits canonical metadata documents and flags structural, semantic, or confidence errors."""

    def __init__(self):
        self.canonical_categories = {"Temple Ritual", "Devotional Music", "Spiritual Discourse", "Festival Procession", "Temple Darshan"}
        self.canonical_families = {"Abhishekam", "Aarti", "Archana", "Pooja", "Bhajan", "Pravachan", "Procession", "Darshan", "Homa"}

    def validate_canonical_document(self, doc: Dict[str, Any]) -> Tuple[bool, List[Dict[str, Any]]]:
        """
        Validates a canonical document.
        Returns:
            (is_valid, validation_issues)
            where issues list contains dicts with: type, field, message, severity ('error'|'warning')
        """
        issues = []

        # 1. Missing required fields
        required_fields = ["video_id", "primary_category", "primary_ritual", "ritual_family", "primary_deity", "keywords", "confidence"]
        for field in required_fields:
            if not doc.get(field):
                issues.append({
                    "type": "MISSING_FIELD",
                    "field": field,
                    "message": f"Required canonical field '{field}' is missing or empty",
                    "severity": "error"
                })

        # 2. Conflicting Inferences
        ritual = doc.get("primary_ritual", "")
        family = doc.get("ritual_family", "")
        deity = doc.get("primary_deity", "")

        # Conflict example: Jalabhishekam ritual family should be Abhishekam
        if "abhishekam" in ritual.lower() and family != "Abhishekam":
            issues.append({
                "type": "SEMANTIC_CONFLICT",
                "field": "ritual_family",
                "message": f"Ritual '{ritual}' conflicts with family '{family}'. Expected family 'Abhishekam'",
                "severity": "error"
            })

        # 3. Low-Confidence Prediction
        conf = float(doc.get("confidence", 0.0))
        if conf < 0.60:
            issues.append({
                "type": "LOW_CONFIDENCE",
                "field": "confidence",
                "message": f"Confidence {conf:.2f} is below minimum threshold 0.60. Flagged for human review queue.",
                "severity": "warning"
            })

        # 4. Duplicate Keywords
        keywords = doc.get("keywords", [])
        if len(keywords) != len(set(kw.lower() for kw in keywords)):
            issues.append({
                "type": "DUPLICATE_KEYWORDS",
                "field": "keywords",
                "message": "Keywords list contains duplicate entries after case-folding",
                "severity": "warning"
            })

        # 5. Invalid Canonical Values
        if family and family not in self.canonical_families:
            issues.append({
                "type": "UNSUPPORTED_ENTITY",
                "field": "ritual_family",
                "message": f"Ritual family '{family}' is not in approved canonical taxonomy",
                "severity": "error"
            })

        has_errors = any(i["severity"] == "error" for i in issues)
        return not has_errors, issues
