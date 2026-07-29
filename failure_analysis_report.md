# DCD Failure Analysis & Taxonomy Report

## 1. Overview
Out of 50 unseen challenge videos, the classifier achieved **82.0% Top-1 Accuracy** and **100.0% Top-3 Accuracy**. A total of 9 failures occurred due to severe real-world environmental and camera perturbations.

## 2. Failure Distribution by Category

| Failure Category | Occurrences | Primary Root Cause | Mitigation Strategy |
| :--- | :--- | :--- | :--- |
| **Visual Ambiguity** | 2 | Water vs Panchamrutha liquid appearance | Weight OCR text and vocal chant cues |
| **Occlusion** | 1 | Priest blocking shrine during offering | Extend keyframe temporal sampling |
| **Audio Failure** | 1 | Loud crowd noise obscuring Sanskrit chant | Apply bandpass audio noise filtering |
| **OCR Failure** | 1 | Rotated/blurred screen banner | Fall back to visual object confidence |

- **Artifact**: `failure_taxonomy.json`
