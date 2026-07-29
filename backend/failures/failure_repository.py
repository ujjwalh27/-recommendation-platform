import os
import json
from typing import Dict, Any, List

FAILURES_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "failure_repository.json")

class FailureRepositoryManager:
    """
    Module 4 – Failure Repository Manager.
    Stores and indexes structured failure records when predictions are corrected.
    """

    def __init__(self):
        if not os.path.exists(FAILURES_FILE):
            with open(FAILURES_FILE, "w", encoding="utf-8") as f:
                json.dump([], f)

    def log_failure(self, failure_record: Dict[str, Any]) -> Dict[str, Any]:
        failures = self.get_failures()
        failures.insert(0, failure_record)
        with open(FAILURES_FILE, "w", encoding="utf-8") as f:
            json.dump(failures, f, indent=2)
        return failure_record

    def get_failures(self) -> List[Dict[str, Any]]:

        if os.path.exists(FAILURES_FILE):
            try:
                with open(FAILURES_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return []

    def get_failure_by_id(self, failure_id: str) -> Dict[str, Any]:
        failures = self.get_failures()
        for f in failures:
            if f.get("failure_id") == failure_id or f.get("video_id") == failure_id:
                return f
        return {}
