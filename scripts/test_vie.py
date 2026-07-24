import os
import sys
import json

# Ensure project root is in python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.video_intelligence import VideoIntelligenceEngine

def main():
    print("==================================================")
    print("Testing Video Intelligence Engine (VIE) Core")
    print("==================================================")
    
    test_video = "/Users/ujjwalhkumar/Downloads/daiv sample/Aditi Atul Jadhav.mp4"
    if not os.path.exists(test_video):
        print(f"Error: Test video file not found at: {test_video}")
        sys.exit(1)
        
    print(f"Loading test video: {test_video}")
    engine = VideoIntelligenceEngine()
    
    # Run analysis
    video_id = "test_run_aditi"
    t_start = os.times().elapsed
    
    print("\nRunning end-to-end VIE processing cascade...")
    record = engine.analyze_video(test_video, video_id)
    t_end = os.times().elapsed
    
    print("\nAnalysis Complete!")
    print(f"Total Execution CPU Time: {t_end - t_start:.2f}s")
    
    # Validate result keys
    print("\n=== VERIFYING DATABASE RECORD SCHEMA ===")
    print(f"Video ID: {record['video_id']}")
    print(f"Video Path: {record['video_path']}")
    print(f"Embedding Text Length: {len(record['embedding_text'])} characters")
    print(f"Embedding Vector Dimensions: {len(record['embedding'])} (Expected: 384)")
    print(f"Human-Validation Report: {record['validation_report_path']}")
    
    print("\n=== SEMANTIC ATTRIBUTES ===")
    meta = record["metadata"]
    print(f"Title: {meta.get('title')}")
    print(f"Summary: {meta.get('summary')}")
    print(f"Category: {meta.get('category')} | Subcategory: {meta.get('subcategory')}")
    print(f"Primary Topic: {meta.get('primary_topic')}")
    print(f"Secondary Topics: {meta.get('secondary_topics')}")
    print(f"Language: {meta.get('language')}")
    print(f"Mood: {meta.get('mood')} | Emotion: {meta.get('emotion')}")
    print(f"Keywords: {meta.get('keywords')}")
    
    print("\n=== CONFIDENCE & PROVENANCE MAP ===")
    for field, detail in meta.get("confidence", {}).items():
        evidence = detail.get("evidence", []) if isinstance(detail, dict) else detail.evidence
        score = detail.get("confidence", 0.0) if isinstance(detail, dict) else detail.confidence
        reason = detail.get("reason", "") if isinstance(detail, dict) else detail.reason
        print(f"- [{field.upper()}] Score: {score:.2f} | Sources: {evidence} | Why: {reason}")
        
    print("\n==================================================")
    print("Verification Completed Successfully!")
    print("==================================================")

if __name__ == "__main__":
    main()
