import json
import os
from typing import List, Dict, Any, Optional
from src.utils.paths import get_path

class IntelligenceDatabase:
    """Intelligence Database to persist extracted video metadata and embeddings."""
    
    def __init__(self, db_path=None):
        self.db_path = db_path or get_path("datasets/processed/intelligence_metadata.json")
        
        # Ensure parent directories exist
        db_dir = os.path.dirname(self.db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
            
        self.data = self._load_db()

    def _load_db(self) -> Dict[str, Any]:
        if not os.path.exists(self.db_path):
            return {}
        try:
            with open(self.db_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[IntelligenceDatabase] Error loading JSON DB: {e}")
            return {}

    def save_record(self, video_id: str, record: Dict[str, Any]) -> None:
        """Saves a single video's intelligence report to the local JSON store."""
        self.data[str(video_id)] = record
        try:
            with open(self.db_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"[IntelligenceDatabase] Error writing to JSON DB: {e}")

    def get_record(self, video_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves a specific video's intelligence report."""
        self.data = self._load_db()
        return self.data.get(str(video_id))

    def list_records(self) -> List[Dict[str, Any]]:
        """Lists all stored video intelligence reports."""
        self.data = self._load_db()
        return list(self.data.values())
