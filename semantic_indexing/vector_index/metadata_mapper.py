"""
Task 4 – Vector Metadata Mapper
Maps FAISS row offsets to video IDs and CMREE canonical metadata records.
"""

from typing import Dict, Any, List, Optional


class VectorMetadataMapper:
    """Manages 1-to-1 mapping between FAISS row offsets, video IDs, and canonical metadata."""

    def __init__(self, catalog: List[Dict[str, Any]] = None):
        self.catalog_lookup = {}
        if catalog:
            self.load_catalog(catalog)

    def load_catalog(self, catalog: List[Dict[str, Any]]):
        self.catalog_lookup = {str(item["video_id"]): item for item in catalog}

    def get_metadata(self, video_id: str) -> Optional[Dict[str, Any]]:
        return self.catalog_lookup.get(str(video_id))
