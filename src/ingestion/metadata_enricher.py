import re
from typing import List, Dict, Any
import pandas as pd
import json
from src.utils.paths import get_path

# Categories and their keyword triggers
CATEGORY_KEYWORDS = {
    "Automobile": [
        "car", "cars", "bike", "bikes", "auto", "race", "driving", "drive", "wheel", 
        "motor", "engine", "vehicle", "tesla", "bmw", "audi", "toyota", "ferrari", 
        "supercar", "racing", "blade"
    ],
    "Tech": [
        "tech", "technology", "iphone", "phone", "computer", "coding", "gadget", 
        "programming", "software", "hardware", "app", "robotic", "android", "ios", 
        "bend test", "tutorial", "hacks", "trick", "learn", "education", "science"
    ],
    "Food": [
        "food", "recipe", "cook", "cooking", "eat", "eating", "pizza", "chef", "cake", 
        "delicious", "kitchen", "baking", "restaurant", "yummy", "snack", "dessert", 
        "dinner", "lunch", "breakfast", "tasty", "foodmeme", "stamppot"
    ],
    "Animal": [
        "dog", "cat", "animal", "animals", "pet", "pets", "puppy", "puppies", "kitten", 
        "cute", "bird", "lion", "zoo", "pug", "puglife"
    ],
    "Travel": [
        "travel", "trip", "vacation", "beach", "mountain", "nature", "explore", 
        "destination", "world", "flight", "adventure", "lake", "sea", "ocean", "landscape"
    ],
    "Gamer": [
        "roblox", "minecraft", "game", "gamer", "gaming", "xbox", "playstation", 
        "nintendo", "fortnite", "pubg", "multiplayer", "trollingexploits"
    ]
}

# Stopwords to filter out during keyword extraction
STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "is", "are", "was", "were", "to", "for", 
    "in", "on", "at", "by", "with", "from", "of", "about", "as", "into", "like", 
    "through", "this", "that", "these", "those", "my", "your", "his", "her", "its", 
    "our", "their", "me", "you", "him", "us", "them", "i", "we", "he", "she", "it",
    "they", "foryou", "fyp", "foryoupage", "fy", "viral", "trending", "tiktok", "follow"
}


class MetadataEnricher:
    """Enriches video metadata with category mapping and keyword extraction."""

    def __init__(self):
        self.input_csv = get_path("datasets/processed/videos.csv")
        self.output_csv = get_path("datasets/processed/enriched_videos.csv")
        self.output_json = get_path("datasets/processed/enriched_videos.json")

    def _clean_text(self, text: Any) -> str:
        """Cleans input text for keyword matching."""
        if pd.isna(text):
            return ""
        text = str(text).lower()
        # Remove URLs
        text = re.sub(r"http\S+", "", text)
        # Keep alphanumeric characters and spaces
        text = re.sub(r"[^a-zA-Z0-9\s#]", "", text)
        return text

    def map_category(self, caption: str, hashtags: str, music: str) -> str:
        """Determines the video category based on keyword matches."""
        combined_text = f"{caption} {hashtags} {music}".lower()
        
        scores = {}
        for category, keywords in CATEGORY_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in combined_text)
            if score > 0:
                scores[category] = score

        if not scores:
            return "Entertainment"  # Default category
        
        # Return the category with highest match count
        return max(scores, key=scores.get)

    def extract_keywords(self, caption: str, hashtags: str) -> List[str]:
        """Extracts unique relevant keywords from text and hashtags."""
        raw_words = f"{caption} {hashtags}".lower().split()
        keywords = set()
        
        for word in raw_words:
            # Strip hashtag symbol
            clean_word = word.replace("#", "").strip()
            # Filter criteria: length > 2 and not a stopword and not numerical only
            if (
                len(clean_word) > 2 
                and clean_word not in STOPWORDS 
                and not clean_word.isdigit()
            ):
                keywords.add(clean_word)
                
        return list(keywords)

    def enrich(self) -> None:
        """Runs the enrichment pipeline, saving both CSV and JSON formats."""
        print(f"Reading dataset from {self.input_csv}...")
        df = pd.read_csv(self.input_csv)

        enriched_videos = []
        for _, row in df.iterrows():
            caption = str(row.get("caption", ""))
            hashtags = str(row.get("hashtags", ""))
            music = str(row.get("music_name", ""))
            video_id = str(row["video_id"])

            cleaned_caption = self._clean_text(caption)
            cleaned_hashtags = self._clean_text(hashtags)
            cleaned_music = self._clean_text(music)

            category = self.map_category(cleaned_caption, cleaned_hashtags, cleaned_music)
            keywords = self.extract_keywords(cleaned_caption, cleaned_hashtags)

            video_data = {
                "video_id": video_id,
                "caption": caption,
                "hashtags": hashtags,
                "mentions": str(row.get("mentions", "")),
                "creator": str(row.get("creator", "")),
                "creator_name": str(row.get("creator_name", "")),
                "verified": bool(row.get("verified", False)),
                "music_name": music,
                "music_author": str(row.get("music_author", "")),
                "duration": float(row.get("duration", 0.0)),
                "views": int(row.get("views", 0)),
                "likes": int(row.get("likes", 0)),
                "comments": int(row.get("comments", 0)),
                "shares": int(row.get("shares", 0)),
                "engagement_score": float(row.get("engagement_score", 0.0)),
                "engagement_rate": float(row.get("engagement_rate", 0.0)),
                "created_time": int(row.get("created_time", 0)),
                "video_url": str(row.get("video_url", "")),
                "category": category,
                "keywords": keywords
            }
            enriched_videos.append(video_data)

        # Save to CSV
        enriched_df = pd.DataFrame(enriched_videos)
        # Convert list to string for CSV compatibility
        csv_df = enriched_df.copy()
        csv_df["keywords"] = csv_df["keywords"].apply(lambda k: " ".join(k))
        csv_df.to_csv(self.output_csv, index=False)
        print(f"Saved enriched metadata CSV to {self.output_csv}")

        # Save to JSON
        with open(self.output_json, "w", encoding="utf-8") as f:
            json.dump(enriched_videos, f, indent=4, ensure_ascii=False)
        print(f"Saved enriched metadata JSON to {self.output_json}")

        # Summary statistics
        print("\nEnrichment Statistics:")
        print(f"Total videos processed: {len(enriched_df)}")
        print("\nCategory distribution:")
        print(enriched_df["category"].value_counts())
