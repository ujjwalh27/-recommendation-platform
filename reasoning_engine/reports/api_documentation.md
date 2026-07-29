# CMREE API Documentation

## Overview

The **Canonical Metadata Reasoning & Enrichment Engine (CMREE)** exposes REST endpoints via FastAPI in `backend/app.py`.

---

## Endpoints

### 1. Process Observation
- **Endpoint**: `POST /api/reasoning/process`
- **Description**: Converts raw VLM observation JSON into normalized, enriched canonical metadata.
- **Request Body**:
```json
{
  "video_id": "vid_shiva_001",
  "scene": "Devotional ceremony in a temple",
  "actions": ["Pouring Water", "Chanting"],
  "objects": [{"name": "Shiva Linga", "confidence": 0.95}],
  "ocr_text": ["Kashi Vishwanath"],
  "speech_text": "Om Namah Shivaya",
  "language": "Sanskrit",
  "confidence": 0.92
}
```
- **Response**:
```json
{
  "status": "success",
  "canonical_metadata": {
    "video_id": "vid_shiva_001",
    "primary_category": "Temple Ritual",
    "primary_ritual": "Jalabhishekam",
    "ritual_family": "Abhishekam",
    "primary_deity": "Lord Shiva",
    "offerings": ["Water"],
    "language": "Sanskrit",
    "confidence": 0.95,
    "provenance": { ... }
  },
  "validation_issues": []
}
```

---

### 2. Validate Canonical Metadata
- **Endpoint**: `POST /api/reasoning/validate`
- **Description**: Audits canonical metadata documents for missing fields, semantic conflicts, or low confidence.

---

### 3. List Active Reasoning Rules
- **Endpoint**: `GET /api/reasoning/rules`
- **Description**: Returns all active explainable inference rules loaded from `reasoning_rules.yaml`.

---

### 4. Inspect Knowledge Base
- **Endpoint**: `GET /api/reasoning/knowledge-base`
- **Description**: Returns loaded domain knowledge base definitions (Deities, Rituals, Temples, Offerings).
