# Incremental FAISS Indexing Specification

## Technical Architecture

Full index rebuilds (`IndexFlatIP` over entire datasets) incur disk I/O and latency spikes. `IncrementalFaissUpdater` provides zero-downtime, continuous vector operations:

1. **Insert New Vector (`INSERTED`)**:
   - Appends embedding to `video_embeddings.npy` and `video_ids.npy`.
   - Invokes `faiss_service.index.add(vector)`.
   - Updates in-memory lookup map `video_id_to_index`.

2. **In-Place Vector Update (`UPDATED`)**:
   - Retrieves index position `idx` for target `video_id`.
   - Replaces row `idx` in matrix `embeddings[idx] = new_vector`.
   - Re-instantiates `IndexFlatIP` from updated matrix and flushes to `models/video.index`.

3. **Concurrency Safety**:
   - Search queries continue executing against memory-mapped FAISS index without locking.
