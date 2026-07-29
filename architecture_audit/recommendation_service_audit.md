# RAIA Task 6: Recommendation Service & Business Logic Audit

## Overview

This document audits the core `RecommenderService`, Candidate Generation channels, Ranking Signals, Diversity Filters, Cold-Start logic, and Feedback handlers. It highlights logic that can remain unchanged versus logic that requires CMREE enhancement.

---

## 1. Candidate Retrieval Channels Audit

| Channel Name | Method in `CandidateGenerator` | Strategy / Logic | Impact of CMREE Integration | Recommendation |
|:---|:---|:---|:---|:---|
| **Trending Pool** | `retrieve_trending(limit=100)` | Sorts catalog by `engagement_score` & `views` descending | Needs updating to prioritize high-confidence CMREE canonical videos | **REFACTOR**: Filter by `cmree_confidence >= 0.60` |
| **Category Pool** | `retrieve_by_categories(profile)` | Matches user category interest scores to video categories | Currently matches generic categories. Should match CMREE `primary_category` & `ritual_family` | **REFACTOR**: Map user interest directly to CMREE categories & ritual families |
| **FAISS Similar Watch History** | `retrieve_similar_to_watch_history()` | Queries FAISS using recent high-engagement seed video embeddings | Will automatically benefit from CMREE canonical embeddings | **KEEP & UPGRADE EMBEDDINGS**: Retain retrieval logic; upgrade vectors to CMREE canonical embeddings |
| **Collaborative Filtering** | `retrieve_collaborative_filtering()` | User-based cosine similarity on category interest vectors | Upgrade interest vectors to include deity & ritual preferences | **REFACTOR**: Expand user interest vector to include ritual family weights |
| **Creator Affinity** | `retrieve_by_creator_affinity()` | Retrieves top videos from creators user frequently engages with | Unaffected | **KEEP**: Retain logic as-is |
| **Exploration Pool** | `retrieve_exploration(limit=30)` | Uniform random sampling across catalog | Unaffected | **KEEP**: Retain logic as-is |
| **Freshness Pool** | `retrieve_fresh(limit=150)` | Sorts by `created_time` descending | Unaffected | **KEEP**: Retain logic as-is |

---

## 2. Ranking Signals Audit

The `RuleBasedScorer` calculates a weighted composite score across 6 signals:

$$\text{Final Score} = w_1 S_{\text{interest}} + w_2 S_{\text{creator}} + w_3 S_{\text{popularity}} + w_4 S_{\text{similarity}} + w_5 S_{\text{CF}} + w_6 S_{\text{freshness}}$$

| Ranking Signal Class | Current Weight ($w_i$) | Score Formula / Input | Post-CMREE Strategy |
|:---|:---:|:---|:---|
| `InterestSignal` | **0.35** | `interests.get(category, 0.0) / 100.0` | **REFACTOR**: Score category match + ritual family match + deity match |
| `CreatorAffinitySignal` | **0.20** | `creator_affinities.get(creator, 0.0) / 100.0` | **KEEP**: Maintain creator affinity weight |
| `PopularitySignal` | **0.15** | `0.7 * er_score + 0.3 * views_score` | **KEEP**: Maintain engagement & view log-scale popularity |
| `SimilaritySignal` | **0.15** | `candidate.get("similarity_score", 0.0)` | **KEEP & ENHANCE**: Driven by CMREE FAISS vector similarity |
| `CollaborativeFilteringSignal` | **0.10** | `candidate.get("cf_score", 0.0)` | **KEEP**: Maintain collaborative filtering weight |
| `FreshnessSignal` | **0.05** | Exponential age decay ($\lambda = 0.0231$) | **KEEP**: Maintain freshness decay formula |

---

## 3. Cold-Start Handling & Fallbacks Audit

- **Cold-Start Videos** (Fresh uploads with 0 views / 0 likes):
  - Handled in `PopularitySignal`: Assigns a high baseline score ($0.80$) if video age $< 30$ days.
  - Handled in `CandidateGenerator`: `retrieve_fresh()` guarantees 150 recent uploads enter the candidate pool.
  - **CMREE Enhancement**: Add `cmree_confidence >= 0.85` bonus to cold-start videos to prevent unvalidated noisy videos from surfacing.

- **Cold-Start Users** (New users with empty watch history & default interest profile):
  - Fallback logic in `CandidateGenerator`: Merges `Trending Pool` + `Exploration Pool` + `Freshness Pool`.
  - **CMREE Enhancement**: Persona templates (e.g. *Shiva Devotee*, *Sai Baba Follower*) can seed initial deity/ritual preferences immediately.

---

## 4. Diversity Filter Audit (`DiversityFilter`)

- Enforces two business rules:
  1. `max_consecutive_category = 1`: Prevents 2 consecutive recommendations from the same category.
  2. `max_category_ratio = 0.30`: Limits any single category to $\le 30\%$ of the feed.
- **CMREE Enhancement**: Extend consecutive check to `primary_deity` and `primary_ritual` so users do not see 3 identical `Jalabhishekam` videos in a row.
