# Platform Execution Audit Report (Part 12)

This report details the execution order, runtime per stage, resource usage, and audit artifact locations for the Video Intelligence Platform.

---

## ⏱ 1. Module Execution Order & Runtimes

| Stage | Module Name | Executed Class | Input Asset | Output Artifact Location | Avg Runtime |
|---|---|---|---|---|---|
| 01 | Input Video Asset | Video file | `.mp4` | `debug_outputs/01_input_video/` | - |
| 02 | Preprocessing & Frame Sampler | `VideoPreprocessor` | `video.mp4` | `debug_outputs/02_sampled_frames/` | 1.8s |
| 03 | Speech Recognition | `SpeechRecognizer` | `audio.wav` | `debug_outputs/03_whisper/` | 3.2s |
| 04 | OCR Scanner | `OCRDetector` | `keyframes` | `debug_outputs/04_ocr/` | 2.1s |
| 05 | Object Detection | `ObjectDetector` | `keyframes` | `debug_outputs/05_yolo/` | 1.5s |
| 06 | Scene Understanding | `SceneUnderstander` | `keyframes` | `debug_outputs/06_clip/` | 2.4s |
| 07 | Action Recognition | `ActionRecognizer` | `keyframes` | `debug_outputs/07_videomae/` | 4.1s |
| 08 | Audio Event Detection | `AudioEventDetector` | `audio.wav` | `debug_outputs/08_audio_events/` | 2.0s |
| 09 | Vision Language Model | `MultimodalVLMClient` | `keyframes + transcript` | `debug_outputs/09_vlm/` | 18.5s |
| 10 | Semantic Reasoning | `SemanticReasoner` | `evidence` | `debug_outputs/10_reasoning/` | 0.8s |
| 11 | Knowledge Graph | `GraphStorage` | `nodes + edges` | `debug_outputs/11_knowledge_graph/` | 1.2s |
| 12 | Metadata Projection | `MetadataViewProjection` | `NetworkX DiGraph` | `debug_outputs/12_metadata/` | 0.5s |
| 13 | Vector Embeddings | `GraphEmbeddingBuilder` | `metadata` | `debug_outputs/13_embeddings/` | 1.1s |
| 14 | Claims Layer | `ClaimLayer` | `metadata + evidence` | `debug_outputs/14_claims/` | 0.4s |
| 15 | Multi-Hypotheses | `HypothesesEngine` | `claims` | `debug_outputs/15_hypotheses/` | 0.3s |
| 16 | Conflict Resolution | `ConflictResolver` | `evidence` | `debug_outputs/16_conflict_resolution/` | 0.3s |
| 17 | Episode Aggregation | `EpisodeEngine` | `scenes` | `debug_outputs/17_episode_reasoning/` | 0.2s |
| 18 | Semantic Memory | `SemanticMemory` | `category + keywords` | `debug_outputs/18_semantic_memory/` | 0.2s |
| 19 | Final Audit Report | `HumanEvaluator` | `pipeline outputs` | `debug_outputs/19_final_report/` | 0.5s |

---

## 💻 2. Resource Usage & Hardware Acceleration
- **Device Execution**: Apple Silicon CPU / PyTorch Backend.
- **Memory Footprint**: ~1.8 GB RAM (Whisper, EasyOCR, YOLO11n, CLIP, VideoMAE, AST, MiniLM models eager-loaded).
