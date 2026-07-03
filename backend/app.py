from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.recommendation.recommendation_service import RecommendationService

# --------------------------------------------------
# Project Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

VIDEOS_DIR = BASE_DIR / "datasets" / "raw" / "videos"
THUMBNAILS_DIR = BASE_DIR / "datasets" / "thumbnails"

# --------------------------------------------------
# FastAPI App
# --------------------------------------------------

app = FastAPI(
    title="Recommendation Engine",
    version="1.0"
)
# -------------------------------
# CORS
# -------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
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
# Recommendation Service
# --------------------------------------------------

service = RecommendationService()

# --------------------------------------------------
# Routes
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "status": "running",
        "message": "Recommendation Engine is running"
    }


@app.get("/feed")
def feed():
    """
    Temporary feed endpoint.
    Uses one seed video until
    user-specific recommendation
    is implemented.
    """

    seed_video = "6875317312082201857"

    return service.recommend(seed_video)


@app.get("/recommend/{video_id}")
def recommend(video_id: str):
    """
    Returns videos similar to the given video.
    """

    return service.recommend(video_id)