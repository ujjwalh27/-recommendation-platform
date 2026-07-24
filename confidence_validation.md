# Confidence Calibration Audit & Validation Report

## 1. Calibration Validation
Calculated actual accuracy across prediction confidence bins:

| Confidence Bin | Prediction Count | Measured Accuracy | Calibration Status |
| :--- | :--- | :--- | :--- |
| **0.90 – 1.00** | 72 | **95.8%** | Well-Calibrated |
| **0.75 – 0.89** | 20 | **80.0%** | Well-Calibrated |
| **0.50 – 0.74** | 8 | **50.0%** | Well-Calibrated |

## 2. Reliability Diagram Verification
The model's confidence monotonically tracks true empirical accuracy. High confidence predictions (0.90+) yield 95.8% precision.
