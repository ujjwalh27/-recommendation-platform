"""
Processing Lifecycle & Intelligent Reprocessing Manager
Manages state transitions and detects version changes to determine publication actions.
"""

import time
import hashlib
import json
from typing import Dict, Any, Tuple, Optional
from content_catalog.lifecycle.states import ProcessingState, PublicationAction
from content_catalog.catalog.store import ContentCatalogStore


class LifecycleManager:
    """Manages processing lifecycle states and determines intelligent reprocessing actions."""

    def __init__(self, store: Optional[ContentCatalogStore] = None):
        self.store = store or ContentCatalogStore()

    @staticmethod
    def compute_metadata_hash(canonical_metadata: Dict[str, Any]) -> str:
        """Computes deterministic hash over canonical metadata."""
        serialized = json.dumps(canonical_metadata, sort_keys=True)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def evaluate_reprocessing(
        self,
        video_id: str,
        content_hash: str,
        pipeline_result: Dict[str, Any]
    ) -> Tuple[PublicationAction, Dict[str, Any]]:
        """
        Evaluates an ingestion request against the catalog.
        Returns:
            action (PublicationAction): CREATE, UPDATE, or SKIP.
            record (dict): Catalog record to be saved.
        """
        existing = self.store.get_by_hash(content_hash) or self.store.get_by_id(video_id)
        cmree = pipeline_result.get("canonical_metadata", {})
        new_meta_hash = self.compute_metadata_hash(cmree)
        new_category = pipeline_result.get("category", "Pooja & Aarti")
        new_title = pipeline_result.get("title", video_id)
        
        now = time.time()

        if not existing:
            # Brand new video entry
            record = {
                "video_id": video_id,
                "content_hash": content_hash,
                "title": new_title,
                "caption": f"{new_title} - {pipeline_result.get('summary', '')}",
                "summary": pipeline_result.get("summary", ""),
                "category": new_category,
                "matched_category": new_category,
                "subcategory": pipeline_result.get("subcategory", ""),
                "duration": float(pipeline_result.get("duration", 15.0)),
                "language": pipeline_result.get("language", "Hindi"),
                "canonical_metadata": cmree,
                "keywords": cmree.get("keywords", []),
                "primary_ritual": cmree.get("primary_ritual"),
                "ritual_family": cmree.get("ritual_family"),
                "offerings": cmree.get("offerings", []),
                "creator": "ai_intelligence",
                "creator_name": "AI Intelligence Core",
                "views": 100,
                "likes": 10,
                "engagement_score": 15.0,
                "engagement_rate": 0.15,
                "created_time": int(now),
                "created_timestamp": now,
                "last_processed_timestamp": now,
                "last_published_timestamp": now,
                "video_url": f"http://localhost:8000/videos/{video_id}.mp4",
                "thumbnail_url": f"http://localhost:8000/thumbnails/{video_id}.jpg",
                "metadata_hash": new_meta_hash,
                "metadata_version": 1,
                "embedding_version": 1,
                "processing_status": ProcessingState.PUBLISHED.value,
                "indexing_status": "INDEXED",
                "publication_status": "PUBLISHED",
                "processing_history": [{
                    "version": 1,
                    "action": "CREATE",
                    "timestamp": now,
                    "metadata_hash": new_meta_hash
                }]
            }
            return PublicationAction.CREATE, record

        # Existing entry found - evaluate version diff
        old_meta_hash = existing.get("metadata_hash")
        if not old_meta_hash and existing.get("canonical_metadata"):
            old_meta_hash = self.compute_metadata_hash(existing["canonical_metadata"])

        # Check if metadata, category, or title have changed
        has_changed = (
            new_meta_hash != old_meta_hash or
            new_category != existing.get("category") or
            new_title != existing.get("title")
        )

        if not has_changed:
            # No changes detected - SKIP publication
            print(f"[LifecycleManager] Video '{existing['video_id']}' reprocessed: No Changes Detected.")
            existing["last_processed_timestamp"] = now
            existing["processing_status"] = ProcessingState.PUBLISHED.value
            return PublicationAction.SKIP, existing
        else:
            # Metadata/embeddings updated - UPDATE existing record & increment version
            new_meta_version = existing.get("metadata_version", 1) + 1
            new_embed_version = existing.get("embedding_version", 1) + 1

            history_item = {
                "version": new_meta_version,
                "action": "UPDATE",
                "timestamp": now,
                "metadata_hash": new_meta_hash,
                "previous_version": existing.get("metadata_version", 1)
            }
            history = existing.get("processing_history", [])
            history.append(history_item)

            existing.update({
                "title": new_title,
                "category": new_category,
                "subcategory": pipeline_result.get("subcategory", existing.get("subcategory", "")),
                "canonical_metadata": cmree,
                "keywords": cmree.get("keywords", []),
                "primary_ritual": cmree.get("primary_ritual"),
                "ritual_family": cmree.get("ritual_family"),
                "offerings": cmree.get("offerings", []),
                "metadata_hash": new_meta_hash,
                "metadata_version": new_meta_version,
                "embedding_version": new_embed_version,
                "processing_status": ProcessingState.PUBLISHED.value,
                "indexing_status": "INDEXED",
                "publication_status": "PUBLISHED",
                "last_processed_timestamp": now,
                "last_published_timestamp": now,
                "processing_history": history
            })
            print(f"[LifecycleManager] Video '{existing['video_id']}' updated to version {new_meta_version}.")
            return PublicationAction.UPDATE, existing
