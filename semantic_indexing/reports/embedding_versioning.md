# CSIEI Task 3: Embedding Versioning & Metadata Specification

## Overview

The **Embedding Versioning & Metadata Tracking System** guarantees complete auditability and version control for vector embeddings stored on disk. This enables smooth upgrades when switching between model providers (`minilm` -> `bge` -> `e5`) without breaking index consistency.

---

## Manifest Schema (`embedding_manifest.json`)

```json
{
  "metadata_version": "2.0-cmree-enterprise",
  "embedding_version": "v2.0-canonical-semantic",
  "embedding_model": "all-MiniLM-L6-v2",
  "embedding_dimension": 384,
  "total_vectors": 7010,
  "timestamp": "2026-07-27T16:10:00Z",
  "status": "production_ready"
}
```

---

## Disk Persistence Files

- **`models/video.index`**: FAISS binary L2-normalized IndexFlatIP index.
- **`datasets/embeddings/video_embeddings.npy`**: Float32 matrix (N x 384).
- **`datasets/embeddings/video_ids.npy`**: String array of video IDs.
- **`datasets/embeddings/embedding_manifest.json`**: Manifest tracking schema and model versions.
