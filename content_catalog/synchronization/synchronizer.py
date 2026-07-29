"""
Real-Time Recommendation Feed Synchronizer
Synchronizes published catalog entries directly into live RecommenderService memory caches.
"""

from typing import Dict, Any, Optional
from src.recommender.service import RecommenderService


class CatalogFeedSynchronizer:
    """Updates candidate generator lookup maps and category indices in real time without service restart."""

    def __init__(self, recommender_service: Optional[RecommenderService] = None):
        self.service = recommender_service

    def synchronize(self, catalog_record: Dict[str, Any]) -> None:
        """Pushes a newly published catalog entry into the active candidate lookup engine."""
        if not self.service:
            # RecommenderService is singleton / memory instance
            return

        vid = catalog_record["video_id"]
        cg = self.service.candidate_generator

        # Update candidate generator main videos list
        cg.videos = [v for v in cg.videos if v.get("video_id") != vid]
        cg.videos.append(catalog_record)

        # Update candidate generator video lookup dictionary
        cg.video_lookup[vid] = catalog_record

        # Update category lookup index
        cat = catalog_record.get("category", "Pooja & Aarti")
        if cat in cg.videos_by_category:
            filtered = [v for v in cg.videos_by_category[cat] if v.get("video_id") != vid]
            filtered.append(catalog_record)
            cg.videos_by_category[cat] = filtered
        else:
            cg.videos_by_category[cat] = [catalog_record]

        # Update ritual family lookup index
        family = catalog_record.get("ritual_family")
        if family:
            filt = [v for v in cg.videos_by_ritual_family.get(family, []) if v.get("video_id") != vid]
            filt.append(catalog_record)
            cg.videos_by_ritual_family[family] = filt

        # Update service level helper maps
        self.service.video_to_category[vid] = cat
        self.service.video_to_creator[vid] = catalog_record.get("creator", "ai_intelligence")

        print(f"[CatalogFeedSynchronizer] Synchronized '{vid}' into live recommendation feed memory cache.")
