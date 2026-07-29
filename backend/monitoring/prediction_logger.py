import os
import json
import time
from typing import Dict, Any, List

LOGS_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "production_monitoring", "prediction_logs.json")

class PredictionLogger:
    """
    Module 1 – Production Prediction Logger.
    Records every production semantic prediction with immutable metadata.
    """

    def __init__(self):
        os.makedirs(os.path.dirname(LOGS_FILE), exist_ok=True)
        if not os.path.exists(LOGS_FILE):
            with open(LOGS_FILE, "w", encoding="utf-8") as f:
                json.dump([], f)

    def log_prediction(self, record: Dict[str, Any]) -> Dict[str, Any]:
        logs = self.get_all_logs()
        logs.insert(0, record)
        with open(LOGS_FILE, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=2)
        return record

    def get_all_logs(self) -> List[Dict[str, Any]]:
        if os.path.exists(LOGS_FILE):
            try:
                with open(LOGS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return []

    def get_log(self, prediction_id: str) -> Dict[str, Any]:
        logs = self.get_all_logs()
        for l in logs:
            if l.get("prediction_id") == prediction_id or l.get("video_id") == prediction_id:
                return l
        return {}
