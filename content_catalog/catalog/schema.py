"""
Content Catalog Data Schemas & Validations
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import time


class CatalogRecord(BaseModel):
    video_id: str
    content_hash: str
    title: str
    caption: Optional[str] = ""
    summary: Optional[str] = ""
    category: str = "Pooja & Aarti"
    subcategory: Optional[str] = ""
    duration: float = 15.0
    language: str = "Hindi"
    canonical_metadata: Dict[str, Any] = Field(default_factory=dict)
    keywords: List[str] = Field(default_factory=list)
    primary_ritual: Optional[str] = None
    ritual_family: Optional[str] = None
    offerings: List[str] = Field(default_factory=list)
    
    metadata_version: int = 1
    embedding_version: int = 1
    
    processing_status: str = "PUBLISHED"
    indexing_status: str = "INDEXED"
    publication_status: str = "PUBLISHED"
    
    created_timestamp: float = Field(default_factory=time.time)
    last_processed_timestamp: float = Field(default_factory=time.time)
    last_published_timestamp: float = Field(default_factory=time.time)
    
    processing_history: List[Dict[str, Any]] = Field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()
