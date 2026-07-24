# Task 12 – Final Engineering Decision & Evidence Answers

### 1. Can the selected model (`minicpm-v`) genuinely understand a single image?
**YES.**
- **Evidence**: `debug_root_cause/minimal_image_test/response.txt`
- **Output**: `minicpm-v` correctly identified Lord Ganesha, marigold flowers in brass bowls, lit oil lamps, copper pots, and the green altar cloth with zero hallucinations.

### 2. Can it understand multiple chronological frames?
**YES, but optimal with 3 frames.**
- **Evidence**: `debug_root_cause/api_responses/task7_multi_image_benchmark.json`
- **Finding**: Passing 3 representative frames (0s, 22s, 43s) provides full visual narrative (altar setup → holding worship plate → offering flowers). Passing 7+ frames increases latency (+14s) without adding semantic richness.

### 3. Is the Ollama integration correct?
**YES.**
- **Evidence**: `debug_root_cause/api_requests/task3_request.json` & `debug_root_cause/api_responses/task4_decoding_response.json`
- **Endpoint**: `http://localhost:11434/api/chat` accepting `{"model": "minicpm-v", "messages": [{"images": ["<b64_string>"]}]}` returns HTTP 200.

### 4. Are keyframes suitable for semantic understanding?
**YES.**
- **Evidence**: `debug_root_cause/keyframe_contact_sheet.png` & Keyframe Metrics
- **Finding**: All 7 keyframes sampled via OpenCV HSV histogram difference have Laplacian sharpness > 200 and high brightness contrast, capturing the complete ritual flow.

### 5. What was the verified root cause of failure?
- **Root Cause 1**: Legacy model `qwen2.5:1.5b` was text-only and threw HTTP 400 on image payloads, forcing text-only fallback hallucinations.
- **Root Cause 2**: `MetadataGenerator` threw a Pydantic `ValidationError` when VLM returned dict items inside `people` / `locations` string lists.
- **Root Cause 3**: Hardcoded `[Qwen 2.5]` strings in `ContentIntelligence.jsx` UI logs.

## Minimal Changes Required & Verified Fixes Applied
1. Upgraded VLM model configuration to `minicpm-v` in `config.py` and `backend/app.py`.
2. Added `_to_str_list()` array sanitizer in `src/video_intelligence/metadata_generator.py`.
3. Updated logger stage text in `frontend/src/features/intelligence/ContentIntelligence.jsx` to `[MiniCPM-V 4.5]`.
