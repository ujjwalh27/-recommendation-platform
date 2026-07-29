# Live VLM Validation (LVV) – Downstream Pipeline Impact Report

## Downstream Metric Comparison (Measured on Real Daiv Content)

| Metric | minicpm-v:latest (Baseline) | qwen2.5:1.5b (Candidate) | Delta |
|:---|:---:|:---:|:---:|
| **JSON Parse Success Rate** | **100.0%** | 0.0% | **+100.0%** |
| **Average Downstream Confidence** | **0.646** | 0.495 | **+0.151** |
| **Recommendation Eligibility %** | **100.0%** | 0.0% | **+100.0%** |
| **Unknown Entity Rate %** | **0.0%** | 100.0% | **-100.0%** |
| **Human Review Workload %** | **0.0%** | 100.0% | **-100.0%** |

---

## Technical Conclusion

The baseline `minicpm-v:latest` model successfully extracts structured JSON metadata that can be directly consumed by the SRCDE rule engine. Candidate lightweight models fail to output valid structured JSON under complex multi-field schema prompts, resulting in empty responses or parse errors.
