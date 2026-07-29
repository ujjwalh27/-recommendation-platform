"""
Task 4 – FAISS Integration Service
Connects the existing FaissSearchService to CMREE canonical embeddings.
"""

import os
import json
import numpy as np
from src.utils.paths import get_path
from src.indexing.faiss_service import FaissSearchService
from semantic_indexing.embedding_pipeline.batch_processor import BatchEmbeddingProcessor
from semantic_indexing.vector_index.index_builder import FAISSIndexBuilder


class CanonicalFaissIntegration:
    """Orchestrates FAISS index rebuilds and updates using CMREE Canonical Embeddings."""

    def __init__(self):
        self.processor = BatchEmbeddingProcessor()
        self.builder = FAISSIndexBuilder()

    def rebuild_faiss_index_from_catalog(self, catalog: list) -> dict:
        """Rebuilds the entire FAISS index and saves to models/video.index and datasets/embeddings/."""
        matrix, video_ids, manifest = self.processor.process_catalog(catalog)

        # 1. Save FAISS binary index
        index = self.builder.build_flat_ip_index(matrix)
        index_path = get_path("models/video.index")
        self.builder.save_index(index, index_path)

        # 2. Save video_embeddings.npy and video_ids.npy
        embeddings_path = get_path("datasets/embeddings/video_embeddings.npy")
        video_ids_path = get_path("datasets/embeddings/video_ids.npy")
        manifest_path = get_path("datasets/embeddings/embedding_manifest.json")

        os.makedirs(os.path.dirname(embeddings_path), exist_ok=True)
        np.save(embeddings_path, matrix)
        np.save(video_ids_path, video_ids)
        np.save(get_path("models/video_ids.npy"), video_ids)

        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=4)

        print(f"[CSIEI-FAISSIntegration] Rebuild complete. Index total: {index.ntotal}")

        return manifest
