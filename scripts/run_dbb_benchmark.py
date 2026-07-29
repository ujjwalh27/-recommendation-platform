import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.dbb_engine import DaivBenchmarkBuilderEngine

def run_dbb():
    print("==========================================================================")
    print("        DAIV BENCHMARK BUILDER (DBB) EVALUATION RUNNER")
    print("==========================================================================")

    dbb = DaivBenchmarkBuilderEngine()
    taxonomy = dbb.get_taxonomy()
    annotations = dbb.get_all_annotations()

    print(f"Taxonomy Loaded: Version {taxonomy.get('taxonomy_version', '2.0')}")
    print(f"Annotated Benchmark Dataset Records Found: {len(annotations)} Videos")

    eval_results = dbb.run_benchmark_evaluation()

    print(f"\n[DBB Results] Overall Accuracy: {eval_results['overall_accuracy_percent']}%")
    print(f"[DBB Results] Macro F1-Score: {eval_results['macro_f1_score']}")

    with open("dbb_confusion_matrix.json", "w") as f:
        json.dump(eval_results["confusion_matrix"], f, indent=2)

    report_md = f"""# Daiv Benchmark Builder (DBB) Evaluation Report

## 1. Executive Summary
- **Total Ground-Truth Annotated Videos**: `{eval_results['total_annotated_videos']}`
- **Overall Accuracy**: **`{eval_results['overall_accuracy_percent']}%`**
- **Macro F1-Score**: **`{eval_results['macro_f1_score']}`**

## 2. Per-Class Precision, Recall, and F1-Score Breakdown

| Primary Class | Precision | Recall | F1-Score |
| :--- | :--- | :--- | :--- |
"""
    for cls, m in eval_results["per_class_metrics"].items():
        report_md += f"| **{cls}** | {m['precision']*100:.1f}% | {m['recall']*100:.1f}% | **{m['f1_score']:.4f}** |\n"

    report_md += f"""
## 3. Failure Analysis
- Total Misclassifications: {len(eval_results['failure_analysis'])}
"""
    for fail in eval_results["failure_analysis"]:
        report_md += f"- **{fail['video_id']}** ({fail['title']}): Expected `{fail['ground_truth_class']}`, Predicted `{fail['predicted_class']}`. Reason: {fail['evidence_mismatch']}\n"

    with open("dbb_evaluation_report.md", "w") as f:
        f.write(report_md)

    print("\n==========================================================================")
    print("  ALL DBB BENCHMARK EVALUATION ARTIFACTS GENERATED SUCCESSFULLY!")
    print("==========================================================================")

if __name__ == "__main__":
    run_dbb()
