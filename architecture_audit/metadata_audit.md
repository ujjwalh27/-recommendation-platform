# RAIA Task 3: Metadata Usage & Schema Audit

## Overview

This document audits every metadata field currently produced, stored, and consumed across the Recommendation Platform. It evaluates whether each legacy field should be **maintained**, **augmented**, or **replaced** by CMREE's Canonical Metadata schema.

---

## Metadata Field Audit Matrix

| Metadata Field | Where Produced | Where Stored | Where Consumed | CMREE Integration Strategy |
|:---|:---|:---|:---|:---|
| `video_id` | CIP / Upload handler | `enriched_videos.json`, `intelligence_metadata.json`, FAISS `video_ids.npy` | Candidate lookup, FAISS queries, API responses | **KEEP**: Core unique identifier across all services |
| `title` / `caption` | VLM perception / Manual entry | `enriched_videos.json` (`caption`), `intelligence_metadata.json` (`title`) | Display UI, SentenceTransformer embedding input | **AUGMENT**: Supplement with CMREE canonical ritual title |
| `summary` | VLM perception (`SceneUnderstander`) | `intelligence_metadata.json` (`summary`), `enriched_videos.json` (`caption`) | SentenceTransformer embedding input, UI info card | **REPLACE/AUGMENT**: Combine VLM scene summary with CMREE reasoning trace |
| `category` | Hardcoded CLIP / Heuristic mapper | `enriched_videos.json` (`category`), `intelligence_metadata.json` (`category`) | Candidate Generator (`videos_by_category`), `InterestSignal`, Diversity Filter | **REPLACE**: Replace generic `Entertainment` / `People` with CMREE `primary_category` (`Temple Ritual`, `Devotional Music`, etc.) |
| `subcategory` | VLM heuristic string | `intelligence_metadata.json` | Candidate Generator, UI filters | **REPLACE**: Replace generic subcategory with CMREE `ritual_family` (`Abhishekam`, `Aarti`, `Archana`, `Pooja`, `Bhajan`) |
| `tags` / `keywords` | VLM raw string tokens | `enriched_videos.json` (`keywords`), `intelligence_metadata.json` (`keywords`) | SentenceTransformer embedding input, Search API matching | **REPLACE**: Replace raw token list with deduplicated CMREE `keywords` list |
| `objects` | YOLO / VLM perception | `intelligence_metadata.json` (`objects`) | CMREE Entity Resolver | **MAINTAIN AS PROVENANCE**: Keep raw object list as input to CMREE Entity Resolver |
| `scenes` | CLIP perception | `intelligence_metadata.json` (`scenes`) | CMREE Rule Engine | **MAINTAIN AS PROVENANCE**: Keep raw scene labels as input to CMREE Rule Engine |
| `actions` | ActionRecognizer / VLM | `intelligence_metadata.json` (`actions`) | CMREE Rule Engine | **MAINTAIN AS PROVENANCE**: Keep raw action labels as input to CMREE Rule Engine |
| `ocr` / `ocr_text` | EasyOCR detector | `intelligence_metadata.json` (`ocr`) | CMREE Entity Resolver & Rule Engine | **MAINTAIN AS PROVENANCE**: Keep raw OCR text as input to CMREE Entity Resolver |
| `transcript` | Whisper SpeechRecognizer | `intelligence_metadata.json` (`transcript`) | CMREE Entity Resolver & Rule Engine | **MAINTAIN AS PROVENANCE**: Keep raw transcript as input to CMREE Entity Resolver |
| `primary_topic` | Legacy heuristic | `intelligence_metadata.json` | Recommendation Explainer | **REPLACE**: Replace legacy topic string with CMREE `primary_ritual` |
| `primary_ritual` | **CMREE Rule Engine** | `intelligence_metadata.json` (`primary_ritual`) | Candidate Generator, Scorer, Explainer | **CMREE NATIVE**: Direct canonical indexing & ritual-based candidate retrieval |
| `ritual_family` | **CMREE Knowledge Base** | `intelligence_metadata.json` (`ritual_family`) | Diversity Filter, Subcategory matching | **CMREE NATIVE**: Hierarchy grouping for ritual-level candidate retrieval |
| `primary_deity` | **CMREE Entity Resolver** | `intelligence_metadata.json` (`primary_deity`) | Candidate Generator, Scorer, Explainer | **CMREE NATIVE**: Deity affinity matching & deity candidate retrieval |
| `temple` | **CMREE Knowledge Base** | `intelligence_metadata.json` (`temple`) | Search API, Explainer | **CMREE NATIVE**: Temple location indexing & geography-based retrieval |
| `tradition` | **CMREE Knowledge Base** | `intelligence_metadata.json` (`tradition`) | Scorer, User Profile Persona matching | **CMREE NATIVE**: Sampradaya / Tradition alignment scoring (Shaivism, Vaishnavism, etc.) |
| `offerings` | **CMREE Rule Engine** | `intelligence_metadata.json` (`offerings`) | Search API, Feature filters | **CMREE NATIVE**: Offering attributes indexing (Water, Milk, Flowers, Oil Lamp) |
| `cmree_confidence` | **CMREE Confidence Engine** | `intelligence_metadata.json` (`cmree_confidence`) | Quality filtering, PMCLP monitoring queue | **CMREE NATIVE**: Gating low-confidence predictions (<0.60) from recommendation feed |

---

## Key Replacement Directives

1. **Category Normalization**: Existing generic categories (e.g., `Entertainment`, `People`, `General Video`) in `enriched_videos.json` MUST be updated to CMREE `primary_category` (`Temple Ritual`, `Devotional Music`, `Spiritual Discourse`, `Festival Procession`, `Temple Darshan`).
2. **Subcategory Alignment**: Existing subcategories MUST map directly to CMREE `ritual_family` (`Abhishekam`, `Aarti`, `Archana`, `Pooja`, `Bhajan`, `Pravachan`, `Procession`, `Darshan`, `Homa`).
3. **Deity & Ritual Indexing**: `primary_deity` and `primary_ritual` must be exposed as first-class filtering fields in `CandidateGenerator` and `RecommenderService`.
