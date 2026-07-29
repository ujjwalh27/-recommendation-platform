# RAIA Task 5: Vector Search & FAISS Indexing Audit

## Overview

This document audits the vector search architecture, FAISS index configuration, indexing lifecycle, update strategies, similarity metrics, and metadata filtering capabilities.

---

## Vector Search Technical Specifications

| Parameter | Current Configuration | Architectural Assessment |
|:---|:---|:---|
| **FAISS Index Type** | `IndexFlatIP` (Flat Inner Product) | **Optimal for Exact Cosine Similarity**: Given $L_2$-normalized vectors, Inner Product is mathematically identical to Cosine Similarity ($\mathbf{a} \cdot \mathbf{b} = \cos \theta$). Exact $O(N)$ search is extremely fast for catalog sizes $< 100,000$ videos ($< 2\text{ ms}$ per query). |
| **Vector Dimension** | 384 dimensions | Matches `SentenceTransformer("all-MiniLM-L6-v2")` output dimension. |
| **Normalization** | `faiss.normalize_L2(embedding)` | Enforced on index build, dynamic additions, and query vectors. |
| **Index Persistence Location** | `models/video.index` | Binary FAISS index format written directly to disk via `faiss.write_index()`. |
| **Embedding Matrix File** | `datasets/embeddings/video_embeddings.npy` | Raw float32 numpy array (7,010 x 384) matching index order 1-to-1. |
| **ID Mapping File** | `datasets/embeddings/video_ids.npy` | String array of video IDs matching index row offset 1-to-1. |
| **Similarity Metric** | Cosine Similarity ($0.0 \le S \le 1.0$) | Scores strictly bounded between 0.0 and 1.0. |

---

## Index Lifecycle & Maintenance Workflows

### 1. Initialization Workflow
When `FaissSearchService()` is instantiated:
1. Loads binary index `models/video.index`.
2. Loads string ID array `datasets/embeddings/video_ids.npy`.
3. Loads matrix array `datasets/embeddings/video_embeddings.npy`.
4. Builds in-memory lookup dictionary `video_id_to_index = {vid: i for i, vid in enumerate(video_ids)}`.

### 2. Dynamic Incremental Addition
When `FaissSearchService.add_video(video_id, embedding)` is invoked:
1. Normalizes 384-dim input vector with `faiss.normalize_L2`.
2. Adds vector to in-memory `self.index`.
3. Rewrites binary index `models/video.index`.
4. Appends `video_id` to `video_ids.npy` on disk.
5. Appends embedding row to `video_embeddings.npy` on disk.
6. Updates in-memory dictionary `self.video_id_to_index[video_id] = new_idx`.

### 3. Full Rebuild Strategy
Currently, full rebuilds are executed manually via offline scripts. To support CMREE canonical embeddings, a full re-indexing pipeline MUST be triggered whenever the CMREE knowledge base or embedding generator is updated.

---

## Metadata Attachment & Filtering Assessment

- **Current Capability**: FAISS indexes dense vectors only; video metadata is attached post-retrieval via `CandidateGenerator.video_lookup` dictionary.
- **Can it consume CMREE Canonical Metadata directly?**: **YES**.
  - No changes are required to the underlying FAISS C++ binary library or `IndexFlatIP` schema.
  - The vector embeddings generated from CMREE Canonical Metadata are simply indexed into `video.index`.
  - When similarity search returns top $K$ candidate `video_id`s, `CandidateGenerator` retrieves the enriched CMREE metadata document (`primary_ritual`, `ritual_family`, `primary_deity`, `temple`) directly from the database.
