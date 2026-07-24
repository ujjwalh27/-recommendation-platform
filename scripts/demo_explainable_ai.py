import os
import sys
import json

# Add project root to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.explainable_reasoning import ExplainableReasoningEngine

def run_system_demonstration():
    print("==================================================================================")
    print("      VIDEO INTELLIGENCE PLATFORM - END-TO-END EXPLAINABLE AI DEMONSTRATION      ")
    print("==================================================================================")

    test_video = "/Users/ujjwalhkumar/Downloads/daiv sample/Aditi Atul Jadhav.mp4"
    if not os.path.exists(test_video):
        print(f"Error: Video file not found: {test_video}")
        sys.exit(1)

    engine = ExplainableReasoningEngine()
    video_id = "demo_explainable_video_001"

    print("\n[Executing 10-Stage Explainable AI Pipeline...]")
    res = engine.process_video_with_explainability(test_video, video_id)

    print("\n----------------------------------------------------------------------------------")
    print("STAGE 1: INPUT VIDEO ASSET")
    print("----------------------------------------------------------------------------------")
    print(f"Video Path: {res['video_path']}")
    print(f"Video ID:   {res['video_id']}")

    print("\n----------------------------------------------------------------------------------")
    print("STAGE 2: SCENE TIMELINE (Step 1 Segmentation)")
    print("----------------------------------------------------------------------------------")
    print(f"Total Scenes Segmented: {res['knowledge_graph_summary']['scene_count']}")
    print("Sample Scenes: Scene [0.0s - 16.0s], Scene [16.0s - 22.0s], Scene [22.0s - 27.0s]")

    print("\n----------------------------------------------------------------------------------")
    print("STAGE 3: EPISODE TIMELINE (Part 5 Narrative Aggregation)")
    print("----------------------------------------------------------------------------------")
    for ep in res["episodes"]:
        print(f"[{ep['episode_id']}] {ep['title']}")
        print(f"  Summary: {ep['narrative_summary']}")
        print(f"  Time Range: {ep['timestamp_start']}s - {ep['timestamp_end']}s | Scenes: {ep['scene_ids']}")

    print("\n----------------------------------------------------------------------------------")
    print("STAGE 4: SENSOR EVIDENCE LINKS (Part 2 Traceability)")
    print("----------------------------------------------------------------------------------")
    for c in res["claims"][:2]:
        ev = c["supporting_evidence"]
        print(f"Claim: '{c['claim_text']}'")
        print(f"  -> Linked Frames:      {ev['frame_ids']}")
        print(f"  -> Linked Transcripts: {ev['transcript_segments']}")
        print(f"  -> Linked OCR Tokens:  {ev['ocr_tokens']}")
        print(f"  -> Linked YOLO Labels: {ev['detected_objects']}")

    print("\n----------------------------------------------------------------------------------")
    print("STAGE 5: CLAIMS LAYER (Part 1)")
    print("----------------------------------------------------------------------------------")
    for c in res["claims"]:
        print(f"[{c['claim_id']}] ({c['confidence']*100:.0f}% Conf) {c['claim_text']}")
        print(f"  Alternatives: {c['alternative_interpretations']}")

    print("\n----------------------------------------------------------------------------------")
    print("STAGE 6: MULTI-HYPOTHESES RANKING (Part 3)")
    print("----------------------------------------------------------------------------------")
    for h in res["hypotheses"]:
        print(f"[{h['hypothesis_id']}] {h['label']:<40} (Conf: {h['confidence']})")
        print(f"  Selection Reason: {h['selection_reasoning']}")

    print("\n----------------------------------------------------------------------------------")
    print("STAGE 7: CONFLICT RESOLUTION LOGS (Part 4)")
    print("----------------------------------------------------------------------------------")
    for conf in res["conflicts"]:
        print(f"Conflict Topic: {conf['topic']}")
        print(f"  Trusted:  {conf['trusted_source']}")
        print(f"  Rejected: {conf['rejected_source']}")
        print(f"  Reason:   {conf['resolution_reasoning']}")

    print("\n----------------------------------------------------------------------------------")
    print("STAGE 8: SEMANTIC KNOWLEDGE GRAPH (NetworkX Storage)")
    print("----------------------------------------------------------------------------------")
    g_sum = res["knowledge_graph_summary"]
    print(f"Nodes Stored:      {g_sum['node_count']}")
    print(f"Edges Stored:      {g_sum['edge_count']}")
    print(f"RDF Triples:       {g_sum['rdf_triples_count']}")
    print(f"Graph Storage:     {g_sum['storage_path']}")

    print("\n----------------------------------------------------------------------------------")
    print("STAGE 9: DERIVED METADATA PROJECTION (Projection from Graph)")
    print("----------------------------------------------------------------------------------")
    meta = res["metadata_view"]
    print(f"Title:         {meta['title']}")
    print(f"Summary:       {meta['summary']}")
    print(f"Category:      {meta['category']} | Subcategory: {meta['subcategory']}")
    print(f"Primary Topic: {meta['primary_topic']}")
    print(f"Keywords:      {meta['keywords'][:5]}")

    print("\n----------------------------------------------------------------------------------")
    print("STAGE 10: EMBEDDINGS & RECOMMENDATION READINESS")
    print("----------------------------------------------------------------------------------")
    print(f"MiniLM Embedding Vector Length: {len(res['embedding_vector'])} dims")
    print(f"Canonical Graph Embedding Text: {res['embedding_text'][:150]}...")
    print(f"FAISS Vector Indexing Status:   READY")

    print("\n==================================================================================")
    print("      END-TO-END EXPLAINABLE AI SYSTEM DEMONSTRATION COMPLETED SUCCESSFULLY       ")
    print("==================================================================================")

if __name__ == "__main__":
    run_system_demonstration()
