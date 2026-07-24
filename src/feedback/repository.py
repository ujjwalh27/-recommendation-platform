import os
import time
import json
from typing import Dict, Any, List

FEEDBACK_STORE_PATH = "datasets/processed/feedback_repository.json"

class FeedbackRepository:
    """Tasks 5 & 6: Human Feedback Repository capturing reviewer approvals, corrections, and persona edits."""

    def __init__(self, store_file: str = None):
        self.store_file = store_file or FEEDBACK_STORE_PATH
        os.makedirs(os.path.dirname(self.store_file), exist_ok=True)
        self.feedback_list = self._load_feedback()

    def _load_feedback(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.store_file):
            try:
                with open(self.store_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return []

    def record_feedback(
        self,
        video_id: str,
        reviewer: str,
        original_pred: Dict[str, Any],
        corrected_val: Dict[str, Any],
        reason: str = "Category / Metadata Correction"
    ):
        entry = {
            "feedback_id": f"fb_{int(time.time())}_{video_id}",
            "video_id": video_id,
            "reviewer": reviewer,
            "timestamp": time.time(),
            "original_prediction": original_pred,
            "corrected_prediction": corrected_val,
            "reason": reason
        }
        self.feedback_list.append(entry)
        try:
            with open(self.store_file, "w", encoding="utf-8") as f:
                json.dump(self.feedback_list, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[FeedbackRepository] Error persisting feedback: {e}")
