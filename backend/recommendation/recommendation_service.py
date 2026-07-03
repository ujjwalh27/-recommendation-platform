import numpy as np
import pandas as pd

from backend.recommendation.vector_search import VectorSearch


BASE_URL = "http://127.0.0.1:8000"


class RecommendationService:

    def __init__(self):

        self.search = VectorSearch()

        self.video_ids = np.load(
            "datasets/embeddings/video_ids.npy",
            allow_pickle=True
        )

        self.embeddings = np.load(
            "datasets/embeddings/video_embeddings.npy"
        )

        self.metadata = pd.read_csv(
            "datasets/processed/video_metadata.csv"
        )

        self.metadata = self.metadata.set_index("video_id")

    def recommend(self, video_id, limit=10):

        matches = np.where(self.video_ids == video_id)[0]

        if len(matches) == 0:
            return {
                "error": "Video not found"
            }

        embedding = self.embeddings[matches[0]]

        results = self.search.search(
            embedding,
            k=limit
        )

        enriched = []

        for item in results:

            vid = item["video_id"]

            meta = self.metadata.loc[int(vid)]

            enriched.append({

                "video_id": vid,

                "title": vid,

                "duration": meta["duration_seconds"],

                "thumbnail_url":
                    f"{BASE_URL}/thumbnails/{vid}.jpg",

                "video_url":
                    f"{BASE_URL}/videos/{vid}.mp4",

                "score": item["score"]

            })

        return enriched