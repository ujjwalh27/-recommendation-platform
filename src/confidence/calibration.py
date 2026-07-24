from typing import Dict, Any, List

CONFIDENCE_THRESHOLD = 0.60

class ConfidenceCalibrationEngine:
    """Task 4: Confidence Calibration Engine flagging low-trust predictions and providing uncertainty explanations."""

    def calibrate_predictions(self, predictions: Dict[str, Any], confidence_score: float) -> Dict[str, Any]:
        is_low_confidence = confidence_score < CONFIDENCE_THRESHOLD

        return {
            "prediction": predictions,
            "calibrated_confidence": round(confidence_score, 3),
            "is_flagged_for_review": is_low_confidence,
            "threshold": CONFIDENCE_THRESHOLD,
            "uncertainty_explanation": (
                "High confidence grounded by multi-modal evidence concurrence."
                if not is_low_confidence else
                "Low confidence prediction (< 0.60). Flagged for human reviewer verification."
            )
        }
