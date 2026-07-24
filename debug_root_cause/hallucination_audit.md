# Task 7 – Hallucination Audit Report

## Strict Categorization Matrix

| Statement | Classification | Empirical Basis / Justification |
| :--- | :--- | :--- |
| *"Woman holding flowers and prayer plate"* | **Directly Observed** | Visible in Keyframe 2 (22s) |
| *"Lit oil lamps (deepa) on green tablecloth"* | **Directly Observed** | Visible in Keyframe 1 (0s) and Keyframe 3 (43s) |
| *"Golden idol of Lord Ganesha"* | **Directly Observed** | Visible in Keyframe 1 (0s) |
| *"Hindu home devotional puja ritual"* | **Inferred** | Logically derived from shrine setup, deepa lighting, and flower offerings |
| *"Diwali festival celebration"* | **Assumed (Prevented)** | Flagged and excluded to prevent presenting speculation as fact |

## System Constraint Policy
Inferences are allowed when supported by multiple visual cues. **Assumptions are strictly prohibited** and excluded from final JSON output records.
