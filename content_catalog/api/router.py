"""
Catalog Management REST API Router
Exposes OpenAPI endpoints for content publication, catalog inspection, status tracking, and audit logging.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Query
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import os
import shutil
import time
from content_catalog.publisher.publisher import ContentPublisher
from content_catalog.catalog.store import ContentCatalogStore
from content_catalog.audit.logger import AuditLogger

router = APIRouter(prefix="/api/catalog", tags=["Content Catalog"])

# Shared singleton instances
catalog_store = ContentCatalogStore()
audit_logger = AuditLogger()


class PublishRequestPayload(BaseModel):
    video_id: str
    video_file_path: str
    pipeline_result: Dict[str, Any]


@router.post("/publish")
def publish_content(payload: PublishRequestPayload):
    """
    Publishes a processed video to the recommendation catalog and live feed.
    Validates pre-conditions, enforces duplicate detection, updates FAISS, and logs audit event.
    """
    publisher = ContentPublisher()
    result = publisher.publish_video(
        video_file_path=payload.video_file_path,
        pipeline_result=payload.pipeline_result,
        video_id=payload.video_id
    )
    if result.get("publication_status") == "BLOCKED":
        raise HTTPException(status_code=400, detail=result.get("failure_reason"))
        
    return result


@router.get("/list")
def list_catalog(limit: int = 50, category: Optional[str] = None):
    """
    Lists catalog entries with optional category filter.
    """
    records = catalog_store.list_records()
    if category:
        records = [r for r in records if r.get("category") == category]
    return records[:limit]


@router.get("/{video_id}")
def get_catalog_entry(video_id: str):
    """
    Retrieves detailed catalog information for a specific video ID.
    """
    record = catalog_store.get_by_id(video_id)
    if not record:
        raise HTTPException(status_code=404, detail=f"Catalog record for video ID '{video_id}' not found.")
    return record


@router.get("/status/{video_id}")
def get_catalog_status(video_id: str):
    """
    Views processing, indexing, and publication status for a video ID.
    """
    record = catalog_store.get_by_id(video_id)
    if not record:
        raise HTTPException(status_code=404, detail=f"Catalog status for video ID '{video_id}' not found.")
        
    return {
        "video_id": record["video_id"],
        "content_hash": record.get("content_hash"),
        "processing_status": record.get("processing_status"),
        "indexing_status": record.get("indexing_status"),
        "publication_status": record.get("publication_status"),
        "metadata_version": record.get("metadata_version", 1),
        "last_published_timestamp": record.get("last_published_timestamp")
    }


@router.get("/audit/{video_id}")
def get_audit_trail(video_id: str):
    """
    Retrieves complete processing audit history logs for a video ID.
    """
    logs = audit_logger.get_logs_for_video(video_id)
    return {
        "video_id": video_id,
        "total_audit_events": len(logs),
        "audit_logs": logs
    }


@router.put("/reprocess/{video_id}")
def reprocess_video(video_id: str, payload: Dict[str, Any]):
    """
    Reprocesses and updates an existing catalog video entry.
    """
    record = catalog_store.get_by_id(video_id)
    if not record:
        raise HTTPException(status_code=404, detail=f"Cannot reprocess. Video ID '{video_id}' not found.")
        
    publisher = ContentPublisher()
    file_path = payload.get("video_file_path") or f"datasets/raw/msrvtt/{video_id}.mp4"
    
    result = publisher.publish_video(
        video_file_path=file_path,
        pipeline_result=payload.get("pipeline_result", record),
        video_id=video_id
    )
    return result
