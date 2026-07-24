import os
import sys
import json

# Add project root to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.explainable_reasoning import ExplainableReasoningEngine
from src.utils.pipeline_inspector import PipelineInspector

def run_audit():
    print("=========================================================================")
    print("       EXPLICIT ENTERPRISE AI PIPELINE AUDIT & DEBUG INSPECTOR RUN       ")
    print("=========================================================================")

    test_video = "/Users/ujjwalhkumar/Downloads/daiv sample/Aditi Atul Jadhav.mp4"
    if not os.path.exists(test_video):
        print(f"Error: Test video not found at {test_video}")
        sys.exit(1)

    inspector = PipelineInspector()
    inspector.dump_stage(1, "video_input_info.json", {
        "video_path": test_video,
        "video_name": os.path.basename(test_video),
        "file_size_bytes": os.path.getsize(test_video)
    })

    engine = ExplainableReasoningEngine()
    video_id = "audit_run_aditi"

    print("\n[Executing Repaired Explainable Pipeline with Inspector active...]")
    res = engine.process_video_with_explainability(test_video, video_id)

    # Dump remaining stages to debug_outputs/
    inspector.dump_stage(11, "networkx_graph_summary.json", res["knowledge_graph_summary"])
    inspector.dump_stage(13, "embedding_info.json", {
        "embedding_text": res["embedding_text"],
        "vector_dims": len(res["embedding_vector"])
    })
    inspector.dump_stage(15, "hypotheses.json", res["hypotheses"])
    inspector.dump_stage(16, "conflicts.json", res["conflicts"])
    inspector.dump_stage(17, "episodes.json", res["episodes"])
    inspector.dump_stage(19, "final_audit_summary.json", res)

    print("\n=========================================================================")
    print("                        AUDIT RUN SUMMARY OUTPUT                         ")
    print("=========================================================================")
    print(f"Video ID:            {res['video_id']}")
    print(f"Projected Category:  {res['metadata_view']['category']} ({res['metadata_view']['subcategory']})")
    print(f"Projected Title:     {res['metadata_view']['title']}")
    print(f"Projected Summary:   {res['metadata_view']['summary']}")
    print(f"Primary Topic:       {res['metadata_view']['primary_topic']}")

    print("\n=== VERIFYING EVIDENCE TRACEABILITY LINKS IN CLAIMS ===")
    for idx, claim in enumerate(res["claims"]):
        ev = claim["supporting_evidence"]
        print(f"Claim {idx+1}: '{claim['claim_text']}'")
        print(f"  -> Linked Frames:      {ev['frame_ids']}")
        print(f"  -> Linked Transcripts: {ev['transcript_segments']}")
        print(f"  -> Linked OCR Tokens:  {ev['ocr_tokens']}")
        print(f"  -> Linked YOLO Labels: {ev['detected_objects']}")

    print("\n=========================================================================")
    print("Pipeline Inspector dumped all raw outputs to 'debug_outputs/' (01 to 19)")
    print("=========================================================================")

if __name__ == "__main__":
    run_audit()
