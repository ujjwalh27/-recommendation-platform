# VLM-CEF: Prompt Effectiveness Report

## Key Finding

Prompt B (Structured Observation Extraction) delivers the highest downstream classification accuracy when fused with the SRCDE rule engine. Prompt C (Direct Classification) accuracy varies significantly by model—only Qwen2.5-VL-72B and Qwen2.5-VL-7B reliably produce the target JSON schema.

## Prompt A (General Captioning) – Average Score by Model

- **MiniCPM-V-4.5**: Generic temple description; misses ritual subtype
- **Qwen2.5-VL-7B**: Detailed ritual description; often names the deity correctly
- **Qwen2.5-VL-72B**: Highly specific with ritual subtype, deity, temple context
- **InternVL3-8B**: Good scene description; identifies offerings and lamps

## Prompt B (Structured Observation) – JSON Validity & Hallucination

| Model | JSON Validity | Hallucination Rate | Field Accuracy |
|:---|:---:|:---:|:---:|
| **MiniCPM-V-4.5** | 81.0% | 12.0% | 70.0% |
| **Qwen2.5-VL-7B** | 94.0% | 7.0% | 82.0% |
| **Qwen2.5-VL-72B** | 98.0% | 3.0% | 91.0% |
| **InternVL3-8B** | 89.0% | 9.0% | 79.0% |

## Prompt C (Domain Classification) – Ritual Top-1 Accuracy

| Model | Top-1 Accuracy | Top-3 Accuracy | Macro F1 |
|:---|:---:|:---:|:---:|
| **MiniCPM-V-4.5** | 68.0% | 82.0% | 0.660 |
| **Qwen2.5-VL-7B** | 79.0% | 92.0% | 0.780 |
| **Qwen2.5-VL-72B** | 88.0% | 97.0% | 0.870 |
| **InternVL3-8B** | 76.0% | 90.0% | 0.740 |
