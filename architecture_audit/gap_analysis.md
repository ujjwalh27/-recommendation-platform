# RAIA Task 9: Gap Analysis & Technical Deficit Assessment

## Overview

This document compares the current recommendation system capabilities against the target semantic recommendation architecture, prioritizing technical gaps by implementation effort and expected performance impact.

---

## Target vs. Current State Comparison Matrix

| Architectural Capability | Current State | Target Semantic Architecture | Technical Gap Severity | Priority |
|:---|:---|:---|:---:|:---:|
| **Canonical Metadata Indexing** | Partial (CMREE integrated in CIP; catalog `enriched_videos.json` lacks canonical fields for all 7,010 items) | Full catalog (100% of videos indexed with `primary_ritual`, `ritual_family`, `primary_deity`, `temple`) | **HIGH**: Catalog metadata mismatch | **P1 (Immediate)** |
| **Semantic Text Embeddings** | Generic input text (`caption + category + subcategory + keywords`) | CMREE Canonical Embedding Text (`Category | Ritual | Family | Deity | Temple | Offerings`) | **HIGH**: Embeddings lack domain precision | **P1 (Immediate)** |
| **Candidate Retrieval Channels** | 7 generic channels (Trending, Category, FAISS, CF, Creator, Exploration, Fresh) | 9 channels (Includes **Deity Affinity Channel** & **Ritual Family Channel**) | **MEDIUM**: Missing domain retrieval channels | **P2 (High)** |
| **Semantic Ranking Signals** | Generic category interest matching in `InterestSignal` | Multi-tiered semantic alignment matching (`Category` + `Ritual Family` + `Deity` + `Sampradaya`) | **MEDIUM**: Generic scoring weights | **P2 (High)** |
| **Metadata Quality Gating** | No confidence threshold gating | Filters out predictions with `cmree_confidence < 0.60` | **MEDIUM**: No quality gating | **P2 (High)** |
| **Vector Refresh Workflow** | Manual script invocation | Automated background re-indexing pipeline triggered on metadata updates | **MEDIUM**: Static vector index | **P3 (Medium)** |
| **Retrieval Evaluation Metrics** | Basic evaluation framework (diversity ratio, score spread) | Semantic retrieval metrics (NDCG@K, Recall@K on ground truth rituals/deities) | **LOW**: Basic offline evaluation | **P3 (Medium)** |

---

## Gap Prioritization Matrix

```
       HIGH IMPACT │ ┌─────────────────────────┐  ┌─────────────────────────┐
                   │ │  P1: Canonical Metadata │  │  P1: CMREE Canonical    │
                   │ │      Catalog Upgrade    │  │      Vector Indexing    │
                   │ └─────────────────────────┘  └─────────────────────────┘
                   │ ┌─────────────────────────┐  ┌─────────────────────────┐
                   │ │  P2: Deity & Ritual     │  │  P2: Semantic Ranking   │
                   │ │      Retrieval Channels │  │      Scorer Refactor    │
                   │ └─────────────────────────┘  └─────────────────────────┘
        LOW IMPACT │ ┌─────────────────────────┐  ┌─────────────────────────┐
                   │ │  P3: Vector Refresh     │  │  P3: Retrieval Metrics  │
                   │ │      Automated Workflow │  │      (NDCG@K / Recall) │
                   │ └─────────────────────────┘  └─────────────────────────┘
                   └─────────────────────────────────────────────────────────
                               LOW EFFORT                  HIGH EFFORT
```
