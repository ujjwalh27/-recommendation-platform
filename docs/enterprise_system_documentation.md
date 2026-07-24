# Enterprise System Technical Documentation (Task 10)

This document provides complete technical documentation for the **Video Intelligence Platform** architecture, operational modules, deployment, developer guide, and troubleshooting.

---

## 🏛 1. Overall System Architecture

The Video Intelligence Platform transforms uploaded video files with **zero manual metadata** into structured machine-understandable Knowledge Graphs, metadata views, MiniLM vector embeddings, and persona recommendations.

```
Uploaded Video (video.mp4)
      ↓
Perception Layer (Whisper, EasyOCR, YOLO11n, CLIP, VideoMAE, AST)
      ↓
Evidence Fusion (UnifiedPerceptionEvidence)
      ↓
Semantic Reasoning & Knowledge Engine (SKE & NetworkX DiGraph)
      ↓
Metadata Projection & Provenance Confidence Engine
      ↓
Graph Embedding Generation (SentenceTransformer all-MiniLM-L6-v2)
      ↓
FAISS Vector Search Index & Recommendation Engine
```

---

## 🛠 2. Core Subsystems

### A. Perception Layer
- **Speech Recognizer**: `Faster-Whisper Large-v3` with multilingual transcription (Hindi/Marathi/English), timestamps, repetition penalty (1.2).
- **OCR Scanner**: `EasyOCR` on keyframes.
- **Object Detection**: `YOLO11n` bounding box detector.
- **Scene Understanding**: `CLIP (openai/clip-vit-base-patch32)` zero-shot classifier.
- **Action Recognizer**: `VideoMAE (MCG-NJU/videomae-base-short-finetuned-kinetics)` with >0.20 confidence threshold filter.
- **Audio Event Detector**: `AST (MIT/ast-finetuned-audioset)` audio spectrogram classifier.

### B. Semantic Knowledge Engine (SKE)
- **Scene Graph Segmentation**: Histograms keyframe sampling & scene node generation.
- **14-Category Entity Extractor**: Multimodal entity detection.
- **Relationship Builder**: Directional Subject-Predicate-Object triples.
- **Domain Ontology**: Extended devotional taxonomy & IS_A concept hierarchy.
- **NetworkX DiGraph Storage**: JSON digraph container exportable to RDF triples.

### C. Explainable AI & Claim Layer
- **Claim Layer**: Claims referencing Frame IDs, Transcripts, OCR Tokens, and Objects.
- **Multi-Hypotheses Engine**: Ranks competing semantic interpretations (H1 vs H2 vs H3).
- **Conflict Resolution Engine**: Explains trusted vs rejected sensor sources.

---

## 🔌 3. API Reference & Health Endpoints
- `GET /health`: Health status & pipeline readiness.
- `GET /feed?user_id=user_1`: Persona recommendations feed.
- `GET /content-intelligence/videos`: Processed videos list.
- `POST /content-intelligence/analyze`: Video processing cascade.

---

## 🚀 4. Deployment & Developer Guide
- **Local Startup**:
  ```bash
  python -m uvicorn backend.app:app --host 0.0.0.0 --port 8000
  cd frontend && npm run dev
  ```
- **Automated Test Suite**:
  ```bash
  python tests/test_enterprise_suite.py
  ```
