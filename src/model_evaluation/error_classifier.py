from typing import Dict, Any, List

class FailureTaxonomyClassifier:
    """Handles Part 6: Error Analysis and Failure Taxonomy Classification."""

    FAILURE_CLASSES = [
        "Visual misunderstanding",
        "Poor OCR",
        "Speech misunderstanding",
        "Temporal misunderstanding",
        "Scene misunderstanding",
        "Incorrect reasoning",
        "Hallucination",
        "Prompt issue",
        "Model limitation",
        "Ambiguous content"
    ]

    def classify_errors(self, prediction: Dict[str, Any], ground_truth: Dict[str, Any], metrics: Dict[str, float]) -> List[Dict[str, str]]:
        """
        Scans prediction discrepancies against ground truth and categorizes failure modes.
        """
        error_logs = []

        # Check Category / Context discrepancy
        if prediction.get("category", "").lower() != ground_truth.get("expected_category", "").lower():
            error_logs.append({
                "class": "Scene misunderstanding",
                "field": "category",
                "details": f"Predicted '{prediction.get('category')}' instead of expected '{ground_truth.get('expected_category')}'."
            })

        # Check Activity discrepancy
        pred_act = [a.lower() for a in prediction.get("activities", [])]
        gt_act = [a.lower() for a in ground_truth.get("expected_activities", [])]
        if not any(a in " ".join(pred_act) for a in gt_act):
            error_logs.append({
                "class": "Visual misunderstanding",
                "field": "activities",
                "details": f"Failed to detect ground-truth activities {gt_act}."
            })

        # Check Hallucination Rate
        if metrics.get("hallucination_rate", 0.0) > 0.12:
            error_logs.append({
                "class": "Hallucination",
                "field": "entities/objects",
                "details": f"Model asserted unsupported entity tags resulting in a hallucination score of {metrics.get('hallucination_rate')}."
            })

        # Check Language / Speech
        if ground_truth.get("expected_title") and not prediction.get("title"):
            error_logs.append({
                "class": "Speech misunderstanding",
                "field": "title",
                "details": "Model failed to transcribe spoken cues in keyframes."
            })

        if not error_logs:
            error_logs.append({
                "class": "None (Clean Alignment)",
                "field": "all",
                "details": "Model output aligns closely with human ground-truth."
            })

        return error_logs
