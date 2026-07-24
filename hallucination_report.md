# Large-Scale Hallucination Benchmark Report

## 1. Executive Summary
Evaluating the production pipeline across 100 diverse benchmark videos measured a **1.53% overall hallucination rate**, down from **18.4%** in legacy text-only baseline systems.

## 2. Statement Classification Distribution

| Statement Classification Category | Count | Percentage |
| :--- | :--- | :--- |
| **Directly Observed (Vision)** | 540 | 63.53% |
| **Supported by Speech (Whisper)** | 160 | 18.82% |
| **Supported by OCR (Screen Text)** | 85 | 10.00% |
| **Logically Inferred** | 52 | 6.12% |
| **Hallucinated / Unsupported** | 13 | **1.53%** |

## 3. Top Hallucination Examples & Mitigations
- **Example 1**: Model inferred *"Diwali Celebration"* from marigold flowers in a non-festival home worship.
  - *Mitigation*: Enforce strict prompt policy — festivals must be supported by speech/OCR text cues.
- **Example 2**: Model inferred *"Professional Kitchen Studio"* in a home cooking vlog clip.
  - *Mitigation*: Ground environment labels strictly in detected background items.
