# RAIA Task 2: End-to-End Recommendation Request Lifecycle

## Overview

This document details the exact runtime lifecycle of a recommendation request through the system, mapping inputs, outputs, source files, data structures, and component dependencies at every stage.

---

## Request Execution Flow

```
[Client Application]
         │
         │  GET /api/feed?user_id=usr_102&limit=10
         ▼
 ┌────────────────────────────────────────────────────────┐
 │ Stage 1: FastAPI Request Routing                       │
 │ Source: backend/app.py                                 │
 └───────────────────────┬────────────────────────────────┘
                         │
                         ▼
 ┌────────────────────────────────────────────────────────┐
 │ Stage 2: User Resolution & Profile Lookup              │
 │ Source: src/recommender/service.py                     │
 └───────────────────────┬────────────────────────────────┘
                         │
                         ▼
 ┌────────────────────────────────────────────────────────┐
 │ Stage 3: Multi-Channel Candidate Retrieval             │
 │ Source: src/candidate_generation/candidate_generator.py│
 └───────────────────────┬────────────────────────────────┘
                         │
                         ▼
 ┌────────────────────────────────────────────────────────┐
 │ Stage 4: Multi-Signal Scoring & Ranking                │
 │ Source: src/ranking/scorer.py                          │
 └───────────────────────┬────────────────────────────────┘
                         │
                         ▼
 ┌────────────────────────────────────────────────────────┐
 │ Stage 5: Diversity Re-Ranking & Filtering              │
 │ Source: src/recommender/diversity.py                   │
 └───────────────────────┬────────────────────────────────┘
                         │
                         ▼
 ┌────────────────────────────────────────────────────────┐
 │ Stage 6: Explanation Generation & Payload Formatting   │
 │ Source: src/recommender/explainer.py & service.py      │
 └───────────────────────┬────────────────────────────────┘
                         │
                         ▼
                 [JSON HTTP Response]
```

---

## Detailed Stage Analysis

### Stage 1: FastAPI Request Routing
- **Source File**: [`backend/app.py`](file:///Users/ujjwalhkumar/Documents/hello_flutter/recommendation-platform/backend/app.py) (Lines 75–95)
- **Input**: Query parameters `user_id` (str, default `"usr_101"`), `limit` (int, default `10`).
- **Output**: JSON payload returned by `RecommenderService.get_recommendations()`.
- **Dependencies**: `RecommenderService` singleton.
- **Data Structure**: `GET /api/feed?user_id=usr_102&limit=10`.

### Stage 2: User Resolution & Profile Lookup
- **Source File**: [`src/recommender/service.py`](file:///Users/ujjwalhkumar/Documents/hello_flutter/recommendation-platform/src/recommender/service.py) (Lines 65–100)
- **Input**: `user_query` string (e.g. `"usr_102"` or `"Devotee Persona"`).
- **Output**: `user_profile` dict, `interest_profile` dict, `watch_history` list, `creator_affinities` dict.
- **Dependencies**: `users.json`, `interest_profiles.json`, `watch_history.json`.
- **Data Structures**:
  - `interest_profile`: `{"user_id": "usr_102", "persona": "Devotee Persona", "interests": {"Religion & Spirituality": 85.0, "Temple Ritual": 90.0}}`.
  - `creator_affinities`: `{"ai_intelligence": 45.0, "temple_trust": 25.0}`.

### Stage 3: Multi-Channel Candidate Retrieval
- **Source File**: [`src/candidate_generation/candidate_generator.py`](file:///Users/ujjwalhkumar/Documents/hello_flutter/recommendation-platform/src/candidate_generation/candidate_generator.py) (Lines 196–279)
- **Input**: `interest_profile`, `watch_history`, `creator_affinities`.
- **Output**: Candidate list of video dicts containing retrieval source tags and similarity scores.
- **Dependencies**: `FaissSearchService`, `enriched_videos.json`.
- **Retrieval Channels Executed**:
  1. **Trending Pool**: Top 100 videos by engagement score.
  2. **Category Pool**: Top 15 videos per positive interest category.
  3. **FAISS Similar Watch History**: Top 10 similar videos per recent positive watch event.
  4. **Collaborative Filtering**: Top 20 videos watched by cosine-similar users.
  5. **Creator Affinity**: Top 10 videos per high-affinity creator.
  6. **Exploration Pool**: 30 randomized videos across the catalog.
  7. **Freshness Pool**: 150 most recently uploaded videos.
- **Deduplication**: Candidates merged by `video_id`, accumulating all `retrieval_sources`.

### Stage 4: Multi-Signal Scoring & Ranking
- **Source File**: [`src/ranking/scorer.py`](file:///Users/ujjwalhkumar/Documents/hello_flutter/recommendation-platform/src/ranking/scorer.py) (Lines 100–200)
- **Input**: Merged candidate list, `interest_profile`, `creator_affinities`.
- **Output**: Score-sorted candidate list with `final_score` and `score_breakdown` attached.
- **Dependencies**: `InterestSignal`, `CreatorAffinitySignal`, `PopularitySignal`, `SimilaritySignal`, `CollaborativeFilteringSignal`, `FreshnessSignal`.
- **Weighting Formula**:
  $$\text{Final Score} = 0.35 \cdot S_{\text{interest}} + 0.20 \cdot S_{\text{creator}} + 0.15 \cdot S_{\text{popularity}} + 0.15 \cdot S_{\text{similarity}} + 0.10 \cdot S_{\text{CF}} + 0.05 \cdot S_{\text{freshness}}$$

### Stage 5: Diversity Re-Ranking & Filtering
- **Source File**: [`src/recommender/diversity.py`](file:///Users/ujjwalhkumar/Documents/hello_flutter/recommendation-platform/src/recommender/diversity.py) (Lines 1–80)
- **Input**: Score-ranked candidate list, `limit` (default `10`).
- **Output**: Diversity-filtered candidate list (max 1 consecutive video of same category, max 30% ratio per category).
- **Dependencies**: Python standard library.

### Stage 6: Explanation Generation & Payload Formatting
- **Source File**: [`src/recommender/explainer.py`](file:///Users/ujjwalhkumar/Documents/hello_flutter/recommendation-platform/src/recommender/explainer.py) & `service.py` (Lines 120–150)
- **Input**: Diverse candidate list, user interaction state mapping (`is_liked`, `is_saved`, `is_commented`).
- **Output**: Final recommendation feed payload array.
- **JSON Output Format**:
```json
[
  {
    "video_id": "video_ci_1784804233",
    "title": "Devotional Worship in Temple",
    "duration": 15.0,
    "category": "Religion & Spirituality",
    "thumbnail_url": "http://127.0.0.1:8000/thumbnails/video_ci_1784804233.jpg",
    "video_url": "http://127.0.0.1:8000/videos/video_ci_1784804233.mp4",
    "score": 0.845,
    "explanation": "Recommended because it aligns with your interest in Religion & Spirituality and features high community engagement.",
    "score_breakdown": {
      "interest_score": 0.85,
      "creator_score": 0.45,
      "popularity_score": 0.80,
      "similarity_score": 0.78,
      "cf_score": 0.0,
      "freshness_score": 0.82
    },
    "retrieval_sources": ["category_retrieval", "faiss_similarity", "fresh_retrieval"],
    "is_liked": false,
    "is_saved": false,
    "is_commented": false
  }
]
```
