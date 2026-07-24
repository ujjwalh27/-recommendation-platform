import os

MEMORY_STORE_PATH = os.environ.get("MEMORY_STORE_PATH", "datasets/processed/semantic_memory.json")
MIN_CONFIDENCE_THRESHOLD = 0.30
HYPOTHESES_MAX_COUNT = 3

# Source Trust Weights for Conflict Resolution
SOURCE_WEIGHTS = {
    "Speech": 0.95,
    "VLM": 0.90,
    "OCR": 0.85,
    "YOLO": 0.80,
    "VideoMAE": 0.75,
    "AST": 0.70,
    "CLIP": 0.65
}
