import os
# ── Python 3.13 / Apple-MPS crash prevention ──────────────────────────────────
# Must be done BEFORE any torch/transformers/easyocr/joblib imports.
# HuggingFace pipelines create DataLoaders with pin_memory=True which causes
# loky semaphore leaks on Python 3.13 that kill the uvicorn worker process.
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

import torch
import torch.utils.data
_OrigDataLoader = torch.utils.data.DataLoader
class _SafeDataLoader(_OrigDataLoader):
    def __init__(self, *args, **kwargs):
        kwargs["pin_memory"] = False
        kwargs["num_workers"] = 0
        super().__init__(*args, **kwargs)
torch.utils.data.DataLoader = _SafeDataLoader
# ──────────────────────────────────────────────────────────────────────────────

from pathlib import Path
import sys
import shutil
import json
import time
import cv2
import numpy as np
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, Any

# Ensure the project root is in the python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from src.recommender.service import RecommenderService
from src.indexing.faiss_service import FaissSearchService
from src.content_intelligence.pipeline import ContentIntelligencePipeline

# --------------------------------------------------
# Project Paths
# --------------------------------------------------

VIDEOS_DIR = BASE_DIR / "datasets" / "raw" / "msrvtt"
THUMBNAILS_DIR = BASE_DIR / "datasets" / "thumbnails"

# Ensure directories exist to prevent StaticFiles RuntimeError
VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
THUMBNAILS_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# FastAPI App
# --------------------------------------------------

app = FastAPI(
    title="Daiv Clips Recommendation Platform API",
    version="2.0",
    description="Production-grade rule-based recommendation platform for Daiv ecosystem clips."
)

# -------------------------------
# Health Check Endpoint
# -------------------------------
@app.get("/health")
def health_check():
    return {
        "status": "HEALTHY",
        "api_version": "2.0-enterprise",
        "pipeline_status": "READY",
        "timestamp": time.time()
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# Static Files
# --------------------------------------------------

app.mount(
    "/videos",
    StaticFiles(directory=str(VIDEOS_DIR)),
    name="videos"
)

app.mount(
    "/thumbnails",
    StaticFiles(directory=str(THUMBNAILS_DIR)),
    name="thumbnails"
)

# --------------------------------------------------
# Recommender Services
# --------------------------------------------------

service = RecommenderService()
faiss_service = FaissSearchService()
ci_pipeline = ContentIntelligencePipeline()

@app.on_event("startup")
def preload_ci_models():
    print("[Startup] Eagerly loading Content Intelligence models into RAM...")
    # Force access to the properties to trigger loading of lazy instances
    _ = ci_pipeline.speech_rec
    _ = ci_pipeline.ocr_det
    _ = ci_pipeline.obj_det
    _ = ci_pipeline.scene_und
    _ = ci_pipeline.act_rec
    _ = ci_pipeline.aud_det
    _ = ci_pipeline.embedding_model
    _ = ci_pipeline.intelligence_engine
    print("[Startup] Eager loading complete! All CI models are pre-loaded in memory.")

# --------------------------------------------------
# Schemas
# --------------------------------------------------

class FeedbackPayload(BaseModel):
    user_id: str
    video_id: str
    watch_completion_rate: float
    watch_time_seconds: float = 0.0
    replay_count: int = 0
    is_liked: bool = False
    is_saved: bool = False
    is_shared: bool = False
    is_commented: bool = False
    is_final: bool = False

# --------------------------------------------------
# Routes
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "status": "running",
        "message": "Daiv Recommendation Engine is running",
        "version": "2.0"
    }


@app.get("/feed")
def feed(user_id: str = "user_1", limit: int = 10):
    """
    Returns personalized recommendation feed with scoring details and natural explanations.
    Accepts user_id (e.g. 'user_1') or persona name (e.g. 'Gamer', 'Traveler', 'Automobile Enthusiast').
    """
    return service.get_recommendations(user_id, limit=limit)


@app.get("/recommend/{video_id}")
def recommend(video_id: str, limit: int = 10):
    """
    Returns items semantically similar to the given video_id using FAISS search.
    """
    results = faiss_service.search_by_id(video_id, top_k=limit)
    
    enriched = []
    video_lookup = service.candidate_generator.video_lookup
    
    for item in results:
        vid = item["video_id"]
        meta = video_lookup.get(vid)
        if not meta:
            continue
            
        enriched.append({
            "video_id": vid,
            "title": meta.get("caption") or f"Clip {vid}",
            "duration": float(meta.get("duration", 0.0)),
            "category": meta.get("category", "Entertainment"),
            "thumbnail_url": f"http://localhost:8000/thumbnails/{vid}.jpg",
            "video_url": f"http://localhost:8000/videos/{vid}.mp4",
            "score": item["score"]
        })
        
    return enriched


@app.post("/feedback")
def feedback(payload: FeedbackPayload):
    """
    Submits user interaction feedback (watch time, like, save, etc.)
    and recalculates user interest profile/creator affinities.
    """
    return service.submit_feedback(
        user_id=payload.user_id,
        video_id=payload.video_id,
        engagement={
            "watch_completion_rate": payload.watch_completion_rate,
            "watch_time_seconds": payload.watch_time_seconds,
            "replay_count": payload.replay_count,
            "is_liked": payload.is_liked,
            "is_saved": payload.is_saved,
            "is_shared": payload.is_shared,
            "is_commented": payload.is_commented,
            "is_final": payload.is_final
        }
    )


@app.get("/profile/{user_id}")
def get_user_profile(user_id: str):
    """
    Returns current interest profile, creator affinities, and watch statistics for a user.
    """
    user = service.find_user_by_id_or_persona(user_id)
    uid = user["user_id"]
    
    interest_profile = service.interest_profiles.get(uid, {})
    creator_affinities = service.user_creator_affinities.get(uid, {})
    watch_history = service.user_watch_histories.get(uid, [])
    
    return {
        "user_id": uid,
        "username": user["username"],
        "persona": user["persona"],
        "interests": interest_profile.get("interests", {}),
        "creator_affinities": creator_affinities,
        "total_watched": len(watch_history)
    }


# --------------------------------------------------
# Content Intelligence Routes
# --------------------------------------------------

@app.post("/content-intelligence/analyze")
def analyze_video(file: UploadFile = File(...)):
    """
    Uploads a raw video file, executes the Content Intelligence Pipeline,
    dynamically embeds metadata, updates FAISS index, and registers it in the recommender feed catalog.
    """
    # 1. Generate unique video ID
    timestamp = int(time.time())
    video_id = f"video_ci_{timestamp}"
    
    # 2. Save video file to static mount directory
    video_filename = f"{video_id}.mp4"
    video_path = VIDEOS_DIR / video_filename
    
    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # 3. Extract thumbnail frame 0
    thumbnail_path = THUMBNAILS_DIR / f"{video_id}.jpg"
    cap = cv2.VideoCapture(str(video_path))
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(str(thumbnail_path), frame)
    else:
        # Save placeholder black thumbnail
        black_img = np.zeros((360, 640, 3), dtype=np.uint8)
        cv2.imwrite(str(thumbnail_path), black_img)
    cap.release()
    
    # 4. Execute Content Intelligence Pipeline
    record = ci_pipeline.analyze_video(str(video_path), video_id, force_reanalyze=True)
    
    # 5. Dynamic FAISS Vector Indexing
    faiss_service.add_video(video_id, record["embedding"])
    
    # 6. Map Category safely matching platform personas
    category_label = record.get("category", "Entertainment")
    known_categories = [
        "Automobile", "Food", "Animation", "Kids/Family", "Animal", 
        "Sports", "Education", "TV Shows", "Comedy", "Tech", 
        "Gamer", "People", "Advertisement", "How-to", "Music", 
        "News", "Fashion", "Travel", "Documentary"
    ]
    matched_category = "Entertainment"
    for cat in known_categories:
        if cat.lower() in category_label.lower():
            matched_category = cat
            break
            
    # 7. Compile video metadata to append to enriched_videos.json
    duration = 15.0
    cap = cv2.VideoCapture(str(video_path))
    if cap.isOpened():
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        if fps > 0:
            duration = frame_count / fps
        cap.release()

    video_meta = {
        "video_id": video_id,
        "caption": f"{record['title']} - {record['summary']}",
        "hashtags": " ".join([f"#{t.lower()}" for t in record["tags"]]),
        "mentions": "nan",
        "creator": "ai_intelligence",
        "creator_name": "AI Intelligence Core",
        "verified": True,
        "music_name": f"Synthesis_{video_id}",
        "music_author": "AI Synthesizer",
        "duration": round(duration, 2),
        "views": 100,
        "likes": 10,
        "comments": 2,
        "shares": 1,
        "engagement_score": 15.0,
        "engagement_rate": 0.15,
        "created_time": timestamp,
        "video_url": f"http://localhost:8000/videos/{video_filename}",
        "category": matched_category,
        "keywords": record["keywords"]
    }
    
    # Load and append to enriched_videos.json
    enriched_path = BASE_DIR / "datasets" / "processed" / "enriched_videos.json"
    existing_meta = []
    if enriched_path.exists():
        try:
            with open(enriched_path, "r", encoding="utf-8") as f:
                existing_meta = json.load(f)
        except Exception:
            pass
            
    existing_meta.append(video_meta)
    
    with open(enriched_path, "w", encoding="utf-8") as f:
        json.dump(existing_meta, f, indent=4)
        
    # 8. Register in recommender service catalog in memory
    service.candidate_generator.video_lookup[video_id] = video_meta
    
    # 9. Return JSON intelligence report
    return record


@app.get("/content-intelligence/videos")
def list_analyzed_videos():
    """
    Lists all videos that have been analyzed by the content intelligence layer.
    """
    return ci_pipeline.db.list_records()


@app.get("/content-intelligence/video/{video_id}")
def get_analyzed_video(video_id: str):
    """
    Retrieves the complete intelligence report for a given video ID.
    """
    record = ci_pipeline.db.get_record(video_id)
    if not record:
        return {"status": "error", "message": f"Analysis for video {video_id} not found."}
    return record