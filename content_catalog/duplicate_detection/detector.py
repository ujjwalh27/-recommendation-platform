"""
Duplicate & Idempotency Detection Engine
Detects existing catalog records based on content hash or stable video ID.
"""

from typing import Tuple, Optional, Dict, Any
from content_catalog.catalog.store import ContentCatalogStore
from content_catalog.duplicate_detection.hasher import ContentHasher


class DuplicateDetector:
    """Detects whether a processed video is a new entry, an exact duplicate, or an update."""

    def __init__(self, store: Optional[ContentCatalogStore] = None):
        self.store = store or ContentCatalogStore()

    def check_duplicate(self, video_file_path: str, video_id: Optional[str] = None) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        Checks if the video is already present in the catalog.
        Returns:
            is_duplicate (bool): True if an existing entry matches content_hash or video_id.
            content_hash (str): Computed SHA-256 hash.
            existing_record (dict or None): Existing catalog entry if duplicate found.
        """
        content_hash = ContentHasher.compute_file_hash(video_file_path)

        # 1. Check by content hash
        existing = self.store.get_by_hash(content_hash)
        if existing:
            return True, content_hash, existing

        # 2. Check by explicit video ID if provided
        if video_id:
            existing = self.store.get_by_id(video_id)
            if existing:
                return True, content_hash, existing

        return False, content_hash, None
