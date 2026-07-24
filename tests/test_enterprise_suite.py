import os
import sys
import unittest

# Add project root to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.evaluation.framework import ProductionEvaluationFramework
from src.monitoring.observability import SystemObservabilityMonitor
from src.confidence.calibration import ConfidenceCalibrationEngine
from src.feedback.repository import FeedbackRepository
from src.models.registry import ModelRegistry
from src.explainable_reasoning import ExplainableReasoningEngine

class TestEnterpriseSuite(unittest.TestCase):
    """Task 9: Comprehensive Automated Test Suite covering Unit, Integration, Regression, and System Verification."""

    def test_01_unit_evaluation_framework(self):
        eval_fw = ProductionEvaluationFramework()
        res = eval_fw.evaluate_pipeline_output({"metadata": {"category": "Devotion"}}, {"category": "Devotion"})
        self.assertIn("semantic_accuracy", res)
        self.assertGreaterEqual(res["semantic_accuracy"], 0.90)

    def test_02_unit_confidence_calibration(self):
        cal_engine = ConfidenceCalibrationEngine()
        res = cal_engine.calibrate_predictions({"title": "Test Clip"}, 0.92)
        self.assertFalse(res["is_flagged_for_review"])
        self.assertEqual(res["calibrated_confidence"], 0.92)

    def test_03_unit_feedback_repository(self):
        repo = FeedbackRepository(store_file="datasets/processed/test_feedback.json")
        repo.record_feedback("video_test", "reviewer_01", {"category": "Food"}, {"category": "Devotion"})
        self.assertGreaterEqual(len(repo.feedback_list), 1)

    def test_04_unit_model_registry(self):
        reg = ModelRegistry()
        vlm_status = reg.get_model_status("multimodal_vlm")
        self.assertEqual(vlm_status.get("status"), "DEPLOYED")

    def test_05_integration_observability(self):
        mon = SystemObservabilityMonitor(metrics_file="datasets/processed/test_metrics.json")
        mon.record_run("v_001", 12.5, 0.94)
        self.assertGreaterEqual(mon.metrics["total_videos_processed"], 1)

    def test_06_e2e_pipeline_execution(self):
        test_video = "/Users/ujjwalhkumar/Downloads/daiv sample/Aditi Atul Jadhav.mp4"
        if os.path.exists(test_video):
            engine = ExplainableReasoningEngine()
            res = engine.process_video_with_explainability(test_video, "e2e_test_video")
            self.assertIn("claims", res)
            self.assertIn("metadata_view", res)
            self.assertEqual(len(res["embedding_vector"]), 384)

if __name__ == "__main__":
    unittest.main()
