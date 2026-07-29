"""
Event Logging & Audit Trail Engine
Maintains persistent audit logs for all content ingestion and publishing events.
"""

import os
import json
import time
import uuid
from typing import Dict, Any, List, Optional
from src.utils.paths import get_path


class AuditLogger:
    """Logs and persists structured audit events to catalog_audit_logs.json."""

    def __init__(self):
        self.log_path = get_path("datasets/processed/catalog_audit_logs.json")
        self._logs: List[Dict[str, Any]] = []
        self._load()

    def _load(self) -> None:
        """Loads audit logs from disk."""
        if os.path.exists(self.log_path):
            try:
                with open(self.log_path, "r", encoding="utf-8") as f:
                    self._logs = json.load(f)
            except Exception as e:
                print(f"[AuditLogger] Error loading audit log: {e}")
                self._logs = []
        else:
            self._logs = []

    def save(self) -> None:
        """Flushes audit logs to disk."""
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        with open(self.log_path, "w", encoding="utf-8") as f:
            json.dump(self._logs, f, indent=2, ensure_ascii=False)

    def log_event(
        self,
        video_id: str,
        content_hash: str,
        processing_result: str,
        duplicate_detected: bool,
        publication_action: str,
        processing_duration_ms: float,
        details: Optional[Dict[str, Any]] = None,
        request_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Creates and records an audit log entry."""
        req_id = request_id or f"req_{uuid.uuid4().hex[:12]}"
        event = {
            "request_id": req_id,
            "video_id": video_id,
            "content_hash": content_hash,
            "processing_result": processing_result,
            "duplicate_detected": duplicate_detected,
            "publication_action": publication_action,
            "processing_duration_ms": round(processing_duration_ms, 2),
            "timestamp": time.time(),
            "details": details or {}
        }
        self._logs.append(event)
        self.save()
        return event

    def get_logs_for_video(self, video_id: str) -> List[Dict[str, Any]]:
        """Retrieves audit trail entries for a specific video ID."""
        return [log for log in self._logs if log.get("video_id") == video_id]

    def list_all_logs(self) -> List[Dict[str, Any]]:
        """Returns all recorded audit logs."""
        return self._logs
