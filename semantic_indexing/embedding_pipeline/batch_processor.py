"""
Task 3 – Batch Processor Module
Processes full video catalogs in configurable batch sizes and outputs numpy matrices & ID mappings.
"""

import os
import json
from typing import List, Dict, Any, Tuple
import numpy as np
from src.utils.paths import get_path
from semantic_indexing.embedding_pipeline.generator import CanonicalEmbeddingGenerator
from semantic_indexing.embedding_pipeline.versioning import EmbeddingMetadataTracker


class BatchEmbeddingProcessor:
    """Processes large video catalogs into dense canonical embedding matrices."""

    def __init__(self, generator: CanonicalEmbeddingGenerator = None):
        self.generator = generator or CanonicalEmbeddingGenerator()

    def process_catalog(self, catalog: List[Dict[str, Any]], batch_size: int = 64) -> Tuple[np.ndarray, np.ndarray, Dict[str, Any]]:
        """
        Processes a full catalog list of video dicts.
        Returns:
            (embeddings_matrix, video_ids_array, version_manifest)
        """
        total = len(catalog)
        print(f"[CSIEI-BatchProcessor] Processing {total} videos using model '{self.generator.provider.model_name()}'...")

        video_ids = []
        all_vectors = []

        for i in range(0, total, batch_size):
            batch = catalog[i:i + batch_size]
            batch_ids = [str(item["video_id"]) for item in batch]
            
            res = self.generator.generate_batch_embeddings(batch)
            vecs = res["embeddings"]

            video_ids.extend(batch_ids)
            all_vectors.append(vecs)

        embeddings_matrix = np.vstack(all_vectors).astype("float32")
        video_ids_array = np.array(video_ids)

        manifest = EmbeddingMetadataTracker.create_embedding_manifest(
            model_name=self.generator.provider.model_name(),
            dimension=self.generator.provider.embedding_dimension(),
            total_vectors=len(video_ids)
        )

        return embeddings_matrix, video_ids_array, manifest
