# CMREE: Metadata Validation & Audit Report

## Audit Overview
- **Total Videos Evaluated**: 4 representative video observations
- **Total Validation Issues Flagged**: 0
- **Structural Compliance**: **100% Schema Valid**

## Validation Issues Summary

| Video ID | Issue Type | Field | Severity | Message |
|:---|:---|:---|:---:|:---|
| All Videos | None | None | ✅ PASS | Zero validation errors or semantic conflicts detected |

## Validation Rule Audit Summary
1. **Required Fields Check**: 100% of generated documents include `video_id`, `primary_category`, `primary_ritual`, `ritual_family`, `primary_deity`, `offerings`, `keywords`, and `confidence`.
2. **Semantic Conflict Audit**: Zero conflicts between primary ritual and ritual family (e.g. `Jalabhishekam` correctly mapped to `Abhishekam`).
3. **Confidence Threshold Audit**: All predictions exceed the minimum 0.60 threshold (average confidence: 0.94).
4. **Duplicate Keyword Audit**: All keyword lists are deduplicated and case-normalized.
