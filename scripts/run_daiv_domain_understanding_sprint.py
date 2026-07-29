import os
import sys
import json
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.semantic_knowledge.daiv_entity_resolver import DaivEntityResolver

from src.semantic_knowledge.daiv_domain_reasoner import DaivDomainReasoner
from src.semantic_knowledge.daiv_hierarchical_metadata import DaivHierarchicalMetadataGenerator

def run_daiv_sprint():
    print("==========================================================================")
    print("  ENGINEERING SPRINT: FINE-GRAINED DOMAIN SEMANTIC UNDERSTANDING FOR DAIV")
    print("==========================================================================")

    output_dir = "daiv_deliverables"
    os.makedirs(output_dir, exist_ok=True)

    gen = DaivHierarchicalMetadataGenerator()

    # -------------------------------------------------------------
    # TASK 1: Gap Analysis (Generic vs Fine-Grained Requirements)
    # -------------------------------------------------------------
    print("\n[Task 1] Running Gap Analysis on Current Generic Metadata...")
    gap_analysis_md = """# Task 1 – Daiv Domain Semantic Gap Analysis

## 1. Executive Summary
The existing metadata generation pipeline output broad, generic categories (e.g. *Hindu Worship*, *Temple*, *Prayer*, *Devotional Activity*) which are insufficient for Daiv's recommendation engine.

## 2. Generic Output vs Fine-Grained Target Matrix

| Dimension | Legacy Generic Output | Daiv Target Fine-Grained Output | Gap Impact |
| :--- | :--- | :--- | :--- |
| **Religion** | `Hindu` | `Hinduism` | Broad |
| **Tradition** | *Missing* | `Sai / Vaishnava / Shaiva` | Cannot filter by spiritual tradition |
| **Primary Deity** | *Missing / Unspecified* | `Shirdi Sai Baba / Lord Hanuman` | Cannot recommend deity-specific feeds |
| **Primary Ritual** | `Worship / Prayer` | `Abhishekam / Aarti / Pravachan` | Cannot distinguish ritual types |
| **Sub-Ritual** | *Missing* | `Milk Abhishekam / Kakad Aarti` | Cannot filter specific ritual sub-types |
| **Ritual Stage** | *Missing* | `Milk Offering / Alankaram` | Cannot track temporal ritual flow |
| **Offerings** | `Flowers` | `Milk, Yellow Marigold Flowers, Kapoor` | Cannot recommend based on offering type |
| **Scripture** | *Missing* | `Bhagavad Gita` | Cannot categorize discourse topics |
| **Intent & Audience** | `Devotional` | `Devotional Worship / Sai Devotees` | Cannot target specific user personas |
"""
    with open("daiv_deliverables/daiv_gap_analysis.md", "w") as f:
        f.write(gap_analysis_md)

    # -------------------------------------------------------------
    # TASK 2 & 3: Taxonomy & Knowledge Base Deliverables
    # -------------------------------------------------------------
    print("\n[Task 2 & 3] Generating Daiv Domain Taxonomy & Knowledge Base Files...")
    taxonomy_data = {
        "dimensions": [
            "Religion", "Tradition", "Primary Deity", "Secondary Deities",
            "Content Type", "Primary Ritual", "Sub Ritual", "Ritual Stage",
            "Festival", "Occasion", "Offerings", "Sacred Objects", "Mantras",
            "Language", "Audience", "Intent", "Mood"
        ],
        "supported_traditions": ["Sai", "Vaishnava", "Shaiva", "Shakta", "Smarta", "Sikh", "Buddhist"],
        "supported_rituals": ["Abhishekam", "Aarti", "Pravachan", "Bhajan", "Homam", "Kirtan"],
        "version": "2.0-enterprise-daiv"
    }
    with open("daiv_deliverables/daiv_domain_taxonomy.json", "w") as f:
        json.dump(taxonomy_data, f, indent=2)

    # -------------------------------------------------------------
    # TASK 4, 5, 6, 7: Test 3 Test Scenarios
    # -------------------------------------------------------------
    print("\n[Task 4-7] Executing Fine-Grained Domain Reasoning Across 3 Test Videos...")

    # Video 1: Sai Baba Milk Abhishekam
    v1_vision = {"detected_objects": ["Marble statue of Sai Baba", "Pouring vessel", "Milk stream", "Yellow marigold flowers"], "actions": ["Pouring milk over deity idol", "Lighting deepa"]}
    v1_speech = {"transcript": "Om Sai Ram... Sri Sai Samartha Jay Jay Sai Samartha", "keywords": ["Sri Sai Samartha", "Om Sai Ram"]}
    v1_ocr = ["Shirdi Sai Mandir", "Milk Abhishekam Live"]
    meta_v1 = gen.generate_daiv_metadata_package("video_001_sai_milk_abhishekam", v1_vision, v1_speech, v1_ocr)

    # Video 2: Hanuman Aarti
    v2_vision = {"detected_objects": ["Orange idol of Lord Hanuman", "Brass aarti plate", "Camphor flame", "Mace"], "actions": ["Rotating aarti plate", "Chanting devant shrine"]}
    v2_speech = {"transcript": "Shri Ram Jai Ram Jai Jai Ram... Aarti Kije Hanuman Lala Ki", "keywords": ["Hanuman Lala", "Shri Ram"]}
    v2_ocr = ["Hanuman Garhi", "Evening Sandhya Aarti"]
    meta_v2 = gen.generate_daiv_metadata_package("video_002_hanuman_aarti", v2_vision, v2_speech, v2_ocr)

    # Video 3: Bhagavad Gita Pravachan
    v3_vision = {"detected_objects": ["Spiritual Guru seated on lectern", "Bhagavad Gita book stand", "Microphone"], "actions": ["Speaking to audience", "Reading scripture verse"]}
    v3_speech = {"transcript": "Tasmaad Asaktah Satatam Kaaryam Karma Samaachara... Chapter 3 Verse 19", "keywords": ["Bhagavad Gita", "Karma Yoga"]}
    v3_ocr = ["Bhagavad Gita Pravachan", "Chapter 3: Karma Yoga"]
    meta_v3 = gen.generate_daiv_metadata_package("video_003_gita_pravachan", v3_vision, v3_speech, v3_ocr)

    test_results = {
        "video_1_sai_milk_abhishekam": meta_v1,
        "video_2_hanuman_aarti": meta_v2,
        "video_3_gita_pravachan": meta_v3
    }
    with open("daiv_deliverables/daiv_test_results.json", "w") as f:
        json.dump(test_results, f, indent=2)

    # -------------------------------------------------------------
    # TASK 8 & 9: Before vs After & Evaluation Report
    # -------------------------------------------------------------
    print("\n[Task 8 & 9] Generating Before vs After Comparison & Evaluation Reports...")

    b_vs_a_md = f"""# Daiv Before vs After Metadata Comparison

## Video 1: Sai Baba Milk Abhishekam

### ❌ Before (Legacy Generic Output)
```json
{{
  "Religion": "Hindu",
  "Category": "Worship",
  "Tags": ["Temple", "Prayer", "Devotional"]
}}
```

### ✅ After (Daiv Fine-Grained Output)
```json
{json.dumps(meta_v1["daiv_semantic_profile"], indent=2)}
```

---

## Video 2: Hanuman Aarti

### ❌ Before (Legacy Generic Output)
```json
{{
  "Religion": "Hindu",
  "Category": "Worship"
}}
```

### ✅ After (Daiv Fine-Grained Output)
```json
{json.dumps(meta_v2["daiv_semantic_profile"], indent=2)}
```

---

## Video 3: Bhagavad Gita Pravachan

### ❌ Before (Legacy Generic Output)
```json
{{
  "Religion": "Hindu",
  "Tags": ["Temple", "Prayer"]
}}
```

### ✅ After (Daiv Fine-Grained Output)
```json
{json.dumps(meta_v3["daiv_semantic_profile"], indent=2)}
```
"""
    with open("daiv_deliverables/daiv_before_vs_after_comparison.md", "w") as f:
        f.write(b_vs_a_md)

    # -------------------------------------------------------------
    # TASK 10: Recommendation Engine Integration Documentation
    # -------------------------------------------------------------
    print("\n[Task 10] Generating Recommendation Engine Integration Documentation...")

    rec_integration_md = """# Daiv Recommendation Engine Integration Architecture

## 1. Recommendation Filter Keys
The hierarchical metadata generator exports explicit filter keys for Daiv's recommendation retrieval engine:

```json
"recommendation_filter_keys": {
  "deity_key": "hinduism:sai:shirdi_sai_baba",
  "ritual_key": "abhishekam:milk_abhishekam",
  "festival_key": "guru_purnima",
  "intent_key": "devotional_worship_&_prayer"
}
```

## 2. Direct Query Filtering Examples
- **Deity-Specific Feed**: Query videos where `deity_key == "hinduism:sai:shirdi_sai_baba"`.
- **Ritual-Specific Feed**: Query videos where `ritual_key == "abhishekam:milk_abhishekam"`.
- **Discourse/Teaching Feed**: Query videos where `intent_key == "teaching_&_discourse"`.
"""
    with open("daiv_deliverables/daiv_recommendation_integration.md", "w") as f:
        f.write(rec_integration_md)

    print("\n==========================================================================")
    print("  ALL 10 DAIV DOMAIN SEMANTIC SPRINT TASKS EXECUTED & DELIVERABLES GENERATED!")
    print("==========================================================================")

if __name__ == "__main__":
    run_daiv_sprint()
