# Production Confidence Calibration Report

## 1. Reliability & Calibration Bins

| Confidence Bin Range | Total Predictions | Actual Measured Accuracy | Calibration Status |
| :--- | :--- | :--- | :--- |
| **0.90 – 1.00** | 68 | **95.6%** | Well-Calibrated |
| **0.75 – 0.89** | 22 | **81.8%** | Well-Calibrated |
| **0.50 – 0.74** | 10 | **50.0%** | Slight Overconfidence |

- **Overconfidence Rate**: `3.8%`
- **Underconfidence Rate**: `1.2%`

## 2. Calibration Mechanics
Confidence scores are calculated via `ConfidenceEngine` using a weighted 3-factor formula:
`Score = (0.50 * VLM_Conf) + (0.30 * Modal_Agreement) + (0.20 * Completeness)`
