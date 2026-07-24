import os
import sys
import time
from pathlib import Path

# Setup project root path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from src.content_intelligence.pipeline import ContentIntelligencePipeline

def process_dataset():
    print("==================================================")
    print("Content Intelligence - Validation Dataset Processing")
    print("==================================================")
    
    video_dir = Path("/Users/ujjwalhkumar/Downloads/daiv sample")
    if not video_dir.exists():
        print(f"[-] Error: Directory {video_dir} not found.")
        sys.exit(1)
        
    videos = sorted(list(video_dir.glob("*.mp4")))
    if not videos:
        print("[-] Error: No .mp4 files found in sample directory.")
        sys.exit(1)
        
    print(f"[+] Found {len(videos)} sample videos to process.")
    
    # Initialize pipeline
    pipeline = ContentIntelligencePipeline()
    
    for idx, video_path in enumerate(videos):
        # Create a clean, unique slug from filename
        clean_name = video_path.stem.split("-")[0].strip().replace(" ", "_")
        video_id = f"video_ci_validation_{clean_name.lower()}"
        
        print(f"\n[+] Processing Video {idx+1}/{len(videos)}: {video_path.name}")
        print(f"    Assigned ID: {video_id}")
        
        t0 = time.time()
        try:
            record = pipeline.analyze_video(str(video_path), video_id, force_reanalyze=True)
            duration = round(time.time() - t0, 2)
            
            print(f"    Success! Title: '{record['title']}'")
            print(f"    Category: {record['category']} | Subcategory: {record['subcategory']}")
            print(f"    Mood: {record['mood']} | Language: {record['language']}")
            print(f"    Confidence: {record['overall_confidence']} | Duration: {duration}s")
        except Exception as e:
            print(f"    [-] Failed to process {video_path.name}: {e}")
            import traceback
            traceback.print_exc()

    print("\n==================================================")
    print("Validation Dataset Processing Complete!")
    print("==================================================")

if __name__ == "__main__":
    process_dataset()
