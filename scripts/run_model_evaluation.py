import os
import sys

# Add project root to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.model_evaluation import MultimodalBenchmarkHarness

def main():
    print("==================================================")
    print("Phase 4: Multimodal Foundation Model Benchmarking")
    print("==================================================")

    harness = MultimodalBenchmarkHarness(gold_standard_path="docs/gold_standard_dataset.json")
    results = harness.run_benchmark_suite()

    comp_report, arch_report = harness.generate_reports(results)

    print("\n==================================================")
    print("PHASE 4 BENCHMARK SUITE COMPLETED SUCCESSFULLY!")
    print("==================================================")

    print("\n=== MODEL RANKING & SEMANTIC ACCURACY SUMMARY ===")
    ranked_models = sorted(
        results.items(),
        key=lambda x: x[1]["average_metrics"]["semantic_understanding_accuracy"],
        reverse=True
    )

    for rank, (m_name, res) in enumerate(ranked_models, 1):
        m = res["average_metrics"]
        print(f"Rank #{rank}: {m_name:<16} | Semantic Acc: {m['semantic_understanding_accuracy']*100:.1f}% | Human Agreement: {m['human_agreement_score']*100:.1f}% | Hallucination Rate: {m['hallucination_rate']*100:.1f}%")

    print("\n=== GENERATED DELIVERABLE REPORTS ===")
    print(f"1. Model Comparison Report: {comp_report}")
    print(f"2. Architecture Validation Report: {arch_report}")
    print(f"3. Human Gold-Standard Dataset: docs/gold_standard_dataset.json")

    print("\n==================================================")
    print("Verification Completed Successfully!")
    print("==================================================")

if __name__ == "__main__":
    main()
