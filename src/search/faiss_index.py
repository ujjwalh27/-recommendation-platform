import faiss
import numpy as np
import os


class FaissIndex:

    def __init__(self):

        self.index = None
        self.video_ids = None

    def build(self, embeddings, video_ids):

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(dimension)

        faiss.normalize_L2(embeddings)

        self.index.add(embeddings)

        self.video_ids = video_ids

    def save(self, folder):

        os.makedirs(folder, exist_ok=True)

        faiss.write_index(
            self.index,
            os.path.join(folder, "video.index")
        )

        np.save(
            os.path.join(folder, "video_ids.npy"),
            self.video_ids
        )

    def load(self, folder):

        self.index = faiss.read_index(
            os.path.join(folder, "video.index")
        )

        self.video_ids = np.load(
            os.path.join(folder, "video_ids.npy"),
            allow_pickle=True
        )

    def search(self, embedding, top_k=10):

        embedding = embedding.reshape(1, -1)

        faiss.normalize_L2(embedding)

        scores, indices = self.index.search(
            embedding,
            top_k
        )

        return scores[0], self.video_ids[indices[0]]