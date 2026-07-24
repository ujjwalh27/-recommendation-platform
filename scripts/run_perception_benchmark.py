import os
import sys
import json

# Add project root to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.explainable_reasoning import ExplainableReasoningEngine
from src.utils.pipeline_inspector import PipelineInspector

def run_perception_benchmark():
    print("=========================================================================")
    print("       PHASE 6: PRODUCTION-GRADE PERCEPTION UPGRADE BENCHMARK RUN        ")
    print("=========================================================================")

    test_video = "/Users/ujjwalhkumar/Downloads/daiv sample/Aditi Atul Jadhav.mp4"
    if not os.path.exists(test_video):
        print(f"Error: Test video not found at {test_video}")
        sys.exit(1)

    engine = ExplainableReasoningEngine()
    video_id = "phase6_perception_benchmark_aditi"

    print("\n[Executing Phase 6 Upgraded Perception Pipeline...]")
    res = engine.process_video_with_explainability(test_video, video_id)
    metadata = res["metadata_view"]

    print("\n=========================================================================")
    print("                   PHASE 6 EVALUATION SUMMARY OUTPUT                     ")
    print("=========================================================================")
    print(f"Video ID:            {res['video_id']}")
    print(f"Projected Category:  {metadata['category']} ({metadata['subcategory']})")
    print(f"Projected Title:     {metadata['title']}")
    print(f"Projected Summary:   {metadata['summary']}")
    print(f"Primary Topic:       {metadata['primary_topic']}")
    print(f"Target Audience:     {metadata['target_audience']}")
    print(f"Keywords:            {metadata['keywords']}")

    print("\n=== VERIFYING EVIDENCE TRACEABILITY LINKS IN CLAIMS ===")
    for idx, claim in enumerate(res["claims"]):
        ev = claim["supporting_evidence"]
        print(f"Claim {idx+1}: '{claim['claim_text']}'")
        print(f"  -> Linked Frames:      {ev['frame_ids']}")
        print(f"  -> Linked Transcripts: {ev['transcript_segments']}")
        print(f"  -> Linked OCR Tokens:  {ev['ocr_tokens']}")
        print(f"  -> Linked YOLO Labels: {ev['detected_objects']}")

    print("\n=========================================================================")
    print("Benchmark execution finished successfully.")
    print("=========================================================================")

if __name__ == "__main__":
    run_perception_benchmark()
