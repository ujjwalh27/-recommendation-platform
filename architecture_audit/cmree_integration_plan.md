# RAIA Task 7: CMREE Integration Plan & Interface Specs

## Overview

This document specifies the target architecture, insertion points, and interface modifications required to fully integrate CMREE Canonical Metadata into the Recommendation Engine.

---

## Target Architecture Blueprint

```
                     ┌──────────────────────────────────────────┐
                     │          Raw Video Input (.mp4)          │
                     └────────────────────┬─────────────────────┘
                                          │
                                          ▼
                     ┌──────────────────────────────────────────┐
                     │   Content Intelligence Pipeline (CIP)    │
                     │  (src/content_intelligence/pipeline.py)   │
                     └────────────────────┬─────────────────────┘
                                          │
                                          ▼
                     ┌──────────────────────────────────────────┐
                     │   CMREE Reasoning & Enrichment Engine    │
                     │    (reasoning_engine/pipeline.py)        │
                     └────────────────────┬─────────────────────┘
                                          │
                                          ▼
                     ┌──────────────────────────────────────────┐
                     │         Canonical Metadata JSON          │
                     │  [Ritual, Deity, Family, Temple, Conf]   │
                     └──────────┬────────────────────┬──────────┘
                                │                    │
            Primary Metadata    │                    │ Canonical Text
                                ▼                    ▼
 ┌──────────────────────────────────────────┐ ┌──────────────────────────────────────────┐
 │      Intelligence Database & Catalog     │ │       Canonical Embedding Generator      │
 │  (datasets/processed/intelligence_db)    │ │  SentenceTransformer("all-MiniLM-L6-v2") │
 └──────────────────────┬───────────────────┘ └────────────────────┬─────────────────────┘
                        │                                          │
                        │                                          ▼
                        │                     ┌──────────────────────────────────────────┐
                        │                     │         FAISS Vector Index Service       │
                        │                     │       (src/indexing/faiss_service.py)    │
                        │                     └────────────────────┬─────────────────────┘
                        │                                          │
                        ▼                                          ▼
 ┌───────────────────────────────────────────────────────────────────────────────────────┐
 │                            Candidate Generation Engine                                │
 │                  (src/candidate_generation/candidate_generator.py)                    │
 │    [Channels: Trending, Category/Ritual, FAISS Similar, CF, Creator, Deity, Fresh]    │
 └──────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
                                            ▼
 ┌───────────────────────────────────────────────────────────────────────────────────────┐
 │                              Rule-Based Ranking Scorer                                │
 │                               (src/ranking/scorer.py)                                 │
 │     [Signals: Ritual/Deity Interest, Creator, Popularity, Vector Similarity, CF]    │
 └──────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
                                            ▼
 ┌───────────────────────────────────────────────────────────────────────────────────────┐
 │                       Diversity Filter & Recommendation Explainer                     │
 │                     (src/recommender/diversity.py & explainer.py)                     │
 └──────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
                                            ▼
 ┌───────────────────────────────────────────────────────────────────────────────────────┐
 │                              FastAPI Production Feed API                              │
 │                                   (backend/app.py)                                    │
 └───────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Interface Change Specifications

### 1. `ContentIntelligencePipeline` Interface Modification
- **Location**: [`src/content_intelligence/pipeline.py`](file:///Users/ujjwalhkumar/Documents/hello_flutter/recommendation-platform/src/content_intelligence/pipeline.py)
- **Change**: Invoke `cmree_pipeline.process_observation(raw_obs)` during `analyze_video()`.
- **Output Record Contract**:
  - Must include `canonical_metadata` object.
  - Top-level keys: `primary_ritual`, `ritual_family`, `primary_deity`, `temple`, `tradition`, `offerings`, `cmree_confidence`, `cmree_reasoning_trace`.

### 2. `FaissSearchService` & Embedding Generator Modification
- **Location**: [`src/indexing/faiss_service.py`](file:///Users/ujjwalhkumar/Documents/hello_flutter/recommendation-platform/src/indexing/faiss_service.py) & `scripts/generate_embeddings.py`
- **Change**: Construct embedding text strictly from CMREE canonical metadata fields:
  ```python
  text = f"Category: {doc['primary_category']} | Ritual: {doc['primary_ritual']} | Family: {doc['ritual_family']} | Deity: {doc['primary_deity']} | Temple: {doc.get('temple', '')} | Keywords: {' '.join(doc['keywords'])}"
  ```

### 3. `CandidateGenerator` Interface Modification
- **Location**: [`src/candidate_generation/candidate_generator.py`](file:///Users/ujjwalhkumar/Documents/hello_flutter/recommendation-platform/src/candidate_generation/candidate_generator.py)
- **Change**: Add 2 new candidate retrieval channels:
  1. `retrieve_by_deity_affinity(user_deity_preferences, limit=15)`
  2. `retrieve_by_ritual_family(user_ritual_preferences, limit=15)`
- **Quality Gate**: Filter out candidates with `cmree_confidence < 0.60`.

### 4. `RuleBasedScorer` Interface Modification
- **Location**: [`src/ranking/scorer.py`](file:///Users/ujjwalhkumar/Documents/hello_flutter/recommendation-platform/src/ranking/scorer.py)
- **Change**: Refactor `InterestSignal` to compute semantic overlap across `primary_category`, `ritual_family`, and `primary_deity`.

### 5. `RecommendationExplainer` Interface Modification
- **Location**: [`src/recommender/explainer.py`](file:///Users/ujjwalhkumar/Documents/hello_flutter/recommendation-platform/src/recommender/explainer.py)
- **Change**: Generate explainable rationale using CMREE canonical fields (e.g., *"Recommended because it features the Kakad Aarti ritual dedicated to Shirdi Sai Baba with high community engagement"*).
