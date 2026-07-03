import json
from pathlib import Path

# -----------------------------
# Paths
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_JSON = BASE_DIR / "datasets" / "raw" / "trending.json"

OUTPUT_JSON = (
    BASE_DIR
    / "datasets"
    / "processed"
    / "videos.json"
)

# -----------------------------
# Load Dataset
# -----------------------------

print("Loading dataset...")

with open(RAW_JSON, "r", encoding="utf-8") as file:
    data = json.load(file)

collector = data["collector"]

print(f"Found {len(collector)} videos")

# -----------------------------
# Process Videos
# -----------------------------

videos = []

for item in collector:

    video = {

        "id": item.get("id"),

        "title": item.get("text", ""),

        "creatorId": item["authorMeta"].get("id"),

        "creatorName": item["authorMeta"].get("name"),

        "creatorNickname": item["authorMeta"].get("nickName"),

        "verified": item["authorMeta"].get("verified"),

        "duration": item["videoMeta"].get("duration"),

        "width": item["videoMeta"].get("width"),

        "height": item["videoMeta"].get("height"),

        "likes": item.get("diggCount", 0),

        "views": item.get("playCount", 0),

        "comments": item.get("commentCount", 0),

        "shares": item.get("shareCount", 0),

        "hashtags": [
            tag.get("name")
            for tag in item.get("hashtags", [])
            if "name" in tag
        ],

        "mentions": item.get("mentions", []),

        "music": item["musicMeta"].get("musicName"),

        "musicAuthor": item["musicMeta"].get("musicAuthor"),

        "videoFile": f"/videos/{item.get('id')}.mp4"

    }

    videos.append(video)

# -----------------------------
# Save
# -----------------------------

with open(
    OUTPUT_JSON,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        videos,
        file,
        indent=4,
        ensure_ascii=False
    )

print()

print("Finished")

print(f"Generated {OUTPUT_JSON}")

print(f"Videos exported : {len(videos)}")