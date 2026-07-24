import os
import json
import cv2

def print_audit():
    video_path = "/Users/ujjwalhkumar/Downloads/daiv sample/Aditi Atul Jadhav.mp4"
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = round(cap.get(cv2.CAP_PROP_FPS), 2)
    duration = round(total_frames / (fps or 30.0), 2)
    cap.release()

    print("================ STAGE 1: INPUT VIDEO ================")
    print(f"File Path:    {video_path}")
    print(f"Duration:     {duration} seconds")
    print(f"FPS:          {fps}")
    print(f"Total Frames: {total_frames}")

    print("\n================ STAGE 2: FRAME SAMPLING ================")
    frames_dir = "debug_outputs/02_sampled_frames"
    sampled_frames = sorted(os.listdir(frames_dir)) if os.path.exists(frames_dir) else []
    print(f"Sampled Keyframes ({len(sampled_frames)}):")
    for f in sampled_frames:
        print(f" - {f}")

    print("\n================ STAGE 3: SPEECH RECOGNITION ================")
    # Load Whisper / Speech from evidence object in final report
    final_rep_path = "debug_outputs/19_final_report/final_audit_summary.json"
    if os.path.exists(final_rep_path):
        with open(final_rep_path) as f:
            final_data = json.load(f)
            claims = final_data.get("claims", [])
            transcript = claims[0]["supporting_evidence"]["transcript_segments"] if claims else []
            print(f"Whisper Transcript: {transcript}")

    print("\n================ STAGE 4: OCR TOKENS ================")
    if os.path.exists(final_rep_path):
        with open(final_rep_path) as f:
            final_data = json.load(f)
            claims = final_data.get("claims", [])
            ocr = claims[0]["supporting_evidence"]["ocr_tokens"] if claims else []
            print(f"OCR Tokens: {ocr}")

    print("\n================ STAGE 5: YOLO OBJECT DETECTIONS ================")
    if os.path.exists(final_rep_path):
        with open(final_rep_path) as f:
            final_data = json.load(f)
            claims = final_data.get("claims", [])
            yolo = claims[0]["supporting_evidence"]["detected_objects"] if claims else []
            print(f"YOLO Object Detections: {yolo}")

    print("\n================ STAGE 9: VLM REQUEST / RESPONSE ================")
    vlm_req_file = "debug_outputs/09_vlm/vlm_text_fallback_request.json"
    vlm_res_file = "debug_outputs/09_vlm/vlm_text_fallback_response.json"
    if os.path.exists(vlm_req_file):
        with open(vlm_req_file) as f:
            req_d = json.load(f)
            print(f"Model Name: {req_d.get('model')}")
            print(f"Endpoint:   {req_d.get('url')}")
            print(f"Prompt:     {req_d.get('prompt')[:300]}...")
    if os.path.exists(vlm_res_file):
        with open(vlm_res_file) as f:
            res_d = json.load(f)
            print("Raw Response Content:")
            print(res_d.get("message", {}).get("content"))

    print("\n================ STAGE 11: KNOWLEDGE GRAPH ================")
    kg_path = "datasets/processed/knowledge_graphs/audit_run_aditi_graph.json"
    if os.path.exists(kg_path):
        with open(kg_path) as f:
            kg_d = json.load(f)
            print(f"Nodes ({len(kg_d.get('nodes', []))}):")
            for n in kg_d.get("nodes", []):
                print(f" - [{n.get('id')}] {n.get('name')} ({n.get('type')}) - Source: {n.get('source')}")
            print(f"Edges ({len(kg_d.get('links', []))}):")
            for e in kg_d.get("links", []):
                print(f" - {e.get('source')} --({e.get('predicate', 'RELATED')})--> {e.get('target')}")

    print("\n================ STAGE 12: CLAIMS LAYER ================")
    claims_file = "debug_outputs/14_claims/claims_layer.json"
    if os.path.exists(claims_file):
        with open(claims_file) as f:
            claims_d = json.load(f)
            for c in claims_d:
                print(f"Claim ID: {c.get('claim_id')}")
                print(f"Text:     {c.get('claim_text')}")
                print(f"Evidence: {c.get('supporting_evidence')}")
                print(f"Conf:     {c.get('confidence')}")

    print("\n================ STAGE 13: METADATA PROJECTION ================")
    meta_file = "debug_outputs/12_metadata/metadata_projection.json"
    if os.path.exists(meta_file):
        with open(meta_file) as f:
            meta_d = json.load(f)
            print(f"Title:         {meta_d.get('title')}")
            print(f"Summary:       {meta_d.get('summary')}")
            print(f"Category:      {meta_d.get('category')}")
            print(f"Subcategory:   {meta_d.get('subcategory')}")
            print(f"Primary Topic: {meta_d.get('primary_topic')}")
            print(f"Keywords:      {meta_d.get('keywords')}")

if __name__ == "__main__":
    print_audit()
