# CSIEI Task 2: Canonical Semantic Document Builder Specification

## Overview

The **Canonical Semantic Document Builder** transforms raw CMREE canonical metadata dicts into structured, deterministic text documents for vector embedding generation. This eliminates generic description noise ("Clip 101", "Entertainment") and forces the vector embedding to focus exclusively on domain-specific ritual, deity, temple, and offering features.

---

## Canonical Document Template

```
Content Type:
{primary_category}
Primary Ritual:
{primary_ritual}
Ritual Family:
{ritual_family}
Primary Deity:
{primary_deity}
Tradition:
{tradition}
Temple:
{temple}
Offerings:
{offerings}
Language:
{language}
Keywords:
{keywords}
```

---

## Dense Embedding Text String (Tokenizer Optimized)

For Transformer model encoding (SentenceTransformers / E5 / BGE), the builder formats the canonical document into a structured pipe-delimited string:

```
Category: {primary_category} | Primary Ritual: {primary_ritual} | Ritual Family: {ritual_family} | Primary Deity: {primary_deity} | Temple: {temple} | Tradition: {tradition} | Offerings: {offerings} | Keywords: {keywords}
```

---

## Field Inclusion Rules

1. **Required Fields**: `primary_category`, `primary_ritual`, `ritual_family`, `primary_deity`.
2. **Optional Fields**: `temple`, `tradition`, `offerings` (included whenever present).
3. **Exclusion Directive**: Free-form unvalidated visual descriptions, OCR noise, or generic filler tokens are **strictly excluded** from the canonical semantic document.
