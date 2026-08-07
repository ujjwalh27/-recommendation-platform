# Evidence Graph Architecture Report

## Overview

The MSFACR engine introduces an internal **Evidence Graph** represented as a Directed Acyclic Graph (DAG). It links raw perception streams through model nodes and evidence nodes down to inferred metadata fields.

---

## Directed Acyclic Graph Structure

```
                      [Perception Stream Root]
                                 │
     ┌───────────┬───────────────┼───────────────┬───────────┐
     ▼           ▼               ▼               ▼           ▼
[MiniCPM]    [YOLOv11]      [VideoMAE]       [Whisper]     [AST]
     │           │               │               │           │
     ▼           ▼               ▼               ▼           ▼
 [Shrine]     [Lamps]        [Pouring]       [Chanting]   [Bells]
     │           │               │               │           │
     └───────────┴───────┬───────┴───────────────┴───────────┘
                         ▼
           [RULE_LIGHTING_001 Evaluation]
                         │
                         ▼
        [Perceptual Field: Lighting = Warm / Oil Lamp Lit]
```

---

## Node & Edge Statistics Across Catalog

* **Structure**: `DIRECTED_ACYCLIC_GRAPH`
* **Average Nodes per Video**: `24`
* **Average Edges per Video**: `38`
* **Node Types**: `ROOT`, `MODEL`, `PERCEPTUAL_FIELD`, `EMOTIONAL_FIELD`
* **Edge Relations**: `EXTRACTED_BY`, `SUPPORTS_INFERENCE`
