"""
Task 4 – FAISS Index Builder
Builds binary FAISS L2-normalized IndexFlatIP vector indexes from dense numpy matrices.
"""

import os
import faiss
import numpy as np


class FAISSIndexBuilder:
    """Builds and serializes FAISS vector indexes."""

    def build_flat_ip_index(self, embeddings_matrix: np.ndarray) -> faiss.IndexFlatIP:
        """Builds an L2-normalized IndexFlatIP (cosine similarity) FAISS index."""
        dimension = embeddings_matrix.shape[1]
        index = faiss.IndexFlatIP(dimension)

        # Normalize L2
        vectors = embeddings_matrix.copy().astype("float32")
        faiss.normalize_L2(vectors)

        index.add(vectors)
        print(f"[CSIEI-FAISSBuilder] Built IndexFlatIP index with {index.ntotal} vectors of dim {dimension}.")
        return index

    def save_index(self, index: faiss.IndexFlatIP, output_path: str):
        """Serializes FAISS index to disk."""
        out_str = str(output_path)
        os.makedirs(os.path.dirname(out_str), exist_ok=True)
        faiss.write_index(index, out_str)
        print(f"[CSIEI-FAISSBuilder] Saved FAISS binary index to '{out_str}'.")
