# HRCE Classification Evaluation Report

## 1. Overall Performance Metrics (350 Benchmark Videos)
- **Total Benchmark Dataset Size**: 350 Videos (50 videos per ritual class)
- **Overall Accuracy**: **`94.29%`**
- **Macro F1-Score**: **`0.9410`**

## 2. Per-Class Precision, Recall, and F1-Score Breakdown

| Primary Class | Sample Count | True Positives | Precision | Recall | F1-Score |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Abhishekam** | 50 | 48 | 92.3% | 96.0% | **0.9412** |
| **Aarti** | 50 | 48 | 98.0% | 96.0% | **0.9697** |
| **Pooja** | 50 | 47 | 97.9% | 94.0% | **0.9592** |
| **Bhajan** | 50 | 46 | 97.9% | 92.0% | **0.9484** |
| **Pravachan** | 50 | 46 | 97.9% | 92.0% | **0.9484** |
| **Temple Darshan** | 50 | 46 | 86.8% | 92.0% | **0.8932** |
| **Festival Procession** | 50 | 49 | 90.7% | 98.0% | **0.9423** |

## 3. Confusion Matrix Overview
Refer to `classification_confusion_matrix.json` for detailed misclassification counts. Most misclassifications occur between visually similar `Pooja` and `Archana` flower offering clips.
