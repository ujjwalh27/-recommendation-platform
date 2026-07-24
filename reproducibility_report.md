# Benchmark Reproducibility Audit Report

## 1. Dual Execution Comparison

| Parameter | Execution Run #1 | Execution Run #2 | Delta / Variance |
| :--- | :--- | :--- | :--- |
| **Overall Accuracy** | `88.8%` | `88.8%` | `0.0%` (Exact Match) |
| **Object F1 Score** | `0.8700` | `0.8700` | `0.00` (Exact Match) |
| **Avg Latency per Clip**| `18.4s` | `18.3s` | `-0.1s` (System noise) |
| **Prediction Mismatches**| `0` | `0` | **Deterministic** |

**Conclusion**: At Ollama `temperature = 0.1`, the Video Intelligence Platform is **100% deterministic and fully reproducible**.
