# ACPCS Duplicate Detection & Idempotency Strategy

## Executive Summary
This document specifies the deterministic duplicate detection and idempotency mechanism implemented in the Automated Content Publishing & Catalog Synchronization (ACPCS) layer.

---

## Technical Strategy

1. **SHA-256 Byte Hashing**:
   - Every raw video file processed by Content Intelligence is hashed using SHA-256 (`ContentHasher.compute_file_hash`).
   - The SHA-256 hash is content-based and independent of file path or upload filename.

2. **Idempotency Lookup Flow**:
   ```
   Incoming Video File
          │
          ▼
   Compute SHA-256 Hash
          │
          ▼
   Check `ContentCatalogStore` by Hash
          ├───────────────────────────────┐
          │ (Hash Match Found)            │ (No Match)
          ▼                               ▼
   Existing Record Found             New Catalog Entry
          │                               │
   Compare Version Hash             Publication Action = CREATE
   (Metadata & Embeddings)
          ├───────────────┐
          │ (Identical)   │ (Modified)
          ▼               ▼
     Action = SKIP    Action = UPDATE
     (Log "No         (Increment Version
      Changes")        & Replace FAISS Vector)
   ```

3. **Concurrency & Race Condition Handling**:
   - `ContentCatalogStore` maintains an in-memory hash index (`_hash_to_video_id`).
   - Simultaneous ingestion requests for identical video files resolve to the exact same authoritative record, preventing duplicate vector insertions or catalog bloat.
