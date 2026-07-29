# RAIA Task 1: Recommendation Platform Repository Inventory

## Overview

This inventory presents a complete audit of the Recommendation Platform codebase, detailing all components across candidate generation, vector search, ranking, intelligence extraction, metadata storage, API routes, user profiling, and evaluation modules.

---

## Component Inventory Matrix

| Component Area | Key File(s) | Primary Responsibility | Input Data Structure | Output Data Structure | Dependencies |
|:---|:---|:---|:---|:---|:---|
| **Recommendation Service** | [`src/recommender/service.py`](file:///Users/ujjwalhkumar/Documents/hello_flutter/recommendation-platform/src/recommender/service.py) | Main orchestration service for personalized feed generation, feedback handling, and user profile management | `user_query` (user_id / persona string), `limit` | Ranked feed JSON with scores & explanations | `CandidateGenerator`, `RuleBasedScorer`, `DiversityFilter`, `RecommendationExplainer` |
| **Candidate Generation** | [`src/candidate_generation/candidate_generator.py`](file:///Users/ujjwalhkumar/Documents/hello_flutter/recommendation-platform/src/candidate_generation/candidate_generator.py) | Multi-channel candidate retrieval (Trending, Category, Similar Watch History, Collaborative Filtering, Creator Affinity, Exploration, Fresh) | User interest profile dict, watch history list | Merged list of candidate video dicts | `FaissSearchService`, `enriched_videos.json` |
| **Vector Search / Indexing** | [`src/indexing/faiss_service.py`](file:///Users/ujjwalhkumar/Documents/hello_flutter/recommendation-platform/src/indexing/faiss_service.py)<br>[`src/search/faiss_index.py`](file:///Users/ujjwalhkumar/Documents/hello_flutter/recommendation-platform/src/search/faiss_index.py) | FAISS L2-normalized inner product (cosine similarity) vector index management, embedding storage, and similarity querying | Video ID or 384-dim numpy query vector | List of `{video_id, score}` dicts | `faiss`, `video.index`, `video_embeddings.npy`, `video_ids.npy` |
| **Ranking & Scoring** | [`src/ranking/scorer.py`](file:///Users/ujjwalhkumar/Documents/hello_flutter/recommendation-platform/src/ranking/scorer.py) | Multi-signal weighted scoring engine (`InterestSignal`, `CreatorAffinitySignal`, `PopularitySignal`, `SimilaritySignal`, `CollaborativeFilteringSignal`, `FreshnessSignal`) | Candidate list, interest profile, creator affinities | Score-annotated ranked candidate list | `math`, `random` |
| **Diversity & Re-ranking** | [`src/recommender/diversity.py`](file:///Users/ujjwalhkumar/Documents/hello_flutter/recommendation-platform/src/recommender/diversity.py) | Re-ranking filter enforcing category diversity, max consecutive category limits, and freshness insertion | Ranked candidate list | Diversity-filtered candidate list | Python standard library |
| **Recommendation Explainer** | [`src/recommender/explainer.py`](file:///Users/ujjwalhkumar/Documents/hello_flutter/recommendation-platform/src/recommender/explainer.py) | Generates human-readable natural language explanations for recommended videos | Candidate dict, user interest profile | Human-readable explanation string | Python standard library |
| **Content Intelligence Pipeline** | [`src/content_intelligence/pipeline.py`](file:///Users/ujjwalhkumar/Documents/hello_flutter/recommendation-platform/src/content_intelligence/pipeline.py) | End-to-end multimodal perception extraction (Vision, Speech, OCR, Action, Audio) + CMREE Reasoning Engine integration | Video file path, video ID | Enriched intelligence report record | `VideoIntelligenceEngine`, `SentenceTransformer`, `CMREEPipeline`, `IntelligenceDatabase` |
| **CMREE Reasoning Engine** | [`reasoning_engine/pipeline.py`](file:///Users/ujjwalhkumar/Documents/hello_flutter/recommendation-platform/reasoning_engine/pipeline.py) | Deterministic, rule-based semantic reasoning & metadata enrichment (Observation Schema, Entity Resolution, Rule Engine, KB, Confidence Engine) | VLM observation dict | Canonical Metadata document & reasoning trace | `ObservationValidator`, `EntityResolver`, `RuleEngine`, `MetadataEnricher`, `CMREEConfidenceEngine` |
| **Metadata Storage** | [`src/content_intelligence/database.py`](file:///Users/ujjwalhkumar/Documents/hello_flutter/recommendation-platform/src/content_intelligence/database.py) | Persistent JSON store for processed video intelligence records | Video ID, record dict | Disk persistence to `intelligence_metadata.json` | `json`, `os` |
| **User Personas & Profiles** | [`src/users/personas.py`](file:///Users/ujjwalhkumar/Documents/hello_flutter/recommendation-platform/src/users/personas.py)<br>[`src/users/generator.py`](file:///Users/ujjwalhkumar/Documents/hello_flutter/recommendation-platform/src/users/generator.py) | User persona definitions, initial interest profile generation, and synthetic watch history generation | Persona templates | `users.json`, `interest_profiles.json`, `watch_history.json` | `random`, `json` |
| **Backend REST Server** | [`backend/app.py`](file:///Users/ujjwalhkumar/Documents/hello_flutter/recommendation-platform/backend/app.py) | FastAPI web server serving recommendation feeds, video processing, FAISS search, CMREE routes, and PMCLP monitoring APIs | HTTP REST Requests (GET/POST) | JSON HTTP Responses | `RecommenderService`, `FaissSearchService`, `ContentIntelligencePipeline`, `CMREEPipeline` |
| **Evaluation Framework** | [`src/evaluation/framework.py`](file:///Users/ujjwalhkumar/Documents/hello_flutter/recommendation-platform/src/evaluation/framework.py) | Offline evaluation harness for measuring candidate diversity, score distribution, and pipeline latency | Recommender service instance, test user set | Evaluation metrics report dict | `RecommenderService` |
| **Monitoring & Analytics** | [`src/monitoring/observability.py`](file:///Users/ujjwalhkumar/Documents/hello_flutter/recommendation-platform/src/monitoring/observability.py) | Logging and metrics collector for latency tracking, throughput, and error rates | Performance events | Metrics JSON reports | `time`, `json` |

---

## Data Model & Catalog Summary

1. **`datasets/processed/enriched_videos.json`**: Main video metadata catalog (7,010 items) containing `video_id`, `caption`, `category`, `hashtags`, `views`, `likes`, `engagement_score`, `created_time`, `duration`, `video_url`.
2. **`datasets/processed/intelligence_metadata.json`**: Multimodal perception & CMREE canonical metadata store (46 enriched items) containing `canonical_metadata`, `primary_ritual`, `ritual_family`, `primary_deity`, `temple`, `tradition`, `offerings`, `cmree_confidence`, `cmree_reasoning_trace`.
3. **`datasets/embeddings/video_embeddings.npy`**: 384-dimensional dense vector embeddings matrix (7,010 x 384).
4. **`models/video.index`**: Binary FAISS `IndexFlatIP` vector index.
5. **`datasets/processed/users.json`**: User profiles mapped to demographic personas.
6. **`datasets/processed/interest_profiles.json`**: Category interest weights per user.
7. **`datasets/processed/watch_history.json`**: Chronological video engagement events.
