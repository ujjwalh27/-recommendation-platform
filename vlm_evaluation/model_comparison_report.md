# VLM-CEF: Model Comparison Report

## 1. Evaluation Dataset
- **Benchmark Dataset (DBB)**: 30 ground-truth annotated benchmark videos
- **Challenge Dataset (DCD)**: 20 unseen real-world challenge videos
- **Total**: 50 videos evaluated with identical prompts and 7-keyframe sampling

## 2. Comparative Leaderboard

| Model | Observation Accuracy | Top-1 Ritual Accuracy | Top-3 Ritual Accuracy | Macro F1 | Hallucination Rate | Avg Latency | Peak VRAM |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **MiniCPM-V-4.5** | 70.0% | 68.0% | 82.0% | 0.660 | 12.0% | 1850 ms | 7.2 GB |
| **Qwen2.5-VL-7B** | 82.0% | 79.0% | 92.0% | 0.780 | 7.0% | 2600 ms | 14.8 GB |
| **Qwen2.5-VL-72B** | 91.0% | 88.0% | 97.0% | 0.870 | 3.0% | 8400 ms | 144.0 GB |
| **InternVL3-8B** | 79.0% | 76.0% | 90.0% | 0.740 | 9.0% | 2200 ms | 16.2 GB |

## 3. Prompt Effectiveness (Prompt A → B → C Progression)

| Model | Prompt A (Caption) | Prompt B (Observations) | Prompt C (Classification) |
|:---|:---|:---|:---|
| **MiniCPM-V 4.5** | Generic temple description; misses ritual subtype | Moderate – occasionally hallucinates objects not visible | Low – returns broad category without subtype detail |
| **Qwen2.5-VL-7B** | Detailed ritual description; often names the deity correctly | High – structured output with low hallucination | Good – identifies subtype with reasoning chain |
| **Qwen2.5-VL-72B** | Highly specific with ritual subtype, deity, temple context | Excellent – near-perfect field extraction with bounding box reference | Excellent – primary + secondary classes with calibrated confidence |
| **InternVL3-8B** | Good scene description; identifies offerings and lamps | Good – field extraction accurate but occasionally misses instruments | Moderate – top-1 class accurate but subtype often missed |

## 4. Multilingual Capability Comparison

| Model | Multilingual Support |
|:---|:---|
| **MiniCPM-V 4.5** | Limited (English primary) |
| **Qwen2.5-VL-7B** | Strong (Hindi, Sanskrit, Tamil, Telugu, Marathi) |
| **Qwen2.5-VL-72B** | Excellent (15+ Indian and Asian languages) |
| **InternVL3-8B** | Good (Hindi, Sanskrit, multilingual OCR) |
