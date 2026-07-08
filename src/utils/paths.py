from pathlib import Path

# Project root directory
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# Data directories
DATASETS_DIR = ROOT_DIR / "datasets"
RAW_DATA_DIR = DATASETS_DIR / "raw"
PROCESSED_DATA_DIR = DATASETS_DIR / "processed"
EMBEDDINGS_DIR = DATASETS_DIR / "embeddings"

# Model directories (for FAISS indices)
MODELS_DIR = ROOT_DIR / "models"


def get_project_root() -> Path:
    """Returns the absolute path to the project root directory."""
    return ROOT_DIR


def get_path(relative_path: str) -> Path:
    """Resolves a path relative to the project root."""
    return ROOT_DIR / relative_path
