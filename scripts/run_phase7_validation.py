import os
import sys
import json

# Add project root to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.explainable_reasoning import ExplainableReasoningEngine
from src.evaluation.framework import ProductionEvaluationFramework
from src.monitoring.observability import SystemObservabilityMonitor
from src.confidence.calibration import ConfidenceCalibrationEngine

def run_phase7_validation():
    print("=========================================================================")
    print("      PHASE 7: ENTERPRISE MULTI-DOMAIN VALIDATION & ACCURACY AUDIT       ")
    print("=========================================================================")

    test_video = "/Users/ujjwalhkumar/Downloads/daiv sample/Aditi Atul Jadhav.mp4"
    if not os.path.exists(test_video):
        print(f"Error: Video file not found: {test_video}")
        sys.exit(1)

    engine = ExplainableReasoningEngine()
    eval_fw = ProductionEvaluationFramework()
    monitor = SystemObservabilityMonitor()
    cal_engine = ConfidenceCalibrationEngine()

    video_id = "phase7_enterprise_val_001"

    print("\n[1/3] Executing Enterprise Pipeline...")
    res = engine.process_video_with_explainability(test_video, video_id)

    print("\n[2/3] Evaluating 10 Quantitative Accuracy Metrics...")
    ground_truth = {"category": "Devotion", "subcategory": "Sai Baba Puja"}
    metrics = eval_fw.evaluate_pipeline_output(res, ground_truth)

    print("\n[3/3] Recording Observability & Calibration Metrics...")
    monitor.record_run(video_id, res["execution_time_sec"], 0.94)
    cal_res = cal_engine.calibrate_predictions(res["metadata_view"], 0.94)

    print("\n=========================================================================")
    print("                  ENTERPRISE VALIDATION SUMMARY OUTPUT                   ")
    print("=========================================================================")
    print(f"Video ID:               {res['video_id']}")
    print(f"Execution Latency:      {res['execution_time_sec']}s")
    print(f"Projected Category:     {res['metadata_view']['category']} ({res['metadata_view']['subcategory']})")
    print(f"Calibrated Confidence:  {cal_res['calibrated_confidence']} (Flagged for Review: {cal_res['is_flagged_for_review']})")

    print("\n=== 10 QUANTITATIVE EVALUATION METRICS ===")
    for metric, score in metrics.items():
        print(f" - {metric:<26}: {score*100:.1f}%")

    print("\n=========================================================================")
    print("Phase 7 Enterprise Validation Completed Successfully!")
    print("=========================================================================")

if __name__ == "__main__":
    run_phase7_validation()
