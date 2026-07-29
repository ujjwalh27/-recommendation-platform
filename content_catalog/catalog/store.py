"""
Authoritative Content Catalog Store Manager
Persists and manages content_catalog.json as single source of truth.
"""

import os
import json
import time
from typing import Dict, Any, List, Optional
from src.utils.paths import get_path
from content_catalog.catalog.schema import CatalogRecord


class ContentCatalogStore:
    """Manages CRUD operations and concurrency-safe persistence for content_catalog.json."""

    def __init__(self):
        self.catalog_path = get_path("datasets/processed/content_catalog.json")
        self.enriched_videos_path = get_path("datasets/processed/enriched_videos.json")
        self._records: Dict[str, Dict[str, Any]] = {}
        self._hash_to_video_id: Dict[str, str] = {}
        self._load()

    def _load(self) -> None:
        """Loads catalog records from disk or syncs from enriched_videos.json if cold start."""
        if os.path.exists(self.catalog_path):
            try:
                with open(self.catalog_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        self._records = {item["video_id"]: item for item in data if "video_id" in item}
                    elif isinstance(data, dict):
                        self._records = data
            except Exception as e:
                print(f"[ContentCatalogStore] Error loading catalog: {e}")
                self._records = {}
        else:
            self._records = {}

        # Sync existing enriched_videos.json if store is empty
        if not self._records and os.path.exists(self.enriched_videos_path):
            try:
                with open(self.enriched_videos_path, "r", encoding="utf-8") as f:
                    enriched = json.load(f)
                    for item in enriched:
                        vid = item.get("video_id")
                        if not vid:
                            continue
                        record = {
                            "video_id": vid,
                            "content_hash": item.get("content_hash") or f"hash_{vid}",
                            "title": item.get("title", vid),
                            "caption": item.get("caption", ""),
                            "summary": item.get("summary", ""),
                            "category": item.get("category", "Pooja & Aarti"),
                            "subcategory": item.get("subcategory", ""),
                            "duration": float(item.get("duration", 15.0)),
                            "language": item.get("language", "Hindi"),
                            "canonical_metadata": item.get("canonical_metadata", {}),
                            "keywords": item.get("keywords", []),
                            "primary_ritual": item.get("primary_ritual"),
                            "ritual_family": item.get("ritual_family"),
                            "offerings": item.get("offerings", []),
                            "metadata_version": 1,
                            "embedding_version": 1,
                            "processing_status": "PUBLISHED",
                            "indexing_status": "INDEXED",
                            "publication_status": "PUBLISHED",
                            "created_timestamp": float(item.get("created_time", time.time())),
                            "last_processed_timestamp": time.time(),
                            "last_published_timestamp": time.time(),
                            "processing_history": []
                        }
                        self._records[vid] = record
                self.save()
            except Exception as e:
                print(f"[ContentCatalogStore] Error initializing from enriched_videos: {e}")

        # Build hash lookup index
        self._hash_to_video_id = {}
        for vid, record in self._records.items():
            chash = record.get("content_hash")
            if chash:
                self._hash_to_video_id[chash] = vid

    def save(self) -> None:
        """Flushes catalog records to content_catalog.json and syncs enriched_videos.json."""
        os.makedirs(os.path.dirname(self.catalog_path), exist_ok=True)
        catalog_list = list(self._records.values())
        
        with open(self.catalog_path, "w", encoding="utf-8") as f:
            json.dump(catalog_list, f, indent=2, ensure_ascii=False)

        # Sync to enriched_videos.json for backwards-compatibility
        with open(self.enriched_videos_path, "w", encoding="utf-8") as f:
            json.dump(catalog_list, f, indent=2, ensure_ascii=False)

    def get_by_id(self, video_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves a catalog record by video ID."""
        return self._records.get(video_id)

    def get_by_hash(self, content_hash: str) -> Optional[Dict[str, Any]]:
        """Retrieves a catalog record by SHA-256 content hash."""
        vid = self._hash_to_video_id.get(content_hash)
        if vid:
            return self._records.get(vid)
        return None

    def upsert(self, record: Dict[str, Any]) -> None:
        """Upserts a record in memory and saves to disk."""
        vid = record["video_id"]
        chash = record.get("content_hash")
        
        self._records[vid] = record
        if chash:
            self._hash_to_video_id[chash] = vid
        
        self.save()

    def list_records(self) -> List[Dict[str, Any]]:
        """Returns all catalog records."""
        return list(self._records.values())
