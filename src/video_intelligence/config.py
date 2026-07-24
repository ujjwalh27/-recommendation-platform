import os

# Ollama settings
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/chat")
VLM_MODEL = os.environ.get("VLM_MODEL", "minicpm-v")

# Storage settings
TEMP_DIR = "datasets/processed/video_intelligence_temp"
DEBUG_DIR = "datasets/processed/debug_pipeline"

# Frame sampling settings
SCENE_THRESHOLD = 0.35      # FFmpeg scene change threshold (0.0 to 1.0)
MIN_SCENE_DURATION_S = 1.0   # Minimum duration between sampled frames
MAX_SAMPLED_FRAMES = 12      # Maximum frames to feed the VLM to keep inference fast

# Confidence scoring weights
WEIGHT_VLM = 0.50
WEIGHT_MODAL_AGREEMENT = 0.30
WEIGHT_COMPLETENESS = 0.20
