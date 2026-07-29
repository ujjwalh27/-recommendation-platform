import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.regression.regression_runner import RegressionRunnerEngine

def main():
    print("==========================================================================")
    print("       PMCLP AUTOMATED REGRESSION TESTING FRAMEWORK CLI")
    print("==========================================================================")

    engine = RegressionRunnerEngine()
    result = engine.run_regression_test()

    print(f"Deployment Gate Status: {result['deployment_gate_status']}")
    print(f"Overall Accuracy: {result['overall_accuracy']}%")
    print(f"Overall F1 Score: {result['overall_f1_score']}")
    print(f"ECE Calibration Score: {result['ece_score']}")
    print(f"Average Inference Latency: {result['average_latency_ms']} ms")
    print(f"\nResult saved to production_monitoring/latest_regression_result.json")

if __name__ == "__main__":
    main()
