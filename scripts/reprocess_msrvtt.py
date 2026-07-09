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
    print(f"Scanning complete. Found {max_videos} video files.")
    
    print("Loading pre-trained SentenceTransformer model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    categories = [
        "Automobile", "Food", "Animation", "Kids/Family", "Animal", 
        "Sports", "Education", "TV Shows", "Comedy", "Tech", 
        "Gamer", "People", "Advertisement", "How-to", "Music", 
        "News", "Fashion", "Travel", "Documentary"
    ]
    category_embeddings = model.encode(categories, normalize_embeddings=True)

    print("Collecting and preparing captions list for all videos...")
    all_captions = []
    videos_durations = []
    
    for idx, video_path in enumerate(video_files):
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
        videos_durations.append(round(duration, 2))
            
        # Get ground truth annotation list
        ann = annotations_by_video.get(video_id)
        if ann and isinstance(ann.get("caption"), list) and len(ann["caption"]) > 0:
            captions = [c.strip() for c in ann["caption"]]
            # If less than 20, pad it
            if len(captions) < 20:
                captions = captions * 20
            captions = captions[:20]
        else:
            fallback = f"A video clip of MSRVTT dataset labeled {video_id}."
            captions = [fallback] * 20
        all_captions.extend(captions)
        
    print(f"Encoding all {len(all_captions)} captions in batches (CPU-optimized)...")
    all_embeddings = model.encode(all_captions, batch_size=512, show_progress_bar=True, normalize_embeddings=True)
    
    print("Performing semantic consensus filtering and zero-shot category classification...")
    videos_metadata = []
    consensus_embeddings = []
    
    for i, video_path in enumerate(tqdm(video_files, desc="Processing videos")):
        video_id = video_path.stem
        duration = videos_durations[i]
        
        # Slice the 20 captions and their corresponding embeddings
        slice_embeddings = all_embeddings[i*20 : (i+1)*20]
        slice_captions = all_captions[i*20 : (i+1)*20]
        
        # 1. Consensus Caption: Find the caption closest to the centroid of all 20 captions
        centroid = np.mean(slice_embeddings, axis=0)
        centroid_norm = np.linalg.norm(centroid)
        if centroid_norm > 0:
            centroid = centroid / centroid_norm
        similarities = np.dot(slice_embeddings, centroid)
        best_idx = np.argmax(similarities)
        consensus_caption = slice_captions[best_idx]
        consensus_emb = slice_embeddings[best_idx]
        
        # 2. Category Classification: Match consensus embedding with target category name embeddings
        cat_similarities = np.dot(category_embeddings, consensus_emb)
        best_cat_idx = np.argmax(cat_similarities)
        category = categories[best_cat_idx]
        
        # Creator handle sampling
        creators = CREATORS_BY_CATEGORY.get(category, CREATORS_BY_CATEGORY["Entertainment"])
        creator = creators[i % len(creators)]
        
        # Generate statistics
        np.random.seed(i)
        views = int(np.random.randint(5000, 200000))
        likes = int(views * np.random.uniform(0.04, 0.15))
        comments = int(likes * np.random.uniform(0.01, 0.05))
        shares = int(likes * np.random.uniform(0.02, 0.08))
        
        engagement_score = likes + comments * 2 + shares * 3
        engagement_rate = round(engagement_score / views, 5)
        created_time = 1600000000 + i * 86400
        
        # Keywords
        words = consensus_caption.lower().replace("a ", "").replace("an ", "").replace("on ", "").replace("the ", "").split()
        keywords = [w for w in words if len(w) > 2]
        
        metadata = {
            "video_id": video_id,
            "caption": consensus_caption,
            "hashtags": f"#{category.lower()} #msrvtt",
            "mentions": "nan",
            "creator": creator,
            "creator_name": creator.replace("_", " ").title(),
            "verified": (i % 7 == 0),
            "music_name": f"Track_{video_id}",
            "music_author": f"Artist_{creator}",
            "duration": duration,
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
        consensus_embeddings.append(consensus_emb)
        
    embeddings = np.vstack(consensus_embeddings).astype("float32")
    video_ids = np.array([v["video_id"] for v in videos_metadata])
    
    # Save processed JSON metadata
    with open(PROCESSED_DIR / "enriched_videos.json", "w", encoding="utf-8") as f:
        json.dump(videos_metadata, f, indent=4)
    print(f"Saved metadata JSON to {PROCESSED_DIR / 'enriched_videos.json'}")
    
    # Save CSV
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
