"""
Task 7 – Candidate Retrieval Logger
Records structured recommendation retrieval logs for offline evaluation, debugging, and auditability.
"""

import os
import json
import time
import uuid
from typing import Dict, Any, List
from src.utils.paths import get_path


class CandidateRetrievalLogger:
    """Logs candidate generation retrieval events to a structured JSON file store."""

    def __init__(self, log_path: str = None):
        if log_path is None:
            log_path = get_path("datasets/processed/retrieval_logs.json")
        self.log_path = log_path
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)

    def log_retrieval_event(
        self,
        query_video: str,
        embedding_model: str,
        candidate_sources: List[str],
        retrieved_candidates: List[str],
        retrieval_latency_ms: float,
        semantic_similarity_scores: List[float]
    ) -> Dict[str, Any]:
        """
        Records a structured retrieval log entry.
        """
        entry = {
            "request_id": f"req_{uuid.uuid4().hex[:8]}",
            "query_video": str(query_video),
            "embedding_model": embedding_model,
            "candidate_sources": candidate_sources,
            "retrieved_candidates": [str(c) for c in retrieved_candidates],
            "retrieval_latency_ms": round(retrieval_latency_ms, 2),
            "semantic_similarity_scores": [round(float(s), 4) for s in semantic_similarity_scores],
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }

        # Append to log file safely
        existing = []
        if os.path.exists(self.log_path):
            try:
                with open(self.log_path, "r", encoding="utf-8") as f:
                    existing = json.load(f)
            except Exception:
                existing = []

        existing.append(entry)

        with open(self.log_path, "w", encoding="utf-8") as f:
            json.dump(existing[-500:], f, indent=2)  # Keep last 500 logs

        return entry
