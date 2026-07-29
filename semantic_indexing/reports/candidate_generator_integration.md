# CSIEI Task 5: Candidate Generator Integration Specification

## Overview

The `CandidateGenerator` has been refactored to consume CMREE Canonical Metadata vectors and expanded with 2 dedicated semantic retrieval channels:
1. **`retrieve_by_deity(preferred_deities)`**
2. **`retrieve_by_ritual_family(preferred_ritual_families)`**

---

## Retrieval Channels Matrix

| Channel | Method Name | Selection Logic |
|:---|:---|:---|
| **FAISS Semantic Search** | `retrieve_similar_to_watch_history()` | Queries vector index using canonical embeddings of seed watch history |
| **Same Primary Deity** | `retrieve_by_deity()` | Fetches candidates matching user's preferred deity profiles (`Lord Shiva`, `Shirdi Sai Baba`, `Lord Ganesha`) |
| **Same Ritual Family** | `retrieve_by_ritual_family()` | Fetches candidates matching user's preferred ritual families (`Abhishekam`, `Aarti`, `Archana`) |
| **Category Pool** | `retrieve_by_categories()` | Fetches candidates matching user's category interests |
| **Trending Pool** | `retrieve_trending()` | Fetches top high-engagement videos across catalog |
| **Creator Affinity** | `retrieve_by_creator_affinity()` | Fetches top videos from user's favorite creators |
| **Exploration Pool** | `retrieve_exploration()` | Uniform random sampling for discovery |
| **Freshness Pool** | `retrieve_fresh()` | Most recently uploaded videos |
