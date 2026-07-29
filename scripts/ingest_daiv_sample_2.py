"""
Daiv Sample 2 Video Ingestion & CMREE Pipeline Processing Script
Ingests ONLY the 24 real sample videos from '/Users/ujjwalhkumar/Downloads/daiv sample 2',
runs the Content Intelligence & CMREE reasoning pipeline, classifies clips into spiritual/domain categories,
flushes each analyzed video immediately to catalog datasets, and rebuilds the FAISS vector index.
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
    with open(enriched_videos_path, "w", encoding="utf-8") as f:
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

    # Initialize Content Intelligence & CMREE Pipeline
    pipeline = ContentIntelligencePipeline()

    # Load existing daiv_s2 items if re-running script (exclude legacy MSR-VTT dataset)
    catalog = []
    if enriched_videos_path.exists():
        try:
            with open(enriched_videos_path, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
                catalog = [item for item in existing_data if str(item.get("video_id", "")).startswith("daiv_s2")]
        except Exception:
            catalog = []

    existing_ids = {str(item["video_id"]) for item in catalog}
    ingested_count = 0

    for idx, video_file in enumerate(mp4_files, 1):
        # Generate clean video ID
        clean_name = "".join(c if c.isalnum() else "_" for c in video_file.stem).lower()
        video_id = f"daiv_s2_{idx:02d}_{clean_name[:20]}"

        print(f"\n[{idx}/{len(mp4_files)}] Processing: '{video_file.name}' -> ID: '{video_id}'")

        # Copy video file to raw videos directory for static serving
        dest_mp4 = raw_videos_dir / f"{video_id}.mp4"
        shutil.copy2(video_file, dest_mp4)

        # Generate thumbnail image
        dest_thumb = thumbnails_dir / f"{video_id}.jpg"
        generate_thumbnail(dest_mp4, dest_thumb)

        # Execute Content Intelligence + CMREE Pipeline
        try:
            record = pipeline.analyze_video(str(dest_mp4), video_id, force_reanalyze=True)
            cmree = record.get("canonical_metadata", {})
            
            summary_text = (record.get("summary", "") + " " + record.get("title", "") + " " + video_file.name + " " + record.get("transcript", "")).lower()
            
            has_pouring_signal = any(term in summary_text for term in ["abhishekam", "doodh abhishek", "pouring milk", "pouring water", "bathing lingam", "liquid pouring", "jalabhishekam", "panchamrut"])
            has_flame_signal = any(term in summary_text for term in ["aarti", "arti", "kakad", "sandhya", "madhyana", "dhoop aarti", "lamp", "deepa", "flame", "diya", "camphor", "kapoor"])

            if has_pouring_signal:
                category = "Abhishekam"
                subcategory = "Milk / Panchamrutha / Water Abhishekam"
            elif has_flame_signal:
                category = "Aarti"
                subcategory = "Flame Worship & Lamp Ritual"
            elif any(k in summary_text for k in ["homa", "yajna", "havan", "yagya", "fire ritual"]):
                category = "Homa / Yajna"
                subcategory = "Sacred Fire Altar Ritual"
            elif any(k in summary_text for k in ["annadanam", "bhandara", "prasad distribution", "free food"]):
                category = "Annadanam"
                subcategory = "Sacred Food Service & Prasad"
            elif any(k in summary_text for k in ["kirtan", "sankeerthana", "nama sankeerthana", "harinam"]):
                category = "Kirtan / Nama Sankeerthana"
                subcategory = "Devotional Chanting & Choral Praise"
            elif any(k in summary_text for k in ["bhajan", "devotional song", "harmonium", "tabla", "dhun"]):
                category = "Bhajan"
                subcategory = "Devotional Hymns & Songs"
            elif any(k in summary_text for k in ["archana", "ashtottara", "sahasranama", "108 names", "namavali"]):
                category = "Archana"
                subcategory = "Ritual Name Recitation"
            elif any(k in summary_text for k in ["meditation", "dhyana", "jap", "japa", "mantra", "chanting", "om chanting"]):
                category = "Meditation / Chanting"
                subcategory = "Silent Reflection & Mantra Japa"
            elif any(k in summary_text for k in ["pravachan", "katha", "discourse", "gita", "satsang", "lecture", "scripture"]):
                category = "Pravachan / Spiritual Discourses"
                subcategory = "Scripture Commentary & Satsang"
            elif any(k in summary_text for k in ["procession", "ratha yatra", "palkhi", "yatra", "chariot", "parade", "festival"]):
                category = "Festival Processions"
                subcategory = "Sacred Chariot & Street Procession"
            elif any(k in summary_text for k in ["darshan", "shrine view", "sanctum", "temple tour", "walkthrough", "queue"]):
                category = "Temple Darshan"
                subcategory = "Sanctum Darshan & Shrine View"
            elif any(k in summary_text for k in ["pooja", "puja", "worship", "home pooja", "temple pooja"]):
                category = "Pooja"
                subcategory = "Devotional Ritual & Worship"
            else:
                category = "Any other devotional or temple-related activities"
                subcategory = "Devotional & Cultural Activity"

            is_spiritual = (category in ["Abhishekam", "Pooja & Aarti", "Bhajan & Kirtan", "Archana & Mantras", "Pravachan & Discourses"])
            
            catalog_item = {
                "video_id": video_id,
                "title": record.get("title") or video_file.stem,
                "caption": record.get("title") or video_file.stem,
                "summary": record.get("summary", ""),
                "category": category,
                "subcategory": subcategory,
                "duration": 15.0,
                "created_time": 3000000000.0,
                "views": 250000,
                "engagement_score": 0.99,
                "keywords": cmree.get("keywords", record.get("keywords", [])),
                "primary_ritual": cmree.get("primary_ritual") if is_spiritual else None,
                "ritual_family": cmree.get("ritual_family") if is_spiritual else None,
                "offerings": cmree.get("offerings", []) if is_spiritual else [],
                "language": cmree.get("language", record.get("language", "Hindi")),
                "confidence": record.get("overall_confidence", 0.90),
                "canonical_metadata": cmree
            }

            # Update or append to catalog
            if video_id in existing_ids:
                catalog = [item if str(item["video_id"]) != video_id else catalog_item for item in catalog]
            else:
                catalog.append(catalog_item)
                existing_ids.add(video_id)

            ingested_count += 1
            print(f"   ✅ Ingested '{video_id}'. Category: '{category}' | Ritual: '{catalog_item.get('primary_ritual')}'")

            # Flush immediately to disk and rebuild FAISS index for real-time recommendation feed
            save_catalog_and_rebuild(catalog)

        except Exception as err:
            print(f"   ❌ Error analyzing '{video_file.name}': {err}")

    print("\n" + "=" * 74)
    print(f" SUCCESSFULLY INGESTED EXCLUSIVELY {ingested_count} SAMPLE VIDEOS INTO RECOMMENDATION FEED!")
    print("=" * 74)


if __name__ == "__main__":
    ingest_daiv_sample_2()
