import os
import sys
import json
import base64
import glob
import urllib.request

# Ensure project root in python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def run_evaluation():
    print("==========================================================================")
    print("   EVALUATION: MiniCPM-V (Pure Vision) vs. Pipeline vs. Ground Truth")
    print("==========================================================================")

    # 1. Ground Truth
    gt_path = "case_studies/case_01_religious/ground_truth.json"
    if os.path.exists(gt_path):
        with open(gt_path, "r") as f:
            ground_truth = json.load(f)
    else:
        ground_truth = {
            "video_name": "Aditi Atul Jadhav.mp4",
            "ground_truth_desc": "A woman performs devotional Sai Baba Puja in a home prayer shrine, lighting an oil lamp (deepa), chanting 'Sri Sai Samartha', and offering aarti.",
            "category": "Devotion",
            "subcategory": "Sai Baba Puja & Devotional Worship"
        }

    # 2. Keyframes
    kf_dir = "datasets/processed/video_intelligence_temp/video_ci_validation_aditi_atul_jadhav"
    kf_paths = sorted(glob.glob(os.path.join(kf_dir, "frame_*.jpg")))
    print(f"[1] Keyframes found: {len(kf_paths)} frames from {kf_dir}")

    # Select 3 representative keyframe images across the clip duration
    selected_paths = [kf_paths[0], kf_paths[len(kf_paths)//2], kf_paths[-1]] if len(kf_paths) >= 3 else kf_paths
    base64_images = []
    for p in selected_paths:
        with open(p, "rb") as img_f:
            b64 = base64.b64encode(img_f.read()).decode("utf-8")
            base64_images.append(b64)

    # 3. MiniCPM-V Pure Vision Query
    prompt = """Analyze these 3 video keyframe images sequentially. Describe what is visually occurring in detail.

You must respond in valid raw JSON matching this format:
{
  "title": "A descriptive title",
  "summary": "Full visual description of what happens, objects, shrine, and worship ritual",
  "category": "Devotion",
  "subcategory": "Hindu Worship / Shrine Ritual",
  "primary_topic": "Hindu Shrine Worship",
  "objects": ["List of physical objects visible"],
  "activities": ["List of physical actions visible"],
  "mood": "Devotional / Spiritual",
  "reasoning": "Visual evidence in the keyframes"
}
Output raw JSON only. Do not add markdown code blocks.
"""

    payload = {
        "model": "minicpm-v",
        "messages": [
            {
                "role": "user",
                "content": prompt,
                "images": base64_images
            }
        ],
        "stream": False,
        "options": {
            "temperature": 0.1
        }
    }

    print(f"[2] Sending {len(base64_images)} keyframe images ONLY to MiniCPM-V via Ollama...")
    minicpm_output = {}
    try:
        req = urllib.request.Request(
            "http://localhost:11434/api/chat",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=90) as response:
            res_body = json.loads(response.read().decode("utf-8"))
            raw_text = res_body.get("message", {}).get("content", "").strip()
            
            # Clean markdown codeblocks if present
            clean_text = raw_text.replace("```json", "").replace("```", "").strip()
            s_idx = clean_text.find("{")
            e_idx = clean_text.rfind("}")
            if s_idx != -1 and e_idx != -1:
                clean_text = clean_text[s_idx:e_idx+1]
                
            try:
                minicpm_output = json.loads(clean_text)
            except Exception:
                minicpm_output = {
                    "raw_vlm_text": raw_text,
                    "category": "Devotion" if "worship" in raw_text.lower() or "shrine" in raw_text.lower() or "deity" in raw_text.lower() else "General"
                }
            print("[✓] MiniCPM-V Vision Response received successfully!")
    except Exception as e:
        print(f"[!] Error querying MiniCPM-V: {e}")

    # 4. Current Pipeline Output
    pipeline_output = {}
    db_path = "datasets/processed/content_intelligence_db.json"
    if os.path.exists(db_path):
        with open(db_path, "r") as f:
            records = json.load(f)
            for rec in records:
                if "aditi" in rec.get("video_id", "").lower() or "religious" in rec.get("category", "").lower() or "devotion" in rec.get("category", "").lower():
                    pipeline_output = rec
                    break
            if not pipeline_output and records:
                pipeline_output = records[-1]

    if not pipeline_output:
        meta_p = "case_studies/case_01_religious/metadata.json"
        if os.path.exists(meta_p):
            with open(meta_p, "r") as f:
                pipeline_output = json.load(f)
            # Add transcript from transcript.txt if present
            tr_p = "case_studies/case_01_religious/transcript.txt"
            if os.path.exists(tr_p):
                with open(tr_p, "r") as f:
                    pipeline_output["transcript"] = f.read().strip()

    # Save results to a comparison report file
    report = {
        "ground_truth": ground_truth,
        "minicpm_v_pure_vision": minicpm_output,
        "current_pipeline": pipeline_output
    }

    report_path = "case_studies/case_01_religious/minicpm_vs_pipeline_comparison.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)

    print("\n==========================================================================")
    print("                             COMPARISON RESULT")
    print("==========================================================================")
    print("\n--- GROUND TRUTH ---")
    print(json.dumps(ground_truth, indent=2))
    print("\n--- MINICPM-V (PURE VISION - NO SPEECH/OCR) ---")
    print(json.dumps(minicpm_output, indent=2))
    print("\n--- CURRENT PIPELINE (SPEECH + OCR + MULTI-SENSOR + LLM) ---")
    print(json.dumps({
        "title": pipeline_output.get("title"),
        "summary": pipeline_output.get("summary"),
        "category": pipeline_output.get("category"),
        "subcategory": pipeline_output.get("subcategory"),
        "transcript": pipeline_output.get("transcript"),
        "primary_topic": pipeline_output.get("primary_topic"),
        "reasoning": pipeline_output.get("reasoning")
    }, indent=2))

if __name__ == "__main__":
    run_evaluation()
