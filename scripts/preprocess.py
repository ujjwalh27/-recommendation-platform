import json
import pandas as pd
from pathlib import Path

INPUT_FILE = Path("datasets/raw/trending.json")
OUTPUT_FILE = Path("datasets/processed/videos.csv")


def safe_get(dictionary, *keys, default=""):
    value = dictionary

    for key in keys:
        if isinstance(value, dict):
            value = value.get(key)
        else:
            return default

    return value if value is not None else default


with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

videos = []

for video in data["collector"]:

    hashtags = [
        h.get("name", "")
        for h in video.get("hashtags", [])
    ]

    mentions = video.get("mentions", [])

    views = video.get("playCount", 0)
    likes = video.get("diggCount", 0)
    comments = video.get("commentCount", 0)
    shares = video.get("shareCount", 0)

    engagement_score = (
        likes +
        comments * 2 +
        shares * 3
    )

    engagement_rate = (
        engagement_score / views
        if views > 0 else 0
    )

    videos.append({

        "video_id": video.get("id"),

        "caption": video.get("text", ""),

        "hashtags": " ".join(hashtags),

        "mentions": " ".join(mentions),

        "creator": safe_get(video, "authorMeta", "name"),

        "creator_name": safe_get(video, "authorMeta", "nickName"),

        "verified": safe_get(video, "authorMeta", "verified", default=False),

        "music_name": safe_get(video, "musicMeta", "musicName"),

        "music_author": safe_get(video, "musicMeta", "musicAuthor"),

        "duration": safe_get(video, "videoMeta", "duration", default=0),

        "views": views,

        "likes": likes,

        "comments": comments,

        "shares": shares,

        "engagement_score": engagement_score,

        "engagement_rate": round(engagement_rate, 5),

        "created_time": video.get("createTime"),

        "video_url": video.get("webVideoUrl", "")
    })

df = pd.DataFrame(videos)

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("=" * 50)
print("Dataset created successfully")
print("=" * 50)
print()

print(df.head())

print()

print(f"Total Videos : {len(df)}")

print(f"Columns : {len(df.columns)}")