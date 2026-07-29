# RAIA Task 4: Embedding Generation & Model Audit

## Overview

This document audits how vector embeddings are currently generated, stored, indexed, and updated across the platform. It provides recommendations for replacing legacy generic input strings with **CMREE Canonical Metadata Text Embeddings**.

---

## Current Embedding Pipeline

```
[Raw Video Metadata]
        │
        ▼
Legacy Text Construction:
"caption + tags + category + subcategory"
        │
        ▼
SentenceTransformer("all-MiniLM-L6-v2")
[384-dimensional dense vector]
        │
        ▼
L2 Normalization (faiss.normalize_L2)
        │
        ▼
FAISS Index (models/video.index) & Matrix (datasets/embeddings/video_embeddings.npy)
```

---

## Current Configuration & Specifications

| Dimension | Property / Value | Evaluation / Assessment |
|:---|:---|:---|
| **Embedding Model** | `SentenceTransformer("all-MiniLM-L6-v2")` | Lightweight, fast CPU inference (~15ms/vector), 384 dimensions, strong semantic alignment for short text sentences |
| **Input Text Construction** | `f"{title} {summary} {category} {subcategory} {' '.join(keywords)}"` | **Legacy Weakness**: Often includes uninformative filler words ("Clip video_101", "Entertainment", "General Video") which dilutes domain specificity |
| **Vector Storage** | `datasets/embeddings/video_embeddings.npy` (Numpy array 7,010 x 384) | Fast memory-mapped loading, path-safe loading via `get_path()` |
| **ID Mapping Storage** | `datasets/embeddings/video_ids.npy` (Numpy string array 7,010) | String-normalized video ID map synchronized 1-to-1 with matrix row index |
| **Dynamic Update Strategy** | `FaissSearchService.add_video(video_id, embedding)` | Appends new vectors to `video_embeddings.npy`, `video_ids.npy`, and re-writes `models/video.index` on disk |

---

## Recommended CMREE Canonical Embedding Text Specification

To maximize domain-semantic precision, the embedding input text must be constructed directly from CMREE's Canonical Metadata fields:

### Formula:
$$\text{Canonical Embedding Text} = \text{Category} \parallel \text{Ritual} \parallel \text{Family} \parallel \text{Deity} \parallel \text{Temple} \parallel \text{Offerings} \parallel \text{Tradition} \parallel \text{Keywords} \parallel \text{Summary}$$

### Implementation Template:
```python
def build_cmree_canonical_embedding_text(canonical_doc: dict) -> str:
    category = canonical_doc.get("primary_category", "Temple Ritual")
    ritual = canonical_doc.get("primary_ritual", "Devotional Worship")
    family = canonical_doc.get("ritual_family", "Pooja")
    deity = canonical_doc.get("primary_deity", "Lord Shiva")
    temple = canonical_doc.get("temple") or ""
    tradition = canonical_doc.get("tradition", "")
    offerings = ", ".join(canonical_doc.get("offerings", []))
    keywords = " ".join(canonical_doc.get("keywords", []))
    
    parts = [
        f"Category: {category}",
        f"Ritual: {ritual}",
        f"Ritual Family: {family}",
        f"Deity: {deity}"
    ]
    if temple: parts.append(f"Temple: {temple}")
    if tradition: parts.append(f"Tradition: {tradition}")
    if offerings: parts.append(f"Offerings: {offerings}")
    if keywords: parts.append(f"Keywords: {keywords}")
    
    return " | ".join(parts)
```

### Example Input Transformation:
- **Legacy Input**: `"Clip video_ci_1784804233 - Devotional ceremony Entertainment General Video devotional temple"`
- **CMREE Canonical Input**: `"Category: Temple Ritual | Ritual: Jalabhishekam | Ritual Family: Abhishekam | Deity: Lord Shiva | Temple: Kashi Vishwanath | Tradition: Shaivism | Offerings: Water, Flowers | Keywords: Temple Ritual Jalabhishekam Abhishekam Lord Shiva Shaivism Water"`

### Expected Semantic Impact:
1. **High-Precision Cosine Clustering**: Videos performing the same ritual (`Jalabhishekam`) or dedicated to the same deity (`Lord Shiva`) cluster tight together in vector space ($S_{\cos} \ge 0.88$).
2. **Elimination of Generic Noise**: Removes generic fillers (`Entertainment`, `Clip 101`), preventing irrelevant cross-domain retrieval.
