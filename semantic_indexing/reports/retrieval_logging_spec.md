# CSIEI Task 7: Structured Candidate Retrieval Logging Specification

## Overview

The `CandidateRetrievalLogger` records structured JSON logs for every candidate retrieval execution. This enables offline auditability, latency tracking, and metric evaluation without degrading runtime recommendation performance.

---

## Log Schema Definition

```json
{
  "request_id": "req_a1b2c3d4",
  "query_video": "video_ci_1784804233",
  "embedding_model": "all-MiniLM-L6-v2",
  "candidate_sources": [
    "FAISS Semantic Search",
    "Same Primary Deity",
    "Same Ritual Family"
  ],
  "retrieved_candidates": [
    "video_ci_1784874288",
    "video_ci_1784874510",
    "video_ci_1784874588"
  ],
  "retrieval_latency_ms": 1.45,
  "semantic_similarity_scores": [
    0.985,
    0.942,
    0.918
  ],
  "timestamp": "2026-07-27T16:10:00Z"
}
```

---

## Logging Storage Path
- **File Path**: `datasets/processed/retrieval_logs.json`
- **Retention Strategy**: Automatically retains the last 500 retrieval request events.
