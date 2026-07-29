# CMREE Reasoning Trace Examples

## Example 1: Jalabhishekam Water Bath Ritual

```yaml
video_id: "vid_shiva_001"
canonical_metadata:
  primary_ritual: "Jalabhishekam"
  ritual_family: "Abhishekam"
  primary_deity: "Lord Shiva"
  temple: "Kashi Vishwanath"
  confidence: 0.95

reasoning_trace:
  step_1_observation_validation:
    status: "PASS"
    scene: "Devotional ceremony at a temple altar"
    detected_objects: ["Shiva Linga", "Water Vessel", "Marigold Flowers"]
    detected_actions: ["Pouring Water"]
  step_2_entity_resolution:
    resolved_objects:
      - "Lingam" -> "Shiva Linga"
      - "Lota" -> "Water Vessel"
    resolved_deities:
      - "Mahadev" -> "Lord Shiva"
  step_3_rule_evaluation:
    matched_rule: "RULE_001_JALABHISHEKAM"
    explanation: "Shiva Linga object combined with water pouring action confirms Jalabhishekam ritual."
    evidence_points:
      - "✓ Shiva Linga detected"
      - "✓ Water pouring detected"
      - "✓ OCR mentions 'Kashi Vishwanath Abhishek'"
  step_4_enrichment:
    derived_family: "Abhishekam"
    derived_tradition: "Shaivism"
    derived_offerings: ["Water", "Flowers"]
  step_5_confidence_scoring:
    overall_confidence: 0.95
    status: "HIGH_CONFIDENCE"
```

---

## Example 2: Shirdi Sai Kakad Aarti

```yaml
video_id: "vid_sai_004"
canonical_metadata:
  primary_ritual: "Kakad Aarti"
  ritual_family: "Aarti"
  primary_deity: "Shirdi Sai Baba"
  temple: "Shirdi Sai Mandir"
  confidence: 0.96

reasoning_trace:
  step_1_observation_validation:
    status: "PASS"
    scene: "Early morning worship at Shirdi Sai Mandir"
    detected_objects: ["Oil Lamp", "Bell", "Sai Baba Idol"]
    detected_actions: ["Ringing Bell", "Lighting Lamp"]
  step_2_entity_resolution:
    resolved_deities:
      - "Sai Ram" -> "Shirdi Sai Baba"
  step_3_rule_evaluation:
    matched_rule: "RULE_005_KAKAD_AARTI"
    explanation: "Shirdi Sai Baba entity combined with Kakad aarti keywords confirms Kakad Aarti ritual."
    evidence_points:
      - "✓ Shirdi Sai Baba deity identified"
      - "✓ Oil lamp and bell ringing detected"
      - "✓ Audio transcript mentions 'Kakad Aarti'"
  step_4_enrichment:
    derived_family: "Aarti"
    derived_tradition: "Universal Devotional"
    derived_offerings: ["Oil Lamp", "Incense"]
  step_5_confidence_scoring:
    overall_confidence: 0.96
    status: "HIGH_CONFIDENCE"
```
