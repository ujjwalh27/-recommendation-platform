# RAIA Task 10: Phased Implementation Roadmap

## Overview

This roadmap defines the sequential, phased implementation plan for integrating CMREE Canonical Metadata into the Recommendation Platform across 8 structured phases.

---

## Phased Execution Roadmap

```
Phase 1: Canonical Metadata Persistence & Catalog Synchronization
   │
   ▼
Phase 2: CMREE Canonical Vector Embedding Generation
   │
   ▼
Phase 3: FAISS Index Re-building & Dynamic Update Service
   │
   ▼
Phase 4: Semantic Candidate Generation (Deity & Ritual Channels)
   │
   ▼
Phase 5: Hybrid Semantic Ranking Scorer Refactor
   │
   ▼
Phase 6: User Behavior & Devotional Preference Modeling
   │
   ▼
Phase 7: Offline Retrieval & Recommendation Evaluation (NDCG@K)
   │
   ▼
Phase 8: Production Rollout, Monitoring & PMCLP Integration
```

---

## Detailed Phase Breakdown

### Phase 1: Canonical Metadata Persistence & Catalog Synchronization
- **Objective**: Synchronize all catalog items in `datasets/processed/enriched_videos.json` with CMREE canonical fields (`primary_ritual`, `ritual_family`, `primary_deity`, `temple`, `tradition`, `offerings`).
- **Dependencies**: CMREE Engine (`reasoning_engine/pipeline.py`).
- **Estimated Complexity**: Low (1–2 days).
- **Risks**: Schema validation mismatches during batch migration.
- **Expected Benefit**: 100% catalog consistency across all recommendation lookup tables.

### Phase 2: CMREE Canonical Vector Embedding Generation
- **Objective**: Generate dense 384-dimensional text embeddings using CMREE Canonical Embedding Text (`Category | Ritual | Family | Deity | Temple | Offerings`).
- **Dependencies**: Phase 1 catalog update, `SentenceTransformer("all-MiniLM-L6-v2")`.
- **Estimated Complexity**: Low (1–2 days).
- **Risks**: Out-of-memory errors during large matrix generation (mitigated by batching).
- **Expected Benefit**: High semantic clustering precision for ritual and deity similarity search.

### Phase 3: FAISS Index Re-building & Dynamic Update Service
- **Objective**: Rebuild `models/video.index` and `datasets/embeddings/video_embeddings.npy` with canonical embeddings and update `FaissSearchService`.
- **Dependencies**: Phase 2 embeddings.
- **Estimated Complexity**: Low (1 day).
- **Risks**: Index file lock contention during dynamic updates.
- **Expected Benefit**: Sub-2ms vector similarity search returns semantically relevant videos.

### Phase 4: Semantic Candidate Generation (Deity & Ritual Channels)
- **Objective**: Implement 2 new candidate retrieval channels in `CandidateGenerator`:
  1. `retrieve_by_deity_affinity()`
  2. `retrieve_by_ritual_family()`
- **Dependencies**: Phase 1 catalog update, `CandidateGenerator`.
- **Estimated Complexity**: Medium (2–3 days).
- **Risks**: Candidate pool dilution if thresholds are too broad.
- **Expected Benefit**: Candidate retrieval directly matches user devotional intent.

### Phase 5: Hybrid Semantic Ranking Scorer Refactor
- **Objective**: Refactor `RuleBasedScorer` to compute multi-tiered semantic alignment scores across Ritual, Deity, Tradition, and Category.
- **Dependencies**: Phase 4 Candidate Generator updates.
- **Estimated Complexity**: Medium (2–3 days).
- **Risks**: Weight imbalances causing popularity bias.
- **Expected Benefit**: Highly personalized scoring reflecting user spiritual preferences.

### Phase 6: User Behavior & Devotional Preference Modeling
- **Objective**: Update real-time feedback handler in `RecommenderService.submit_feedback()` to dynamically adjust user deity & ritual interest profiles upon completion/like events.
- **Dependencies**: Phase 5 Scorer updates.
- **Estimated Complexity**: Medium (2–3 days).
- **Risks**: Rapid interest drift if feedback weights are set too high.
- **Expected Benefit**: Real-time adaptive feed personalization within the same viewing session.

### Phase 7: Offline Retrieval & Recommendation Evaluation (NDCG@K)
- **Objective**: Implement NDCG@K, Recall@K, and Precision@K evaluation scripts comparing recommended feeds against user persona ground-truth preferences.
- **Dependencies**: Phase 5 Scorer & Phase 6 User Modeling.
- **Estimated Complexity**: Medium (2 days).
- **Risks**: Non-deterministic evaluation runs if test seeds fluctuate.
- **Expected Benefit**: Quantitative validation of recommendation quality prior to production rollout.

### Phase 8: Production Rollout, Monitoring & PMCLP Integration
- **Objective**: Deploy updated recommendation pipeline into staging/production and connect quality monitoring metrics to PMCLP dashboards.
- **Dependencies**: Phases 1–7 complete.
- **Estimated Complexity**: Low (1–2 days).
- **Risks**: Minor latency regression during high-concurrency requests.
- **Expected Benefit**: Full production observability, feedback loops, and continuous quality tracking.
