"""
Task 8 – Canonical Metadata Generator Module
Assembles normalized, enriched canonical metadata documents with provenance logs.
This document is the sole input for search, indexing, and recommendation engines.
"""

from typing import Dict, Any


class CanonicalMetadataGenerator:
    """Assembles normalized canonical metadata JSON documents."""

    def generate_canonical_document(
        self,
        video_id: str,
        resolved_obs: Dict[str, Any],
        enriched_metadata: Dict[str, Any],
        field_confidences: Dict[str, Any],
        reasoning_trace: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Builds the normalized canonical metadata document.
        """
        overall_conf = field_confidences.get("overall", {}).get("confidence", 0.85)

        document = {
            "video_id": video_id,
            "primary_category": enriched_metadata.get("primary_category", "Temple Ritual"),
            "primary_ritual": enriched_metadata.get("primary_ritual", "Devotional Worship"),
            "ritual_family": enriched_metadata.get("ritual_family", "Pooja"),
            "primary_deity": enriched_metadata.get("primary_deity"),
            "temple": enriched_metadata.get("temple"),
            "festival": enriched_metadata.get("festival"),
            "tradition": enriched_metadata.get("tradition", "Universal Devotional"),
            "offerings": enriched_metadata.get("offerings", []),
            "language": resolved_obs.get("language", "Hindi"),
            "keywords": enriched_metadata.get("keywords", []),
            "confidence": overall_conf,
            "provenance": {
                "field_confidences": field_confidences,
                "reasoning_trace": reasoning_trace
            }
        }

        return document
