import os
import sys
# Ensure project root is in the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import urllib.request
import numpy as np
import pandas as pd
import cv2
import faiss
from sentence_transformers import SentenceTransformer
from pathlib import Path
from tqdm import tqdm

# Setup directories
BASE_DIR = Path(__file__).resolve().parent.parent
MSRVTT_DIR = BASE_DIR / "datasets" / "raw" / "msrvtt"
RAW_DIR = BASE_DIR / "datasets" / "raw"
PROCESSED_DIR = BASE_DIR / "datasets" / "processed"
EMBEDDINGS_DIR = BASE_DIR / "datasets" / "embeddings"
MODELS_DIR = BASE_DIR / "models"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)

# Hugging Face URL for ground truth MSR-VTT annotations
ANNOTATIONS_URL = "https://huggingface.co/datasets/friedrichor/MSR-VTT/resolve/main/msrvtt_train_7k.json"
LOCAL_ANNOTATIONS_PATH = RAW_DIR / "msrvtt_train_7k.json"

# Category mapping to match personas in personas.py
MSRVTT_CATEGORIES_MAPPING = {
    0: "Music",
    1: "People",
    2: "Gamer",           # Gaming -> Gamer
    3: "Sports",
    4: "News",
    5: "Education",
    6: "TV Shows",
    7: "Comedy",
    8: "Animation",
    9: "Automobile",      # Vehicles/Autos -> Automobile
    10: "How-to",
    11: "Travel",
    12: "Tech",           # Science/Technology -> Tech
    13: "Animal",         # Animals/Pets -> Animal
    14: "Kids/Family",
    15: "Documentary",
    16: "Food",           # Food/Drink -> Food
    17: "Food",           # Cooking -> Food
    18: "Fashion",        # Beauty/Fashion -> Fashion
    19: "Advertisement"
}

# Creator handles by category
CREATORS_BY_CATEGORY = {
    "Music": ["guitar_hero", "vocal_tunes", "dj_beats", "orchestra_vibes"],
    "People": ["people_vlogs", "daily_alex", "life_talks", "street_interview"],
    "Gamer": ["gamer_pro", "minecraft_builder", "stream_gaming", "retro_player"],
    "Sports": ["sports_zone", "athletic_pro", "surfing_life", "hoop_dreamer"],
    "News": ["news_bulletin", "politics_today", "world_events", "daily_brief"],
    "Education": ["edu_learn", "history_class", "eng_grammar", "math_genius"],
    "TV Shows": ["tv_clip", "show_highlights", "episode_recaps", "drama_time"],
    "Comedy": ["funny_pranks", "cat_fails", "comic_strip", "standup_daily"],
    "Animation": ["anime_style", "cartoon_fun", "drawn_world", "animation_art"],
    "Automobile": ["car_expert", "motor_rider", "mechanic_classic", "autonomous_drift"],
    "How-to": ["diy_crafts", "how_to_fix", "tutorial_easy", "workshop_pro"],
    "Travel": ["travel_soul", "hiking_nature", "explore_eu", "drone_wanderer"],
    "Tech": ["science_lab", "robotics_demo", "planet_orbit", "tesla_coil_arc"],
    "Animal": ["puppy_tails", "cat_laser", "zoo_world", "savanna_wild"],
    "Kids/Family": ["kids_play", "family_vlog", "toy_reviews", "happy_kids"],
    "Documentary": ["doc_history", "nature_docs", "space_mysteries", "crime_files"],
    "Food": ["chef_master", "baking_art", "street_foodie", "latte_critic"],
    "Fashion": ["runway_style", "makeup_expert", "lookbook_fit", "vintage_designer"],
    "Advertisement": ["ad_spot", "promo_commercial", "brand_story", "product_launch"],
    "Entertainment": ["entertainment_hub", "pop_culture", "movie_clips", "celeb_news"]
}

def download_annotations():
    if not LOCAL_ANNOTATIONS_PATH.exists():
        print(f"Downloading MSR-VTT annotations from {ANNOTATIONS_URL}...")
        urllib.request.urlretrieve(ANNOTATIONS_URL, LOCAL_ANNOTATIONS_PATH)
        print("Download complete.")
    else:
        print("Using existing local MSR-VTT annotations file.")

def build_msrvtt_database():
    download_annotations()
    
    print("Loading annotations JSON...")
    with open(LOCAL_ANNOTATIONS_PATH, "r", encoding="utf-8") as f:
        annotations = json.load(f)
        
    # Map by video_id
    annotations_by_video = {item["video_id"]: item for item in annotations}
    
    print("Scanning local MSR-VTT video folder...")
    video_files = sorted(list(MSRVTT_DIR.glob("*.mp4")), key=lambda x: int(x.stem.replace("video", "")))
    max_videos = len(video_files)
    video_files = video_files[:max_videos]
    print(f"Processing all {max_videos} video files.")
    
    videos_metadata = []
    captions_to_encode = []
    
    for idx, video_path in enumerate(tqdm(video_files, desc="Parsing video metadata")):
        video_id = video_path.stem  # e.g., "video0"
        
        # Read duration with OpenCV
        cap = cv2.VideoCapture(str(video_path))
        duration = 15.0
        if cap.isOpened():
            frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
            fps = cap.get(cv2.CAP_PROP_FPS)
            if fps > 0:
                duration = frame_count / fps
            cap.release()
            
        # Get ground truth annotation
        ann = annotations_by_video.get(video_id)
        if ann:
            # Use the first caption from ground truth list
            caption = ann["caption"][0].strip()
            # Map category ID to persona category name
            cat_id = ann.get("category", 19)
            category = MSRVTT_CATEGORIES_MAPPING.get(cat_id, "Entertainment")
        else:
            caption = f"A video clip of MSRVTT dataset labeled {video_id}."
            category = "Entertainment"
            
        # Creator handle sampling
        creators = CREATORS_BY_CATEGORY.get(category, CREATORS_BY_CATEGORY["Entertainment"])
        creator = creators[idx % len(creators)]
        
        # Generate clean statistics
        np.random.seed(idx)
        views = int(np.random.randint(5000, 200000))
        likes = int(views * np.random.uniform(0.04, 0.15))
        comments = int(likes * np.random.uniform(0.01, 0.05))
        shares = int(likes * np.random.uniform(0.02, 0.08))
        
        engagement_score = likes + comments * 2 + shares * 3
        engagement_rate = round(engagement_score / views, 5)
        created_time = 1600000000 + idx * 86400
        
        # Keywords
        words = caption.lower().replace("a ", "").replace("an ", "").replace("on ", "").replace("the ", "").split()
        keywords = [w for w in words if len(w) > 2]
        
        metadata = {
            "video_id": video_id,
            "caption": caption,
            "hashtags": f"#{category.lower()} #msrvtt",
            "mentions": "nan",
            "creator": creator,
            "creator_name": creator.replace("_", " ").title(),
            "verified": (idx % 7 == 0),
            "music_name": f"Track_{video_id}",
            "music_author": f"Artist_{creator}",
            "duration": round(duration, 2),
            "views": views,
            "likes": likes,
            "comments": comments,
            "shares": shares,
            "engagement_score": float(engagement_score),
            "engagement_rate": engagement_rate,
            "created_time": created_time,
            "video_url": f"http://127.0.0.1:8000/videos/{video_id}.mp4",
            "category": category,
            "keywords": keywords
        }
        
        videos_metadata.append(metadata)
        captions_to_encode.append(caption)
        
    print("Loading pre-trained SentenceTransformer model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    print("Generating real semantic text embeddings...")
    embeddings = model.encode(captions_to_encode, show_progress_bar=True, normalize_embeddings=True)
    embeddings = embeddings.astype("float32")
    
    video_ids = np.array([v["video_id"] for v in videos_metadata])
    
    # Save processed JSON metadata
    with open(PROCESSED_DIR / "enriched_videos.json", "w", encoding="utf-8") as f:
        json.dump(videos_metadata, f, indent=4)
    print(f"Saved metadata JSON to {PROCESSED_DIR / 'enriched_videos.json'}")
    
    # Save CSV for compatibility
    pd.DataFrame(videos_metadata).to_csv(PROCESSED_DIR / "enriched_videos.csv", index=False)
    print(f"Saved metadata CSV to {PROCESSED_DIR / 'enriched_videos.csv'}")
    
    # Save Embeddings
    np.save(EMBEDDINGS_DIR / "video_ids.npy", video_ids)
    np.save(EMBEDDINGS_DIR / "video_embeddings.npy", embeddings)
    np.save(MODELS_DIR / "video_ids.npy", video_ids)
    print("Saved vector embeddings.")
    
    # Compile and Save FAISS index
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)
    faiss.write_index(index, str(MODELS_DIR / "video.index"))
    print(f"FAISS Index compiled and saved with dimension {embeddings.shape[1]}.")
    
    # Regenerate user histories and profiles using the new video metadata
    print("Regenerating mock user watch histories and interest profiles...")
    from src.users.generator import MockDataGenerator
    generator = MockDataGenerator(num_users=60)
    generator.generate()
    print("User mock database regeneration complete.")

if __name__ == "__main__":
    build_msrvtt_database()
