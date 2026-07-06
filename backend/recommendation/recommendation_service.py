import numpy as np
import pandas as pd

from backend.recommendation.vector_search import VectorSearch

BASE_URL = "http://127.0.0.1:8000"


class RecommendationService:

    def __init__(self):

        self.search = VectorSearch()

        # -----------------------------
        # Embeddings
        # -----------------------------
        self.video_ids = np.load(
            "datasets/embeddings/video_ids.npy",
            allow_pickle=True
        )

        self.embeddings = np.load(
            "datasets/embeddings/video_embeddings.npy"
        )

        # -----------------------------
        # Metadata
        # -----------------------------
        self.metadata = pd.read_csv(
            "datasets/processed/video_metadata.csv"
        )

        self.metadata["video_id"] = self.metadata["video_id"].astype(str)
        self.metadata = self.metadata.set_index("video_id")

        # -----------------------------
        # Rich Video Details
        # -----------------------------
        self.video_details = pd.read_csv(
            "datasets/processed/videos.csv"
        )

        self.video_details["video_id"] = (
            self.video_details["video_id"].astype(str)
        )

        self.video_details = self.video_details.set_index("video_id")

    # -----------------------------------
    # Helper Functions
    # -----------------------------------

    def clean(self, value):

        if pd.isna(value):
            return None

        return value

    def to_int(self, value):

        if pd.isna(value):
            return 0

        return int(value)

    def to_float(self, value):

        if pd.isna(value):
            return 0.0

        return float(value)

    # -----------------------------------
    # Recommendation API
    # -----------------------------------

    def recommend(self, video_id, limit=10):

        video_id = str(video_id)

        matches = np.where(
            self.video_ids.astype(str) == video_id
        )[0]

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

            vid = str(item["video_id"])

            # Skip if metadata is missing
            if vid not in self.metadata.index:
                continue

            if vid not in self.video_details.index:
                continue

            meta = self.metadata.loc[vid]
            details = self.video_details.loc[vid]

            enriched.append({

                "video_id": vid,

                "title": self.clean(details["caption"]),

                "creator": self.clean(details["creator"]),

                "display_name": self.clean(details["creator_name"]),

                "description": self.clean(details["caption"]),

                "music": self.clean(details["music_name"]),

                "music_author": self.clean(details["music_author"]),

                "hashtags": self.clean(details["hashtags"]),

                "verified": bool(details["verified"])
                if not pd.isna(details["verified"])
                else False,

                "views": self.to_int(details["views"]),

                "likes": self.to_int(details["likes"]),

                "comments": self.to_int(details["comments"]),

                "shares": self.to_int(details["shares"]),

                "duration": self.to_float(
                    meta["duration_seconds"]
                ),

                "thumbnail_url":
                    f"{BASE_URL}/thumbnails/{vid}.jpg",

                "video_url":
                    f"{BASE_URL}/videos/{vid}.mp4",

                "score": self.to_float(item["score"])

            })

        return enriched