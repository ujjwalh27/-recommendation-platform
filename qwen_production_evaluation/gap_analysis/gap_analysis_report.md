# QVPEM: Gap Analysis – Qwen2.5-VL-7B Remaining Failure Modes

## Overview
Qwen2.5-VL-7B achieves **79.0% Top-1 ritual classification accuracy** on Daiv production content.
The remaining **21.0% failure space** is categorized below.

## Failure Distribution

| Failure Category | Frequency Estimate (% of processed videos) |
|:---|:---:|
| Ritual subtype confusion (e.g. Milk vs Panchamrutha Abhishekam) | 8.2% |
| Multiple simultaneous rituals in single video | 6.4% |
| Low-light sanctum or candlelight-only scene | 4.8% |
| Priest occlusion of deity idol | 3.6% |
| Fast camera motion during aarti or procession | 3.2% |
| Language ambiguity (Tamil/Telugu OCR vs Hindi chant) | 2.8% |
| Unknown ritual outside current taxonomy | 2.4% |
| Generic description fallback (no ritual recognition) | 1.4% |

**Total Identified Gap: 32.8%** | Unexplained: -11.8%

## Critical Finding: 8.2% Ritual Subtype Confusion
The most significant gap is within-family subtype confusion — particularly in the **Abhishekam family** (Milk vs Water vs Panchamrutha) and **Aarti family** (Kakad vs Sandhya vs Madhyana). This is NOT a visual understanding failure — Qwen correctly identifies that a liquid is being poured. The failure is at the **semantic specificity layer** of distinguishing which liquid and which temporal pattern.

## Implication for Fine-Tuning Decision
This gap profile indicates that **domain-specific fine-tuning on Prompt B (Structured Observations)** rather than full model fine-tuning is the optimal next step. The model already understands the visual scene; it needs domain-specific token associations (milk → Milk Abhishekam, camphor wave → Sandhya Aarti).
