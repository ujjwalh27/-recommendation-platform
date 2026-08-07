# Metadata Quality & Validation Report

## Validation Suite Execution

Generated automatically by `src/context_experience_engine/reports/validator.py` during catalog recategorization.

---

## Metrics Summary

```json
{
  "catalog_total_videos": 46,
  "completeness": {
    "perceptual_metadata_completeness_pct": 86.96,
    "emotional_metadata_completeness_pct": 86.96,
    "evidence_document_completeness_pct": 86.96,
    "evidence_graph_completeness_pct": 86.96,
    "reasoning_trace_completeness_pct": 86.96
  },
  "confidence_distribution": {
    "average_fused_confidence": 0.87,
    "min_confidence": 0.80,
    "max_confidence": 0.98,
    "confidence_sample_count": 460
  },
  "overall_status": "VALIDATED_PRODUCTION_READY"
}
```

---

## Model Contribution Distribution

| Perception Subsystem | Total Signal Contributions Across Catalog | Contribution Share (%) |
|---|---|---|
| **MiniCPM-V** | 184 | 40.0% |
| **YOLOv11** | 118 | 25.7% |
| **AST Audio** | 72 | 15.7% |
| **Whisper Audio** | 46 | 10.0% |
| **VideoMAE** | 22 | 4.8% |
| **CLIP / OCR** | 18 | 3.9% |
| **Total** | **460** | **100.0%** |
