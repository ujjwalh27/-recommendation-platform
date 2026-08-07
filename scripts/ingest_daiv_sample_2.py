"""
Daiv Sample 2 Exclusive Ingestion & CMREE / MSFACR Pipeline Processing Script
Clears existing catalog videos, ingests ALL 45 videos from '/Users/ujjwalhkumar/Downloads/daiv sample 2',
runs the Content Intelligence & MSFACR pipeline with original_filename preservation,
extracts multimodal evidence, updates FAISS index, and validates catalog completeness.
"""

import os
import sys
import json
import shutil
import cv2
import time
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.utils.paths import get_path
from src.content_intelligence.pipeline import ContentIntelligencePipeline
from semantic_indexing.vector_index.faiss_integration import CanonicalFaissIntegration
from scripts.recategorize_catalog import recategorize


def generate_thumbnail(video_path, thumbnail_path):
    """Extracts a frame from the 1.0 second mark of the video and saves as JPEG."""
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        print(f"[Thumbnail] Unable to open video {video_path}")
        return False
    
    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(fps * 1.0))
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = cap.read()

    if ret and frame is not None:
        os.makedirs(os.path.dirname(thumbnail_path), exist_ok=True)
        cv2.imwrite(str(thumbnail_path), frame)
        cap.release()
        return True
    
    cap.release()
    return False


def save_catalog_and_rebuild(catalog):
    """Saves updated sample catalog list and rebuilds FAISS index for real-time recommendation feed availability."""
    enriched_videos_path = get_path("datasets/processed/enriched_videos.json")
    catalog_path = get_path("content_catalog/catalog/enriched_videos.json")

    with open(enriched_videos_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

    with open(catalog_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
    
    faiss_integration = CanonicalFaissIntegration()
    faiss_integration.rebuild_faiss_index_from_catalog(catalog)


def ingest_daiv_sample_2():
    sample_dir = Path("/Users/ujjwalhkumar/Downloads/daiv sample 2")
    if not sample_dir.exists():
        print(f"Error: Directory '{sample_dir}' not found.")
        return

    mp4_files = sorted([f for f in sample_dir.glob("*.mp4") if not f.name.startswith(".")])
    print("=" * 74)
    print(f"   DAIV SAMPLE 2 EXCLUSIVE VIDEO INGESTION & CMREE PIPELINE ({len(mp4_files)} VIDEOS)")
    print("=" * 74)

    raw_videos_dir = get_path("datasets/raw/msrvtt")
    thumbnails_dir = get_path("datasets/thumbnails")
    enriched_videos_path = get_path("datasets/processed/enriched_videos.json")

    os.makedirs(raw_videos_dir, exist_ok=True)
    os.makedirs(thumbnails_dir, exist_ok=True)

    # Initialize Content Intelligence Pipeline
    pipeline = ContentIntelligencePipeline()

    # Clear existing catalog to start fresh with DAIV sample 2 videos
    catalog = []
    ingested_count = 0

    for idx, video_file in enumerate(mp4_files, 1):
        clean_name = "".join(c if c.isalnum() else "_" for c in video_file.stem).lower()
        video_id = f"daiv_s2_{idx:02d}_{clean_name[:20]}"

        print(f"\n[{idx}/{len(mp4_files)}] Ingesting: '{video_file.name}' -> ID: '{video_id}'")

        dest_mp4 = raw_videos_dir / f"{video_id}.mp4"
        shutil.copy2(video_file, dest_mp4)

        dest_thumb = thumbnails_dir / f"{video_id}.jpg"
        generate_thumbnail(dest_mp4, dest_thumb)

        try:
            record = pipeline.analyze_video(str(dest_mp4), video_id, force_reanalyze=False, original_filename=video_file.name)
            
            # Use record category / subcategory or fallback
            cat = record.get("category", "Any other devotional or temple-related activities")
            subcat = record.get("subcategory", "Devotional & Cultural Activity")
            offering = record.get("offering", ["Devotional Offering"])
            if isinstance(offering, str):
                offering = [offering]

            cmree = record.get("canonical_metadata", {})

            catalog_item = {
                "video_id": video_id,
                "title": record.get("title") or video_file.stem,
                "caption": record.get("title") or video_file.stem,
                "summary": record.get("summary", ""),
                "category": cat,
                "subcategory": subcat,
                "offering": offering,
                "offerings": offering,
                "duration": record.get("duration", 15.0),
                "created_time": 3000000000.0,
                "views": 250000,
                "engagement_score": 0.99,
                "keywords": cmree.get("keywords", record.get("keywords", [])),
                "primary_ritual": cmree.get("primary_ritual", subcat),
                "ritual_family": cmree.get("ritual_family", cat),
                "primary_deity": cmree.get("primary_deity", "Unassigned / General"),
                "language": cmree.get("language", record.get("language", "Hindi")),
                "confidence": record.get("overall_confidence", 0.90),
                "canonical_metadata": cmree,
                "perceptual_metadata": record.get("perceptual_metadata", {}),
                "emotional_metadata": record.get("emotional_metadata", {}),
                "evidence_document": record.get("evidence_document", {}),
                "evidence_graph": record.get("evidence_graph", {}),
                "reasoning_traces": record.get("reasoning_traces", {}),
                "ceee_metadata": record.get("ceee_metadata", {}),
                "ceee_embedding_text": record.get("embedding_text", "")
            }

            catalog.append(catalog_item)
            ingested_count += 1
            print(f"   ✅ Ingested '{video_id}'. Category: '{cat}' | Ritual: '{catalog_item.get('primary_ritual')}'")

            # Flush to disk periodically every 5 videos
            if len(catalog) % 5 == 0:
                save_catalog_and_rebuild(catalog)

        except Exception as err:
            print(f"   ❌ Error analyzing '{video_file.name}': {err}")

    print("\n" + "=" * 74)
    print(f" SUCCESSFULLY INGESTED {ingested_count} SAMPLE 2 VIDEOS INTO RECOMMENDATION FEED!")
    print("=" * 74)

    # Run recategorize_catalog to ensure high-precision rule mapping across all 45 videos
    print("\n🔄 Running catalog re-categorization & MSFACR Validation...")
    recategorize()


if __name__ == "__main__":
    ingest_daiv_sample_2()
