# RAIA Task 1 & 2: Platform Dependency Graph & Component Interactions

## Overview

This document illustrates the end-to-end component dependencies and data flow across the Video Intelligence Platform, CMREE Semantic Engine, Vector Search / Indexing Layer, Candidate Generation, Ranking Scorer, and Recommendation APIs.

---

## Architectural Dependency Map

```
                     ┌──────────────────────────────────────────┐
                     │          Raw Video Input (.mp4)          │
                     └────────────────────┬─────────────────────┘
                                          │
                                          ▼
                     ┌──────────────────────────────────────────┐
                     │   Content Intelligence Pipeline (CIP)    │
                     │  (src/content_intelligence/pipeline.py)   │
                     └──────┬────────────────────────────┬──────┘
                            │                            │
             Multimodal Perception                       │
     (Vision + Speech + OCR + Actions)                   │
                            │                            │
                            ▼                            │
         ┌─────────────────────────────────────┐         │
         │ CMREE Semantic Reasoning Engine     │         │
         │ (reasoning_engine/pipeline.py)      │         │
         └──────────────────┬──────────────────┘         │
                            │                            │
                     Canonical Metadata                  │ 384-dim Text Vector
              (Ritual, Deity, Temple, Family)            │ (SentenceTransformer)
                            │                            │
                            ▼                            ▼
         ┌──────────────────────────────────────────────────────┐
         │              Intelligence Database                   │
         │    (datasets/processed/intelligence_metadata.json)   │
         └──────────────────┬───────────────────────────────────┘
                            │
                            ▼
         ┌──────────────────────────────────────────────────────┐
         │        FAISS Indexing & Vector Search Service        │
         │        (src/indexing/faiss_service.py)               │
         │        [models/video.index + embeddings.npy]         │
         └──────────────────┬───────────────────────────────────┘
                            │
                            ▼
         ┌──────────────────────────────────────────────────────┐
         │             Candidate Generation Engine              │
         │    (src/candidate_generation/candidate_generator.py) │
         │   [Trending, Category, FAISS Similar, CF, Creator]   │
         └──────────────────┬───────────────────────────────────┘
                            │
                            ▼
         ┌──────────────────────────────────────────────────────┐
         │             Rule-Based Ranking Scorer                │
         │             (src/ranking/scorer.py)                  │
         │     [Interest, Creator, Popularity, Freshness]       │
         └──────────────────┬───────────────────────────────────┘
                            │
                            ▼
         ┌──────────────────────────────────────────────────────┐
         │           Diversity Filter & Re-Ranker               │
         │           (src/recommender/diversity.py)             │
         └──────────────────┬───────────────────────────────────┘
                            │
                            ▼
         ┌──────────────────────────────────────────────────────┐
         │          Recommender Service Orchestrator            │
         │          (src/recommender/service.py)                │
         │          + Recommendation Explainer                  │
         └──────────────────┬───────────────────────────────────┘
                            │
                            ▼
         ┌──────────────────────────────────────────────────────┐
         │             FastAPI Backend Web Server               │
         │                  (backend/app.py)                    │
         │            GET /api/feed & POST /api/feedback        │
         └──────────────────────────────────────────────────────┘
```

---

## Detailed Data Dependency Matrix

| Downstream Consumer | Upstream Producer | Interchanged Data Structure | Purpose |
|:---|:---|:---|:---|
| `CMREEPipeline` | `ContentIntelligencePipeline` | Observation Dict (`scene`, `actions`, `objects`, `ocr_text`, `speech_text`, `language`, `confidence`) | Normalizes observations into canonical ritual & deity metadata |
| `IntelligenceDatabase` | `ContentIntelligencePipeline` & `CMREEPipeline` | Intelligence Record Dict (`canonical_metadata`, `primary_ritual`, `primary_deity`, `temple`, `embedding`) | Persists enriched video intelligence records to disk |
| `FaissSearchService` | `IntelligenceDatabase` & `SentenceTransformer` | `video_id` (str), `embedding` (384-dim float32 array) | Maintains inner product vector index for similarity search |
| `CandidateGenerator` | `FaissSearchService` & `enriched_videos.json` | Seed `video_id`, `top_k` limit | Retrieves candidate pools across 7 parallel retrieval channels |
| `RuleBasedScorer` | `CandidateGenerator` & `interest_profiles.json` | Unranked candidate list, user interest profile | Computes multi-signal weighted scores for candidate ranking |
| `DiversityFilter` | `RuleBasedScorer` | Ranked candidate list | Enforces category diversity and prevents consecutive duplicates |
| `RecommenderService` | `DiversityFilter` & `RecommendationExplainer` | Filtered candidate list, interaction state | Assembles production feed payload with scores, breakdowns & explanations |
| `FastAPI (app.py)` | `RecommenderService` | HTTP Request query parameters (`user_id`, `limit`) | Serves REST API responses to client applications |
