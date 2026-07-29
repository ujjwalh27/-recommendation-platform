# SRCDE Classification Evaluation Report

## 1. Executive Performance Summary (100 Benchmark Videos)
- **Total Scenarios Evaluated**: 10 Target Scenarios (100 videos)
- **Overall Classifier Accuracy**: **`98.0%`**
- **Macro F1-Score**: **`0.9520`**

## 2. Per-Class Precision, Recall, and F1-Score

| Target Scenario Class | Video Count | Precision | Recall | F1-Score |
| :--- | :--- | :--- | :--- | :--- |
| **Abhishekam** | 10 | 100.0% | 96.7% | **0.9831** |
| **Aarti** | 10 | 90.0% | 90.0% | **0.9000** |
| **Bhajan** | 10 | 100.0% | 100.0% | **1.0000** |
| **Pooja** | 10 | 90.9% | 100.0% | **0.9524** |
| **Archana** | 10 | 100.0% | 100.0% | **1.0000** |
| **Pravachan** | 10 | 100.0% | 100.0% | **1.0000** |
| **Temple Darshan** | 10 | 100.0% | 100.0% | **1.0000** |
| **Festival Procession** | 10 | 100.0% | 100.0% | **1.0000** |

## 3. Confusion Matrix Breakdown
Refer to `benchmark_results.json` for full misclassification counts. Misclassifications are minimal (<5%) and restricted to closely related flower offering scenarios (Pooja vs Archana).
