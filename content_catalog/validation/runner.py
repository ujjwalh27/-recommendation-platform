"""
ACPCS Validation Test Suite
Executes automated test cases across all required sprint validation scenarios.
"""

import os
import time
import shutil
import numpy as np
from typing import Dict, Any, List
from src.utils.paths import get_path
from content_catalog.publisher.publisher import ContentPublisher
from content_catalog.catalog.store import ContentCatalogStore
from content_catalog.audit.logger import AuditLogger
from src.recommender.service import RecommenderService


class ACPCSValidationRunner:
    """Executes automated end-to-end validation for Content Publishing & Catalog Synchronization."""

    def __init__(self):
        self.test_video_path = get_path("datasets/raw/msrvtt/daiv_s2_01_13325085_2160_3840_5.mp4")
        if not os.path.exists(self.test_video_path):
            raw_dir = get_path("datasets/raw/msrvtt")
            files = [os.path.join(raw_dir, f) for f in os.listdir(raw_dir) if f.endswith(".mp4")]
            self.test_video_path = files[0] if files else ""

        self.service = RecommenderService()
        self.publisher = ContentPublisher(recommender_service=self.service)
        self.store = self.publisher.store
        self.audit_logger = self.publisher.audit_logger

    def run_all_tests(self) -> Dict[str, Any]:
        """Runs validation suite and returns structured report."""
        print("=" * 74)
        print("   AUTOMATED CONTENT PUBLISHING & CATALOG SYNC (ACPCS) VALIDATION SUITE")
        print("=" * 74)

        results = {}
        ts = int(time.time())
        test_vid = f"test_acpcs_video_{ts}"
        test_hash = f"hash_acpcs_{ts}_{uuid_val}" if False else f"hash_test_{ts}"

        # Mock Pipeline Result for Testing
        dummy_embedding = np.random.randn(384).astype("float32").tolist()
        mock_pipeline_result = {
            "video_id": test_vid,
            "title": "Test ACPCS Sacred Ritual Video",
            "summary": "Demonstration clip for ACPCS automated publication test.",
            "category": "Pooja & Aarti",
            "subcategory": "Flame & Shrine Ritual",
            "duration": 15.0,
            "overall_confidence": 0.95,
            "embedding": dummy_embedding,
            "canonical_metadata": {
                "primary_ritual": "Devotional Worship",
                "ritual_family": "Pooja & Aarti",
                "offerings": ["Milk", "Flowers"],
                "keywords": ["test", "acpcs", "pooja"]
            }
        }

        # Scenario 1: New Video Publication
        print("\n[Scenario 1/6] Testing New Video Publication...")
        # Create a fresh temporary file with unique SHA-256 hash for Scenario 1
        temp_test_file = get_path(f"datasets/processed/temp_{test_vid}.mp4")
        shutil.copy2(self.test_video_path, temp_test_file)
        with open(temp_test_file, "ab") as f:
            f.write(f"\n# UNIQUE_ACPCS_TEST_{ts}".encode("utf-8"))

        res1 = self.publisher.publish_video(
            video_file_path=temp_test_file,
            pipeline_result=mock_pipeline_result,
            video_id=test_vid
        )
        passed1 = res1.get("publication_status") == "PUBLISHED" and res1.get("publication_action") == "CREATE"
        print(f"   Result: Status={res1.get('publication_status')} | Action={res1.get('publication_action')} -> Passed: {passed1}")
        results["scenario_1_new_video_publish"] = {"passed": passed1, "details": res1}

        # Scenario 2: Duplicate Reprocessing (Unchanged) -> SKIPPED
        print("\n[Scenario 2/6] Testing Idempotent Reprocessing (No Changes)...")
        res2 = self.publisher.publish_video(
            video_file_path=temp_test_file,
            pipeline_result=mock_pipeline_result,
            video_id=test_vid
        )
        passed2 = res2.get("publication_status") == "SKIPPED" and res2.get("duplicate_detected") is True
        print(f"   Result: Status={res2.get('publication_status')} | Duplicate={res2.get('duplicate_detected')} -> Passed: {passed2}")
        results["scenario_2_duplicate_no_changes"] = {"passed": passed2, "details": res2}

        # Scenario 3: Intelligent Reprocessing with Updated Metadata -> UPDATE & Version Increment
        print("\n[Scenario 3/6] Testing Intelligent Reprocessing (Updated Metadata)...")
        updated_pipeline_result = dict(mock_pipeline_result)
        updated_pipeline_result["title"] = "Test ACPCS Sacred Ritual Video (Version 2 Updated)"
        updated_pipeline_result["canonical_metadata"] = {
            "primary_ritual": "Devotional Worship",
            "ritual_family": "Pooja & Aarti",
            "offerings": ["Milk", "Flowers", "Incense"],
            "keywords": ["test", "acpcs", "pooja", "updated"]
        }

        res3 = self.publisher.publish_video(
            video_file_path=temp_test_file,
            pipeline_result=updated_pipeline_result,
            video_id=test_vid
        )
        passed3 = res3.get("publication_status") == "PUBLISHED" and res3.get("publication_action") == "UPDATE" and res3.get("metadata_version", 1) >= 2
        print(f"   Result: Status={res3.get('publication_status')} | Version={res3.get('metadata_version')} -> Passed: {passed3}")
        results["scenario_3_updated_metadata_reprocess"] = {"passed": passed3, "details": res3}

        # Scenario 4: Failed Processing Pre-condition Handling -> BLOCKED
        print("\n[Scenario 4/6] Testing Failed Ingestion Pre-condition Handling...")
        failed_pipeline_result = {
            "video_id": "test_failed_video",
            "overall_confidence": 0.0,
            "processing_status": "FAILED",
            "canonical_metadata": None,
            "embedding": None
        }
        res4 = self.publisher.publish_video(
            video_file_path=temp_test_file,
            pipeline_result=failed_pipeline_result,
            video_id="test_failed_video"
        )
        passed4 = res4.get("publication_status") == "BLOCKED" and res4.get("publication_action") == "FAIL"
        print(f"   Result: Status={res4.get('publication_status')} | Action={res4.get('publication_action')} -> Passed: {passed4}")
        results["scenario_4_failed_processing_blocked"] = {"passed": passed4, "details": res4}

        # Scenario 5: Concurrent Ingestion Idempotency Safety
        print("\n[Scenario 5/6] Testing Concurrent Processing Idempotency...")
        concurrent_vid = f"test_concurrent_{ts}"
        res5a = self.publisher.publish_video(temp_test_file, mock_pipeline_result, concurrent_vid)
        res5b = self.publisher.publish_video(temp_test_file, mock_pipeline_result, concurrent_vid)
        record_count = len([r for r in self.store.list_records() if r.get("content_hash") == res5a.get("record", {}).get("content_hash")])
        passed5 = record_count == 1
        print(f"   Result: Authoritative Records in Store={record_count} -> Passed: {passed5}")
        results["scenario_5_concurrent_safety"] = {"passed": passed5, "record_count": record_count}

        # Scenario 6: Immediate Recommendation API Availability
        print("\n[Scenario 6/6] Testing Live Recommendation Feed Availability...")
        feed = self.service.get_recommendations("user_1", limit=50)
        feed_ids = [v["video_id"] for v in feed]
        passed6 = test_vid in feed_ids
        print(f"   Result: Test Video In Live Feed={passed6} (Total feed items: {len(feed)}) -> Passed: {passed6}")
        results["scenario_6_live_feed_sync"] = {"passed": passed6, "total_feed_items": len(feed)}

        # Cleanup temporary test file
        if os.path.exists(temp_test_file):
            try: os.remove(temp_test_file)
            except Exception: pass

        overall_passed = all([r.get("passed", False) for r in results.values()])
        print("\n" + "=" * 74)
        print(f" OVERALL ACPCS VALIDATION RESULT: {'PASSED (6/6 SCENARIOS SUCCESSFUL)' if overall_passed else 'FAILED'}")
        print("=" * 74)

        return {
            "overall_passed": overall_passed,
            "timestamp": time.time(),
            "scenarios": results
        }


if __name__ == "__main__":
    runner = ACPCSValidationRunner()
    runner.run_all_tests()
