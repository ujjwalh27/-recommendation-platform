# VLM-CEF: Final Recommendation Report

## Evidence Summary

This evaluation tested 4 Vision-Language Models across 50 videos (30 benchmark + 20 challenge) using 3 standardized prompts and 5 frame sampling strategies.

---

## Recommendation: **Option C – Retain MiniCPM-V for Observation Extraction; Adopt Qwen2.5-VL-7B as the Primary VLM; Pursue Domain-Specific Fine-Tuning for Sub-Class Resolution**

### Justification

#### MiniCPM-V 4.5 (Current)
- Top-1 Ritual Accuracy: **68.0%** — Insufficient for direct production use without SRCDE post-processing.
- Hallucination Rate: **12.0%** — Highest among all evaluated models.
- JSON Validity: **81.0%** — Frequent markdown wrapping of JSON output causes parsing failures.
- **Verdict**: Cannot reliably identify ritual subtypes (e.g. `Milk Abhishekam` vs `Panchamrutha Abhishekam`). Sufficient only as a lightweight visual observation extractor feeding the SRCDE rule engine.

#### Qwen2.5-VL-7B
- Top-1 Ritual Accuracy: **79.0%** — +11 points over current model.
- Hallucination Rate: **7.0%** — Strong improvement.
- JSON Validity: **94.0%** — Reliable structured output.
- Multilingual: Strong Hindi, Sanskrit, Tamil, Telugu, Marathi support — critical for Daiv's Indian language corpus.
- Latency: 2,600ms on CPU — acceptable with GPU acceleration to ~400ms.
- **Verdict**: ✅ **Recommended as primary VLM replacement.** Significantly better ritual discrimination, structured output reliability, and Indian language support than MiniCPM-V 4.5 at manageable hardware cost (16GB GPU).

#### Qwen2.5-VL-72B
- Top-1 Ritual Accuracy: **88.0%** — Best absolute performance.
- Hallucination Rate: **3.0%** — Near-zero hallucination.
- Peak VRAM: **144 GB** — Requires A100-80GB multi-GPU setup.
- **Verdict**: ⚠️ **Not production-feasible at current infrastructure.** Reserve for offline batch annotation of new benchmark videos or fine-tuning teacher model.

#### InternVL3-8B
- Top-1 Ritual Accuracy: **76.0%** — Competitive but below Qwen2.5-VL-7B.
- JSON Validity: **89.0%** — Lower structured output reliability.
- **Verdict**: Viable secondary option; does not offer sufficient advantage over Qwen2.5-VL-7B to justify migration.

---

## Critical Finding: Ritual Subtype Gap

**No evaluated model achieves >88% Top-1 accuracy on the full 12-class subtype taxonomy** (Milk Abhishekam, Panchamrutha Abhishekam, Kakad Aarti, Sandhya Aarti, etc.) using Prompt C alone. The ritual subtype discrimination gap (especially within the Abhishekam family and within Aarti subtypes) exists across all models because:

1. No general-purpose VLM has been trained on Hindu ritual content at this level of granularity.
2. Liquid type (water vs. milk vs. honey) and temporal action sequence (which offering appears in which order) require fine-grained video understanding that static keyframe analysis cannot fully resolve.

---

## Three-Phase Recommended Path Forward

### Phase 1 – Immediate: Replace MiniCPM-V with Qwen2.5-VL-7B (2 weeks)
- Deploy Qwen2.5-VL-7B with Prompt B (Structured Observations) feeding the existing SRCDE pipeline.
- Expected pipeline accuracy improvement: **+11 percentage points** (68% → 79%) without any SRCDE changes.
- Retain the SRCDE classification layer — the VLM provides better raw observations, not direct predictions.

### Phase 2 – Short-Term: Domain Fine-Tuning on DBB Dataset (6-8 weeks)
- Fine-tune Qwen2.5-VL-7B on the 60-video DBB ground-truth dataset using LoRA/QLoRA (fits on a single 24GB GPU).
- Expand to 300+ annotated videos using Qwen2.5-VL-72B offline as annotation assistant.
- Expected accuracy ceiling: **92-95% Top-1** on ritual subtype classification.

### Phase 3 – Medium-Term: Temporal Video Understanding (10-12 weeks)
- Integrate full video clip (not just keyframes) using Qwen2.5-VL's native video input capability.
- This directly addresses the temporal miss failure mode — the primary source of Aarti subtype confusion.

---

## Decision Matrix

| Criterion | MiniCPM-V 4.5 | Qwen2.5-VL-7B | Qwen2.5-VL-72B | InternVL3-8B |
|:---|:---:|:---:|:---:|:---:|
| Ritual Accuracy | ❌ 68% | ✅ 79% | ✅ 88% | ⚠️ 76% |
| Observation Quality | ⚠️ 70% | ✅ 82% | ✅ 91% | ✅ 79% |
| Hallucination Rate | ❌ 12% | ✅ 7% | ✅ 3% | ✅ 9% |
| JSON Reliability | ⚠️ 81% | ✅ 94% | ✅ 98% | ⚠️ 89% |
| Indian Language Support | ❌ Weak | ✅ Strong | ✅ Excellent | ⚠️ Good |
| Production Feasibility | ✅ 6GB GPU | ✅ 16GB GPU | ❌ 80GB+ | ✅ 16GB GPU |
| **Recommendation** | Replace | **✅ ADOPT** | Future/Fine-tune | Secondary |
