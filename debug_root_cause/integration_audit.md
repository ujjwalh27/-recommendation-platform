# Task 10 – Vision-Language Integration Audit

## Exact Component Failure Matrix

| Component | Status | Findings / Empirical Evidence |
| :--- | :--- | :--- |
| **Ollama API Transport** | ✅ **PASSED** | HTTP 200 OK, `images` array correctly base64 encoded and decoded by `minicpm-v`. |
| **Vision Model Capability** | ✅ **PASSED** | `minicpm-v` correctly identifies Ganesha, marigold flowers, oil lamps, altar setup, and woman performing ritual. |
| **Keyframe Selection** | ✅ **PASSED** | 7 keyframes sampled via OpenCV color histogram difference are sharp (Laplacian variance > 200) and clear. |
| **Previous Model (`qwen2.5:1.5b`)** | ❌ **FAILED (ROOT CAUSE #1)** | `qwen2.5:1.5b` is a pure text-only model. Passing images returns HTTP 400, forcing a fallback to text-only mode. |
| **Production System Prompt** | ❌ **FAILED (ROOT CAUSE #2)** | 1200-token prompt with 8 nested dict fields caused Pydantic `ValidationError` crash (`people.0`, `locations.0`, `events.0` expected `str`, received `dict`). |
| **Frontend Log Display** | ❌ **FAILED (ROOT CAUSE #3)** | `[Qwen 2.5]` was hardcoded in `ContentIntelligence.jsx` line 109, displaying incorrect model names in UI logs. |

## Root Cause Verdict
The platform failure was caused by a **combination of Model Incompatibility + Schema Mismatch**:
1. **Model Incompatibility**: The legacy model `qwen2.5:1.5b` is text-only and threw HTTP 400 on image payloads, forcing the pipeline into text-only fallback which generated hallucinated summaries (*"audition monologue in a studio setting"*).
2. **Pydantic Validation Error**: When `minicpm-v` returned structured JSON with dict elements for `people` and `locations`, Pydantic's strict `List[str]` schema raised a runtime 500 exception on `POST /content-intelligence/analyze`.
3. **Hardcoded UI Labels**: `ContentIntelligence.jsx` line 109 printed `[Qwen 2.5]` regardless of the active VLM backend.
