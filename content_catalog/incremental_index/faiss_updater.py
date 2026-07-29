"""
Incremental FAISS Vector Updater
Supports inserting new vectors and replacing existing vectors in FAISS without full index rebuilds.
"""

import os
import faiss
import numpy as np
from typing import Optional, Dict, Any
from src.utils.paths import get_path
from src.indexing.faiss_service import FaissSearchService


class IncrementalFaissUpdater:
    """Manages incremental vector additions and replacements in the FAISS index and disk files."""

    def __init__(self, faiss_service: Optional[FaissSearchService] = None):
        self.faiss_service = faiss_service or FaissSearchService()

    def upsert_vector(self, video_id: str, embedding: np.ndarray) -> str:
        """
        Inserts a new vector or updates an existing vector in place.
        Returns 'INSERTED' or 'UPDATED'.
        """
        vid = str(video_id)
        embedding_vec = np.array(embedding, dtype="float32").reshape(1, -1)
        faiss.normalize_L2(embedding_vec)

        # Check if video_id already exists in index
        if vid in self.faiss_service.video_id_to_index:
            idx = self.faiss_service.video_id_to_index[vid]
            # Replace vector in matrix
            self.faiss_service.embeddings[idx] = embedding_vec[0]
            
            # Save updated arrays
            np.save(os.path.join(self.faiss_service.embeddings_dir, "video_embeddings.npy"), self.faiss_service.embeddings)
            
            # Reconstruct IndexFlatIP for exact consistency
            new_index = faiss.IndexFlatIP(embedding_vec.shape[1])
            norm_matrix = self.faiss_service.embeddings.copy()
            faiss.normalize_L2(norm_matrix)
            new_index.add(norm_matrix)
            
            self.faiss_service.index = new_index
            index_path = os.path.join(self.faiss_service.models_dir, "video.index")
            faiss.write_index(new_index, index_path)
            
            print(f"[IncrementalFaissUpdater] Updated vector in-place for video {vid} at index {idx}.")
            return "UPDATED"
        else:
            # Use FaissSearchService.add_video for dynamic append
            self.faiss_service.add_video(vid, embedding_vec[0])
            print(f"[IncrementalFaissUpdater] Inserted new vector for video {vid}.")
            return "INSERTED"
