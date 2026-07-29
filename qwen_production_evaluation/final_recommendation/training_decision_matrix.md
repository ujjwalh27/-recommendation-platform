# QVPEM: Training Decision Matrix

## Evidence-Based Evaluation Result Summary
| Metric | Threshold Required | MiniCPM-V 4.5 | Qwen2.5-VL-7B | Met? |
|:---|:---:|:---:|:---:|:---:|
| Top-1 Ritual Accuracy | ≥ 75% | 68.0% | **79.0%** | ✅ Qwen |
| Metadata Completeness | ≥ 85% | 71.2% | **88.4%** | ✅ Qwen |
| Recommendation Eligibility | ≥ 88% | 74.0% | **91.2%** | ✅ Qwen |
| Human Correction Rate | ≤ 15% | 24.8% | **8.4%** | ✅ Qwen |
| JSON Validity | ≥ 90% | 81.0% | **94.0%** | ✅ Qwen |
| Hallucination Rate | ≤ 10% | 12.0% | **7.0%** | ✅ Qwen |

## Decision Matrix

| Scenario | Evidence | Recommendation |
|:---|:---|:---|
| Qwen meets all quality targets | Top-1=79%, Eligibility=91.2%, Correction=8.4% | **Deploy Qwen2.5-VL-7B immediately without fine-tuning** |
| Qwen improves but subtype gap remains | 8.2% subtype confusion (within-family) | **Deploy Qwen + collect reviewed production examples via DBB** |
| Subtype gap closes with 300+ examples | DBB grows to 300+ reviewed videos | **Initiate LoRA fine-tune on Qwen2.5-VL-7B (Phase 2)** |
| Subtype gap persists after fine-tuning | Evidence from Phase 2 evaluation | **Invest in temporal video clip input (full video vs keyframes)** |

## Immediate Decision: **DEPLOY QWEN2.5-VL-7B**
All 6 quality thresholds are met by Qwen2.5-VL-7B. Fine-tuning is NOT required at this stage.
