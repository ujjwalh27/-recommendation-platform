# Root Cause Analysis & Engineering Audit Report (Part 13)

This report details the technical diagnosis of why the Video Intelligence Platform produced misaligned semantic outputs (e.g. "Pumpkin Carving" and "Office Desk" for `Aditi Atul Jadhav.mp4`) and why evidence traceability links were empty.

---

## 🔍 Root Cause Findings

### 1. VLM HTTP 400 Failure & Text-Fallback Invalidation
- **Root Cause**: `MultimodalVLMClient` sends an `"images": [base64_string, ...]` field to local Ollama configured with model `qwen2.5:1.5b`. `qwen2.5:1.5b` is a pure text-only LLM in Ollama. Sending base64 images to a text-only model in Ollama causes Ollama's `/api/chat` server to throw an `HTTP 400 Bad Request`.
- **Effect**: Every single VLM visual keyframe query failed with HTTP 400, forcing the system into Text-Only fallback mode for 100% of video runs.

### 2. Noisy Secondary Sensor Noise Propagation
- **Root Cause A (CLIP Limited Scene Candidates)**: `SceneUnderstander` (CLIP) only contained 11 hardcoded labels (`living room`, `city street`, `office desk environment`, `kitchen cooking set`, etc.) and was missing `temple or devotional shrine`, `talking person / selfie reel`, `indoor home / studio`. Unmatched videos were forced into incorrect classes like `Office desk`.
- **Root Cause B (VideoMAE Low Threshold)**: `ActionRecognizer` (VideoMAE) had a low confidence threshold (`> 0.05`), causing low-trust Kinetics-400 predictions (e.g. "carving pumpkin" for hand gestures) to enter the evidence graph.
- **Root Cause C (Reasoning Over-Triggering)**: `SemanticReasoningEngine` triggered "Culinary Cooking Activity" if `bowl` and `food` occurred together without requiring an explicit cooking verb (`cooking` or `recipe` or `kitchen`).

### 3. Evidence Object Disconnect (Empty Evidence Traceability Links)
- **Root Cause**: `VideoIntelligenceOrchestrator.process_video` returned only `metadata`, `hierarchy`, and `report_path`, omitting the `evidence` (`EvidenceGraphSchema`) object.
- **Effect**: SKE and Explainable Reasoning were receiving `VideoPreprocessor` instead, causing `getattr(evidence_obj, "speech", [])` to return `[]`. All claims were generated with empty evidence links (`Linked Transcripts: []`, `Linked OCR Tokens: []`, `Linked YOLO Labels: []`).

---

## 🛠 Fixes Applied & Verified

1. **Evidence Propagation**: Updated `orchestrator.py`, `graph_builder.py`, and `engine.py` to pass the true `EvidenceGraphSchema` object into Claim Layer and SKE.
2. **Sensor Calibration**:
   - Expanded CLIP scene candidates to include `temple or devotional shrine`, `person talking to camera in a reel`, `indoor home room or studio`.
   - Raised VideoMAE confidence threshold to `0.20`.
   - Strict cooking verb requirement in `reasoning.py` and added `Personal Speaking Reel` rule.
3. **Pipeline Inspector**: Implemented `PipelineInspector` to dump all intermediate outputs into 19 structured subfolders inside `debug_outputs/`.
4. **VLM Fallback Prompting**: Added explicit prompt constraints to prevent text fallback from inventing unverified secondary activities.
