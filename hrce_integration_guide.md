# Hierarchical Ritual Classification Engine (HRCE) Integration Guide

## 1. HRCE Output Schema Specification
Every analyzed video produces the following structured JSON metadata payload:

```json
{
  "content_type": "Ritual",
  "primary_class": "Abhishekam",
  "sub_class": "Milk Abhishekam",
  "confidence": 0.96,
  "ranked_candidates": [
    {"class": "Abhishekam", "confidence": 0.96},
    {"class": "Pooja", "confidence": 0.04}
  ],
  "primary_deity": "Shirdi Sai Baba",
  "offerings": ["Milk", "Yellow Marigold Flowers"],
  "temporal_sequence": [
    "Idol Cleaning & Preparation",
    "Milk Abhishekam Pouring",
    "Alankaram (Deity Decoration)",
    "Aarti & Flame Rotation"
  ],
  "evidence": {
    "vision": ["Pouring liquid", "Milk", "Shiva Lingam"],
    "speech": ["Om Namah Shivaya"],
    "ocr": ["Milk Abhishekam Live"],
    "applied_rules": ["Rule-1: Pouring/Milk signal detected -> Boost Abhishekam"]
  }
}
```

## 2. Downstream Recommendation Engine Consumption
- **Category Filter Key**: `content_type == "Ritual"`
- **Primary Ritual Filter Key**: `primary_class == "Abhishekam"`
- **Sub-Class Filter Key**: `sub_class == "Milk Abhishekam"`
- **Offering Recommendation Key**: `offerings CONTAINS "Milk"`
