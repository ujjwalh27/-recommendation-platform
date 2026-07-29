"""
Automated Content Publisher Engine
Orchestrates publication pre-conditions, duplicate detection, lifecycle evaluation, incremental FAISS indexing, catalog persistence, and feed synchronization.
"""

import time
import os
import numpy as np
from typing import Dict, Any, Tuple, Optional
from content_catalog.catalog.store import ContentCatalogStore
from content_catalog.duplicate_detection.detector import DuplicateDetector
from content_catalog.lifecycle.manager import LifecycleManager
from content_catalog.lifecycle.states import ProcessingState, PublicationAction
from content_catalog.incremental_index.faiss_updater import IncrementalFaissUpdater
from content_catalog.synchronization.synchronizer import CatalogFeedSynchronizer
from content_catalog.audit.logger import AuditLogger


class ContentPublisher:
    """Orchestrates end-to-end publishing of processed content into the production catalog and live recommendation feed."""

    def __init__(self, recommender_service: Optional[Any] = None):
        self.store = ContentCatalogStore()
        self.detector = DuplicateDetector(store=self.store)
        self.lifecycle_mgr = LifecycleManager(store=self.store)
        self.faiss_updater = IncrementalFaissUpdater()
        self.synchronizer = CatalogFeedSynchronizer(recommender_service=recommender_service)
        self.audit_logger = AuditLogger()

    def validate_preconditions(self, pipeline_result: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Validates publishing pre-conditions:
        - Content Intelligence analysis succeeded
        - CMREE canonical metadata present
        - Embedding vector present (384-dim)
        """
        if not pipeline_result:
            return False, "Pipeline result is empty."

        status = pipeline_result.get("overall_confidence", 0.0)
        if status <= 0.0 and pipeline_result.get("processing_status") == "FAILED":
            return False, "Content Intelligence pipeline execution failed."

        cmree = pipeline_result.get("canonical_metadata")
        if not cmree or not isinstance(cmree, dict):
            return False, "CMREE canonical metadata missing or invalid."

        embedding = pipeline_result.get("embedding")
        if embedding is None:
            # Fallback check inside CMREE or pipeline result
            embedding = cmree.get("embedding")
            
        if embedding is None or len(embedding) == 0:
            return False, "384-dimensional canonical embedding vector missing."

        return True, None

    def publish_video(
        self,
        video_file_path: str,
        pipeline_result: Dict[str, Any],
        video_id: Optional[str] = None,
        request_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Main entry point for publishing a processed video.
        Returns detailed publication report.
        """
        start_time = time.time()
        target_id = video_id or pipeline_result.get("video_id") or "unknown_video"

        # 1. Validate publishing pre-conditions
        valid, err_msg = self.validate_preconditions(pipeline_result)
        if not valid:
            duration_ms = (time.time() - start_time) * 1000.0
            print(f"[ContentPublisher] Publication BLOCKED for '{target_id}': {err_msg}")
            
            self.audit_logger.log_event(
                video_id=target_id,
                content_hash="N/A",
                processing_result="FAILED",
                duplicate_detected=False,
                publication_action=PublicationAction.FAIL.value,
                processing_duration_ms=duration_ms,
                details={"failure_reason": err_msg},
                request_id=request_id
            )
            
            return {
                "video_id": target_id,
                "publication_status": "BLOCKED",
                "publication_action": PublicationAction.FAIL.value,
                "failure_reason": err_msg,
                "duplicate_detected": False,
                "duration_ms": duration_ms
            }

        # 2. Duplicate Detection (SHA-256 Hashing)
        is_dup, content_hash, existing_record = self.detector.check_duplicate(video_file_path, target_id)
        if is_dup and existing_record:
            target_id = existing_record["video_id"]

        # 3. Lifecycle Evaluation & Versioning
        action, catalog_record = self.lifecycle_mgr.evaluate_reprocessing(
            video_id=target_id,
            content_hash=content_hash,
            pipeline_result=pipeline_result
        )

        duration_ms = (time.time() - start_time) * 1000.0

        # 4. Handle Publication Action
        if action == PublicationAction.SKIP:
            self.audit_logger.log_event(
                video_id=target_id,
                content_hash=content_hash,
                processing_result="SUCCESS",
                duplicate_detected=True,
                publication_action=PublicationAction.SKIP.value,
                processing_duration_ms=duration_ms,
                details={"message": "No Changes Detected. Publication skipped."},
                request_id=request_id
            )
            
            return {
                "video_id": target_id,
                "publication_status": "SKIPPED",
                "publication_action": PublicationAction.SKIP.value,
                "duplicate_detected": True,
                "message": "No Changes Detected.",
                "record": catalog_record,
                "duration_ms": duration_ms
            }

        # 5. Incremental FAISS Index Update (Insert or In-Place Replace)
        embedding = pipeline_result.get("embedding")
        if embedding is not None:
            self.faiss_updater.upsert_vector(target_id, embedding)

        # 6. Upsert Catalog Store (content_catalog.json)
        self.store.upsert(catalog_record)

        # 7. Real-Time Recommendation Feed Memory Synchronization
        self.synchronizer.synchronize(catalog_record)

        # 8. Record Audit Log Trail
        self.audit_logger.log_event(
            video_id=target_id,
            content_hash=content_hash,
            processing_result="SUCCESS",
            duplicate_detected=is_dup,
            publication_action=action.value,
            processing_duration_ms=duration_ms,
            details={
                "metadata_version": catalog_record.get("metadata_version", 1),
                "category": catalog_record.get("category")
            },
            request_id=request_id
        )

        print(f"[ContentPublisher] Successfully published '{target_id}'. Action: {action.value}")

        return {
            "video_id": target_id,
            "publication_status": "PUBLISHED",
            "publication_action": action.value,
            "duplicate_detected": is_dup,
            "metadata_version": catalog_record.get("metadata_version", 1),
            "record": catalog_record,
            "duration_ms": duration_ms
        }
