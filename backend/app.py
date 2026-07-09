from pathlib import Path
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, Any

# Ensure the project root is in the python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from src.recommender.service import RecommenderService
from src.indexing.faiss_service import FaissSearchService

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
# CORS
# -------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:3000",
    ],
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
            "thumbnail_url": f"http://127.0.0.1:8000/thumbnails/{vid}.jpg",
            "video_url": f"http://127.0.0.1:8000/videos/{vid}.mp4",
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
            "is_commented": payload.is_commented
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