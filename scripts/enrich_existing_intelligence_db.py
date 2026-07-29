"""
CMREE Intelligence DB Batch Upgrade Script
Enriches all existing video records in datasets/processed/intelligence_metadata.json
with canonical CMREE fields (primary_ritual, ritual_family, primary_deity, temple, offerings, cmree_confidence, cmree_reasoning_trace).
"""

import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from reasoning_engine.pipeline import CMREEPipeline
from src.content_intelligence.database import IntelligenceDatabase


def upgrade_intelligence_db():
    print("=" * 74)
    print("   UPGRADING INTELLIGENCE DATABASE WITH CMREE CANONICAL METADATA")
    print("=" * 74)

    pipeline = CMREEPipeline()
    db = IntelligenceDatabase()

    records = db.list_records()
    print(f"Loaded {len(records)} existing video records from database.")

    upgraded_count = 0

    for rec in records:
        vid_id = rec.get("video_id", "unknown")

        raw_obs = {
            "video_id": vid_id,
            "scene": rec.get("summary") or rec.get("title") or "",
            "actions": rec.get("actions") or rec.get("activities") or [],
            "objects": rec.get("objects") or rec.get("important_objects") or [],
            "ocr_text": [rec.get("ocr", "")] if isinstance(rec.get("ocr"), str) else rec.get("ocr", []),
            "speech_text": rec.get("transcript", ""),
            "language": rec.get("language", "Hindi"),
            "emotion": rec.get("mood", "Devotional"),
            "confidence": rec.get("overall_confidence", 0.85)
        }

        canonical_doc, issues = pipeline.process_observation(raw_obs)

        # Attach CMREE canonical metadata
        rec["canonical_metadata"] = canonical_doc
        rec["primary_ritual"] = canonical_doc.get("primary_ritual")
        rec["ritual_family"] = canonical_doc.get("ritual_family")
        rec["primary_deity"] = canonical_doc.get("primary_deity")
        rec["temple"] = canonical_doc.get("temple")
        rec["tradition"] = canonical_doc.get("tradition")
        rec["offerings"] = canonical_doc.get("offerings", [])
        rec["cmree_confidence"] = canonical_doc.get("confidence")
        rec["cmree_reasoning_trace"] = canonical_doc.get("provenance", {}).get("reasoning_trace")
        rec["cmree_validation_issues"] = issues
        rec["keywords"] = canonical_doc.get("keywords", rec.get("keywords", []))
        rec["content_type"] = canonical_doc.get("primary_category", rec.get("content_type"))

        db.save_record(vid_id, rec)
        upgraded_count += 1
        print(f"   ✓ Upgraded '{vid_id}': Ritual='{canonical_doc['primary_ritual']}', Deity='{canonical_doc['primary_deity']}' (Conf: {canonical_doc['confidence']:.3f})")

    print("\n" + "=" * 74)
    print(f" SUCCESS: Upgraded {upgraded_count} video records with CMREE Canonical Metadata!")
    print("=" * 74)


if __name__ == "__main__":
    upgrade_intelligence_db()
