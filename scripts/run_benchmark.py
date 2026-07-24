import os
import sys
import json
from pathlib import Path

# Setup project root path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from src.content_intelligence.database import IntelligenceDatabase

# Expected semantic profiles for validation dataset
EXPECTED_PROFILES = {
    "video_ci_validation_aditi_atul_jadhav": {
        "category": "Entertainment",
        "mood": "Nervous",
        "language": "English",
        "concepts": ["performer", "performance", "nervous", "audition", "beautiful", "speech"]
    },
    "video_ci_validation_anjali__jarad": {
        "category": "Entertainment",
        "mood": "Relaxing",
        "language": "English",
        "concepts": ["swami", "samarita", "vlog", "kissing", "person"]
    },
    "video_ci_validation_poonam_goswami": {
        "category": "Entertainment",
        "mood": "Normal",
        "language": "English",
        "concepts": ["cooking", "tutorial", "cake", "decorating", "baking", "kitchen", "person"]
    },
    "video_ci_validation_s.laxmi": {
        "category": "Music",
        "mood": "Playful",
        "language": "English",
        "concepts": ["singer", "performance", "music", "dialogue", "reel"]
    },
    "video_ci_validation_soulfulraveli": {
        "category": "Devotion",
        "mood": "Spiritual",
        "language": "English",
        "concepts": ["sacred", "ritual", "devotion", "temple", "spiritual"]
    },
    "video_ci_validation_iamshwetagopal": {
        "category": "Devotion",
        "mood": "Spiritual",
        "language": "Hindi",
        "concepts": ["lalita", "devotion", "sacred", "mantra", "celebration", "temple", "goddess"]
    }
}

def calculate_match(expected, generated):
    # Category Match (25% weight)
    cat_match = 1.0 if expected["category"].lower() in generated.get("category", "").lower() else 0.0
    
    # Mood Match (20% weight)
    mood_match = 0.0
    gen_mood = generated.get("mood", "").lower()
    for m in expected["mood"].lower().split("/"):
        if m in gen_mood:
            mood_match = 1.0
            break
            
    # Language Match (15% weight)
    lang_match = 1.0 if expected["language"].lower() in generated.get("language", "").lower() else 0.0
    
    # Keyword/Concept Overlap Match (40% weight)
    # Search inside tags, keywords, embedding_text, title, and summary
    search_haystack = " ".join(
        generated.get("tags", []) + 
        generated.get("keywords", []) + 
        [generated.get("title", ""), generated.get("summary", ""), generated.get("embedding_text", ""), generated.get("category", ""), generated.get("subcategory", "")]
    ).lower()
    
    matched_concepts = []
    for concept in expected["concepts"]:
        if concept in search_haystack:
            matched_concepts.append(concept)
            
    concept_score = len(matched_concepts) / len(expected["concepts"]) if expected["concepts"] else 1.0
    
    overall_score = (cat_match * 0.25) + (mood_match * 0.20) + (lang_match * 0.15) + (concept_score * 0.40)
    
    missing_concepts = [c for c in expected["concepts"] if c not in matched_concepts]
    
    return {
        "score": round(overall_score * 100, 1),
        "cat_match": cat_match > 0,
        "mood_match": mood_match > 0,
        "lang_match": lang_match > 0,
        "concept_score": round(concept_score * 100, 1),
        "matched_concepts": matched_concepts,
        "missing_concepts": missing_concepts
    }

def run_benchmark():
    print("==================================================")
    print("Content Intelligence Automated Benchmark Suite")
    print("==================================================")
    
    db = IntelligenceDatabase()
    
    results = []
    scores = []
    
    for video_id, expected in EXPECTED_PROFILES.items():
        record = db.get_record(video_id)
        if not record:
            print(f"[-] Warning: No processed record found for {video_id}. Skipping.")
            continue
            
        eval_res = calculate_match(expected, record)
        scores.append(eval_res["score"])
        
        results.append({
            "video_id": video_id,
            "title": record.get("title"),
            "expected_category": expected["category"],
            "generated_category": record.get("category"),
            "expected_mood": expected["mood"],
            "generated_mood": record.get("mood"),
            "expected_lang": expected["language"],
            "generated_lang": record.get("language"),
            "match_score": eval_res["score"],
            "matched_concepts": eval_res["matched_concepts"],
            "missing_concepts": eval_res["missing_concepts"]
        })
        
    if not results:
        print("[-] Error: No validation records available. Please run process_validation_dataset.py first.")
        sys.exit(1)
        
    avg_score = round(sum(scores) / len(scores), 1)
    print(f"\n[+] Evaluated {len(results)} videos.")
    print(f"[+] Average System Semantic Match Score: {avg_score}%")
    
    # Save Report Markdown
    report_path = BASE_DIR / "docs" / "benchmark_report.md"
    os.makedirs(report_path.parent, exist_ok=True)
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Content Intelligence System Benchmark Report\n\n")
        f.write(f"**Average System Semantic Match Score: {avg_score}%**\n\n")
        f.write("This report compiles semantic alignment metrics between expected video profiles and generated metadata outputs.\n\n")
        f.write("## Semantic Match Matrix\n\n")
        f.write("| Video ID | Title | Expected Category | Generated Category | Expected Mood | Generated Mood | Match Score | Missing Concepts |\n")
        f.write("| --- | --- | --- | --- | --- | --- | --- | --- |\n")
        for r in results:
            clean_id = r["video_id"].replace("video_ci_validation_", "")
            f.write(f"| {clean_id} | {r['title']} | {r['expected_category']} | {r['generated_category']} | {r['expected_mood']} | {r['generated_mood']} | **{r['match_score']}%** | {', '.join(r['missing_concepts'])} |\n")
            
        f.write("\n## Evaluation Details\n\n")
        for r in results:
            clean_id = r["video_id"].replace("video_ci_validation_", "")
            f.write(f"### Video: {clean_id}\n")
            f.write(f"- **Title**: {r['title']}\n")
            f.write(f"- **Category Match**: Expected `{r['expected_category']}`, Generated `{r['generated_category']}`\n")
            f.write(f"- **Mood Match**: Expected `{r['expected_mood']}`, Generated `{r['generated_mood']}`\n")
            f.write(f"- **Language Match**: Expected `{r['expected_lang']}`, Generated `{r['generated_lang']}`\n")
            f.write(f"- **Matched Concepts**: {', '.join(r['matched_concepts'])}\n")
            f.write(f"- **Missing Concepts**: {', '.join(r['missing_concepts'])}\n\n")
            
    print(f"[+] Detailed Benchmark Report successfully saved to: {report_path}")

if __name__ == "__main__":
    run_benchmark()
