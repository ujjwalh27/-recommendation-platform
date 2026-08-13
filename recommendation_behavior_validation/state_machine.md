# Recommendation Behavioral State Machine

```mermaid
stateDiagram-v2
[*] --> P0_Baseline
P0_Baseline --> P1_Interacted : LIKE / SAVE / SHARE / COMMENT
P1_Interacted --> P1_Interacted : NAVIGATE (Read-Only 0 Delta)
P1_Interacted --> P0_Baseline : UNLIKE / UNSAVE (Revert)
```
