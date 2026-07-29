# CMREE Confidence Scoring Specification

## Overview

The **CMREE Confidence Engine** assigns mathematically grounded confidence scores ($0.00 \le C \le 1.00$) to every inferred metadata field in the canonical document. Confidence is calculated dynamically based on **multi-modal evidence cross-validation** rather than arbitrary fixed values.

---

## Confidence Formula

$$C_{\text{field}} = w_{\text{base}} \cdot C_{\text{rule\_base}} + w_{\text{modal}} \cdot S_{\text{agreement}} + w_{\text{coverage}} \cdot S_{\text{coverage}}$$

Where:
- $w_{\text{base}} = 0.50$: Base rule match confidence
- $w_{\text{modal}} = 0.30$: Cross-modal agreement score (Vision + Speech + OCR)
- $w_{\text{coverage}} = 0.20$: Property coverage & attribute completeness

---

## Field-Level Confidence Calculation Matrix

| Metadata Field | Base Rule Weight ($0.50$) | Modal Agreement Conditions ($0.30$) | Attribute Completeness ($0.20$) |
|:---|:---|:---|:---|
| `primary_ritual` | Rule base confidence (0.90–0.96) | +0.15 if OCR matches ritual name<br>+0.15 if Speech matches ritual chant | +0.10 if primary offering identified<br>+0.10 if ritual family derived |
| `primary_deity` | Rule base deity confidence | +0.15 if deity symbol visible<br>+0.15 if deity name spoken in transcript | +0.20 if temple location associated |
| `ritual_family` | Inherited from `primary_ritual` | +0.30 if matches KB taxonomy | +0.20 if offerings match family |
| `overall_confidence` | Mean of field confidences | Modal agreement factor | Schema validation compliance |

---

## Threshold Requirements

| Threshold Level | Minimum $C$ Value | Action / Downstream System |
|:---|:---:|:---|
| **High Confidence** | $\ge 0.85$ | Automatically published to Recommendation & Indexing Engine |
| **Moderate Confidence** | $0.60 \le C < 0.85$ | Indexed with review flag for PMCLP monitoring queue |
| **Low Confidence** | $< 0.60$ | Enters Human Review Queue; suppressed from cold-start feed |
