# RAIA Task 8: Refactoring Recommendations & Codebase Cleanup

## Overview

This document categorizes codebase components into **KEEP**, **REFACTOR**, **REPLACE**, and **REMOVE**, eliminating redundancy, obsolete pipelines, and dead code while consolidating the recommendation architecture around CMREE.

---

## Component Categorization & Decision Matrix

| Module / Component Path | Action | Rationale | Expected Technical Impact |
|:---|:---:|:---|:---|
| `reasoning_engine/` | **KEEP** | Standardized CMREE Reasoning & Enrichment Engine pipeline | Serves as authoritative canonical metadata & rule engine |
| `src/indexing/faiss_service.py` | **KEEP & REFACTOR** | Primary path-safe FAISS search service | Maintain as single vector search service; upgrade vectors to CMREE canonical embeddings |
| `src/candidate_generation/candidate_generator.py` | **REFACTOR** | Multi-channel retrieval engine | Add Deity & Ritual retrieval channels; integrate CMREE quality filter (`confidence >= 0.60`) |
| `src/ranking/scorer.py` | **REFACTOR** | Multi-signal ranking engine | Refactor `InterestSignal` to score CMREE ritual, deity, and sampradaya alignment |
| `src/recommender/diversity.py` | **REFACTOR** | Diversity filter | Extend consecutive category filter to prevent consecutive duplicate deities/rituals |
| `src/recommender/explainer.py` | **REFACTOR** | Recommendation explainer | Incorporate CMREE canonical ritual & deity names into natural language explanations |
| `src/semantic_knowledge/daiv_domain_reasoner.py`<br>`src/semantic_knowledge/hrce_classifier.py`<br>`src/semantic_knowledge/domain_rule_engine.py` | **REPLACE / REMOVE** | Legacy pre-CMREE rule reasoning prototypes | Obsolete; fully superseded by `reasoning_engine/` (CMREE pipeline & rules) |
| `src/search/similarity_search.py`<br>`src/search/faiss_index.py` | **REMOVE** | Legacy duplicate FAISS search module | Duplicate of `src/indexing/faiss_service.py`. Consolidate to `src/indexing/faiss_service.py` |
| `src/content_intelligence/fusion.py` | **REFACTOR** | Evidence fusion logic | Keep as perception evidence aggregator; delegate metadata normalization to CMREE |
| `scripts/run_lvv_sprint.py`<br>`scripts/compile_lvv_reports.py` | **KEEP** | Live VLM validation benchmarks | Keep as offline performance regression benchmarks |

---

## Detailed Refactoring Actions

### 1. Consolidate FAISS Search Infrastructure
- **Action**: Deprecate `src/search/faiss_index.py` and `src/search/similarity_search.py`.
- **Target**: Retain `src/indexing/faiss_service.py` as the sole vector search service across all APIs and scripts.

### 2. Deprecate Legacy Pre-CMREE Semantic Rule Engines
- **Action**: Archive or remove legacy prototypes in `src/semantic_knowledge/` (`daiv_domain_reasoner.py`, `hrce_classifier.py`, `ritual_decision_engine.py`).
- **Target**: Direct all semantic classification requests to `reasoning_engine/pipeline.py`.

### 3. Synchronize Catalog Metadata Stores
- **Action**: Currently, two JSON files store video metadata: `enriched_videos.json` (7,010 videos) and `intelligence_metadata.json` (46 videos).
- **Target**: Merge CMREE canonical fields into `enriched_videos.json` so candidate generator lookups always receive canonical metadata.
