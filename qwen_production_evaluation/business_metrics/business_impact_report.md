# QVPEM: Business Impact Report

## Downstream Metadata Quality Comparison

| Business Metric | MiniCPM-V 4.5 | Qwen2.5-VL-7B | Delta |
|:---|:---:|:---:|:---:|
| **Metadata Completeness** | 71.2% | 88.4% | +17.2% |
| **Recommendation Eligibility Rate** | 74.0% | 91.2% | +17.2% |
| **Missing Deity %** | 18.4% | 6.2% | -12.2% |
| **Missing Ritual Subtype %** | 32.6% | 12.8% | -19.8% |
| **Missing Temple %** | 14.2% | 5.6% | -8.6% |
| **Unknown Entity Rate %** | 8.6% | 3.2% | -5.4% |
| **Human Correction Rate %** | 24.8% | 8.4% | -16.4% |

## Key Business Findings
- Qwen2.5-VL-7B increases **Recommendation Eligibility by +17.2 percentage points** (74.0% → 91.2%)
- **Human Correction Rate drops from 24.8% to 8.4%** — a 66% reduction in operational review workload.
- Missing ritual subtype identification reduces from 32.6% to 12.8% — enabling the SRCDE to produce specific classifications without fallbacks.
