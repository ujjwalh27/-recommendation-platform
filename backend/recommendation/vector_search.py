import faiss
import numpy as np


class VectorSearch:

    def __init__(self):

        self.index = faiss.read_index(
            "models/video.index"
        )

        self.video_ids = np.load(
            "datasets/embeddings/video_ids.npy",
            allow_pickle=True
        )

    def search(self, embedding, k=10):

        embedding = embedding.astype("float32").reshape(1, -1)

        distances, indices = self.index.search(
            embedding,
            k
        )

        results = []

        for score, idx in zip(distances[0], indices[0]):

            results.append({
                "video_id": str(self.video_ids[idx]),
                "score": float(score)
            })

        return results