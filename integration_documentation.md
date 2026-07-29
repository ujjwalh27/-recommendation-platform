# SRCDE Integration & System Architecture Documentation

## 1. System Pipeline Transformation
- **Legacy Flow**: Video -> Vision/Speech/OCR -> Evidence Fusion -> Natural Language Summary Paragraph.
- **Target Flow**: Video -> Vision/Speech/OCR -> Evidence Fusion -> Observation Extraction -> Decision Engine -> Hierarchical Classification -> Target JSON Schema.

## 2. Output Schema Standard
Every pipeline execution outputs the standardized JSON schema:

```json
{
  "classification": {
    "content_type": "Ritual",
    "primary_class": "Abhishekam",
    "sub_class": "Water Abhishekam"
  },
  "confidence": 0.94,
  "observations": {
    "people": ["priest"],
    "objects": ["idol", "flowers", "water vessel", "lamp", "bell"],
    "actions": ["pouring water", "offering flowers"],
    "speech": ["Om Namah Shivaya"],
    "ocr": ["Water Abhishekam"]
  },
  "reasoning": [
    "Water vessel poured over deity",
    "Priest performing ritual",
    "Temple environment detected"
  ],
  "alternative_predictions": [
    {"class": "Pooja", "confidence": 0.05},
    {"class": "Archana", "confidence": 0.01}
  ],
  "explanation": "Strong evidence for Abhishekam (Water Abhishekam). Confirmed with 94% confidence."
}
```
