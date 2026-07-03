import numpy as np

from src.search.faiss_index import FaissIndex


class SimilaritySearch:

    def __init__(self):

        self.index = FaissIndex()

        self.index.load("models")

        self.embeddings = np.load(
            "datasets/embeddings/video_embeddings.npy"
        ).astype("float32")

    def search(self, video_index, top_k=10):

        embedding = self.embeddings[video_index]

        scores, ids = self.index.search(
            embedding,
            top_k + 1
        )

        # Remove the queried video itself
        scores = scores[1:]
        ids = ids[1:]

        return scores, ids