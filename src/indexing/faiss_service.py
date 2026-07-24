import os
import faiss
import numpy as np
from typing import Tuple, List, Dict, Any
from src.utils.paths import get_path


class FaissSearchService:
    """Manages absolute path-safe loading and querying of the FAISS vector index."""

    def __init__(self):
        self.models_dir = get_path("models")
        self.embeddings_dir = get_path("datasets/embeddings")

        # Load FAISS index
        index_path = os.path.join(self.models_dir, "video.index")
        self.index = faiss.read_index(index_path)

        # Load video ID mappings (both models and embeddings folders might have them, we use the embeddings one)
        video_ids_path = os.path.join(self.embeddings_dir, "video_ids.npy")
        self.video_ids = np.load(video_ids_path, allow_pickle=True)
        # Convert IDs to strings for robust matching
        self.video_ids = np.array([str(vid) for vid in self.video_ids])

        # Load embeddings matrix
        embeddings_path = os.path.join(self.embeddings_dir, "video_embeddings.npy")
        self.embeddings = np.load(embeddings_path).astype("float32")

        # Map video ID to its index in the matrix for quick embedding retrieval
        self.video_id_to_index = {str(vid): idx for idx, vid in enumerate(self.video_ids)}

    def get_embedding(self, video_id: str) -> np.ndarray:
        """Retrieves the embedding vector for a given video ID."""
        idx = self.video_id_to_index.get(str(video_id))
        if idx is None:
            raise KeyError(f"Video ID {video_id} not found in index.")
        return self.embeddings[idx]

    def search_by_id(self, video_id: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """Searches for similar videos using a source video ID."""
        try:
            query_embedding = self.get_embedding(video_id)
            return self.search_by_vector(query_embedding, top_k, exclude_video_id=video_id)
        except KeyError:
            return []

    def search_by_vector(self, embedding: np.ndarray, top_k: int = 10, exclude_video_id: str = None) -> List[Dict[str, Any]]:
        """Searches for similar videos using a raw embedding vector."""
        embedding = embedding.reshape(1, -1)
        faiss.normalize_L2(embedding)

        # Query index
        # Fetch top_k + 1 in case we need to filter out the query video itself
        scores, indices = self.index.search(embedding, top_k + 1)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            
            vid = str(self.video_ids[idx])
            if exclude_video_id and vid == exclude_video_id:
                continue

            results.append({
                "video_id": vid,
                "score": float(score)
            })

        return results[:top_k]

    def add_video(self, video_id: str, embedding: np.ndarray) -> None:
        """Dynamically registers a new video embedding into the FAISS index and disk files."""
        video_id = str(video_id)
        if video_id in self.video_id_to_index:
            print(f"[FaissSearchService] Video {video_id} already indexed. Skipping.")
            return

        embedding_vector = np.array(embedding, dtype="float32").reshape(1, -1)
        faiss.normalize_L2(embedding_vector)

        # 1. Add to FAISS index and save index
        self.index.add(embedding_vector)
        index_path = os.path.join(self.models_dir, "video.index")
        faiss.write_index(self.index, index_path)

        # 2. Append to video_ids array and save
        self.video_ids = np.append(self.video_ids, video_id)
        np.save(os.path.join(self.embeddings_dir, "video_ids.npy"), self.video_ids)
        np.save(os.path.join(self.models_dir, "video_ids.npy"), self.video_ids)

        # 3. Append to embeddings matrix and save
        self.embeddings = np.vstack([self.embeddings, embedding_vector]).astype("float32")
        np.save(os.path.join(self.embeddings_dir, "video_embeddings.npy"), self.embeddings)

        # 4. Update memory lookup map
        self.video_id_to_index[video_id] = len(self.video_ids) - 1
        print(f"[FaissSearchService] Dynamic indexing successful for video {video_id}.")
