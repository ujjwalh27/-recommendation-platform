import os
import json
import time
from typing import Dict, Any, List

REVIEW_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "production_monitoring", "pending_reviews.json")

class HumanReviewQueueManager:
    """
    Module 3 – Human Review Queue Manager.
    Automatically routes low-confidence, unknown entity, or modality disagreement predictions for human review.
    """

    def __init__(self):
        os.makedirs(os.path.dirname(REVIEW_FILE), exist_ok=True)
        if not os.path.exists(REVIEW_FILE):
            self._init_seed_reviews()

    def get_pending_reviews(self) -> List[Dict[str, Any]]:
        if os.path.exists(REVIEW_FILE):
            try:
                with open(REVIEW_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return []

    def approve_review(self, review_id: str, reviewer: str = "Admin") -> Dict[str, Any]:
        reviews = self.get_pending_reviews()
        updated = [r for r in reviews if r.get("review_id") != review_id and r.get("video_id") != review_id]
        with open(REVIEW_FILE, "w", encoding="utf-8") as f:
            json.dump(updated, f, indent=2)
        return {"status": "SUCCESS", "message": f"Review {review_id} approved by {reviewer}"}

    def correct_review(self, review_id: str, correction: Dict[str, Any]) -> Dict[str, Any]:
        reviews = self.get_pending_reviews()
        target = next((r for r in reviews if r.get("review_id") == review_id or r.get("video_id") == review_id), None)
        
        updated = [r for r in reviews if r.get("review_id") != review_id and r.get("video_id") != review_id]
        with open(REVIEW_FILE, "w", encoding="utf-8") as f:
            json.dump(updated, f, indent=2)

        # Log failure record when prediction is corrected
        from backend.failures.failure_repository import FailureRepositoryManager
        fail_mgr = FailureRepositoryManager()
        fail_record = {
            "failure_id": f"fail_{int(time.time())}",
            "video_id": target.get("video_id", review_id) if target else review_id,
            "predicted_class": target.get("predicted_class", "Pooja") if target else "Pooja",
            "correct_class": correction.get("correct_class", "Abhishekam"),
            "failure_type": correction.get("failure_type", "Visual Ambiguity"),
            "root_cause": correction.get("root_cause", "Corrected by reviewer in Human Review Queue"),
            "reviewer": correction.get("reviewer", "Reviewer_Senior"),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        fail_mgr.log_failure(fail_record)

        return {"status": "SUCCESS", "message": f"Review {review_id} corrected and failure logged.", "failure_record": fail_record}

    def _init_seed_reviews(self):
        seed = [
            {
                "review_id": "rev_001",
                "video_id": "video_ci_1001",
                "title": "Evening Shrine Aarti Stream",
                "predicted_class": "Pooja",
                "confidence": 0.62,
                "routing_reason": "Confidence below threshold (0.62 < 0.75)",
                "timestamp": "2026-07-27 09:30:00"
            },
            {
                "review_id": "rev_002",
                "video_id": "video_ci_1002",
                "title": "Chandi Homa Yajna Stream",
                "predicted_class": "Home Pooja",
                "confidence": 0.68,
                "routing_reason": "Unknown ritual 'Chandi Homa' detected",
                "timestamp": "2026-07-27 10:15:00"
            }
        ]
        with open(REVIEW_FILE, "w", encoding="utf-8") as f:
            json.dump(seed, f, indent=2)
