# 🏛️ DAIV Recommendation Platform: Technical Architecture & Demo Presentation Script

---

## 📌 Executive Summary

The **DAIV Recommendation Platform** is an enterprise-grade, multimodal video intelligence and real-time personalized recommendation system built specifically for devotional, spiritual, and cultural video content. 

The platform bridges the gap between raw video data ingestion and instant personalized delivery by combining state-of-the-art Computer Vision, Audio Processing, Vision-Language Models (VLM), Cross-Modal Reasoning (CMREE), FAISS Vector Indexing, and a Real-Time Dynamic Interest Profile Vector Engine.

---

## 🏗️ 1. End-to-End System Architecture

The end-to-end processing pipeline transforms raw video uploads into live personalized recommendation streams through 7 distinct pipeline stages:

```
  ┌─────────────────────────────────────────────────────────────────────────┐
  │ 1. Content Intelligence Platform (CIP) - Multimodal Feature Extraction  │
  └────────────────────────────────────┬────────────────────────────────────┘
                                       │ Raw Visual/Audio Features
                                       ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │ 2. Cross-Modal Reasoning & Entity Resolution Engine (CMREE)            │
  └────────────────────────────────────┬────────────────────────────────────┘
                                       │ Canonical Metadata & Standardized Category
                                       ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │ 3. Automated Content Publishing & Catalog Synchronization (ACPCS)       │
  └────────────────────────────────────┬────────────────────────────────────┘
                                       │ Idempotent Catalog & FAISS Ingestion
                                       ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │ 4. Semantic Embedding & FAISS Vector Index (384-dim IndexFlatIP)        │
  └────────────────────────────────────┬────────────────────────────────────┘
                                       │ Vector Similarity Search
                                       ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │ 5. Real-Time Recommender Engine (Candidate Generation & Reranking)     │
  └────────────────────────────────────┬────────────────────────────────────┘
                                       │ Filtered & Alternated Candidates
                                       ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │ 6. Dynamic Interest Profile Vector Adaptation & Real-Time Feedback     │
  └────────────────────────────────────┬────────────────────────────────────┘
                                       │ Real-Time Interest Vector Update
                                       ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │ 7. Modern React Web Application (Reels UI & Live Telemetry Panel)       │
  └─────────────────────────────────────────────────────────────────────────┘
```

---

## 🔬 2. Core Modules & Technical Specifications

### Stage 1: Multimodal Content Intelligence Platform (CIP)
Processes video files by extracting 7 representative keyframes and analyzing them concurrently across 5 AI models:
1. **VideoMAE (`MCG-NJU/videomae-base-short-finetuned-kinetics`)**: Action recognition & motion pattern detection (e.g., pouring, waving flame, dancing, singing).
2. **EasyOCR**: Extraction of embedded textual cues, subtitles, and temple signage.
3. **YOLO11 (`yolo11n.pt`)**: Real-time object detection (detecting lamps, idols, flowers, vessels, crowds).
4. **Whisper (`openai/whisper-tiny`)**: Speech-to-text transcription for chant identification (mantra, stotram, bhajan lyrics).
5. **MiniCPM-V (Vision Language Model)**: Fine-grained spatial scene description and ritual contextual analysis.

---

### Stage 2: Cross-Modal Reasoning & Entity Resolution Engine (CMREE)
CMREE resolves sensory signals from Stage 1 into culturally accurate canonical metadata:
- **Taxonomy Enforcement**: Enforces strict mapping into the **13 Canonical Categories**:
  1. `Abhishekam` (Milk, Panchamrutha, Water Abhishekam)
  2. `Aarti` (Kakad, Sandhya, Madhyana, Devotional Flame Worship)
  3. `Pooja` (Home / Shrine Worship)
  4. `Archana` (Ashtottara & Sahasranama Name Recitations)
  5. `Bhajan` (Devotional Songs & Hymns)
  6. `Kirtan / Nama Sankeerthana` (Choral Praise)
  7. `Pravachan / Spiritual Discourses` (Scripture Commentary)
  8. `Homa / Yajna` (Sacred Fire Altar Rituals)
  9. `Temple Darshan` (Sanctum Shrine Views & Walkthroughs)
  10. `Festival Processions` (Sacred Chariot / Ratha Yatra & Street Parades)
  11. `Annadanam` (Sacred Meal & Prasad Distribution)
  12. `Meditation / Chanting` (Mantra Japa & Silent Dhyana)
  13. `Any other devotional or temple-related activities` (*Explicit Fallback*)

- **Ritual Precedence Rules**:
  - **Abhishekam vs. Aarti**: `Abhishekam` requires active liquid pouring (`pouring water`, `pouring milk`, `doodh abhishek`, `bathing lingam`). If liquid pouring is present, `Abhishekam` takes absolute priority.
  - **Aarti Priority**: Flame/lamp/camphor waving triggers `Aarti`.
  - **Offering Guardrails**: `"Milk"` is strictly prohibited as an offering for `Aarti`, `Bhajan`, `Pooja`, and non-Abhishekam categories. `Aarti` offerings are automatically sanitized to `"Camphor & Flame, Flowers"`.

---

### Stage 3 & 4: Catalog Publishing & FAISS Vector Indexing
- **Content Publisher (`publisher.py`)**: Synchronizes newly processed videos into the production catalog idempotently based on SHA-256 content hashes.
- **FAISS Vector Index (`faiss_integration.py`)**: Uses `all-MiniLM-L6-v2` to generate 384-dimensional dense semantic embeddings. Embeddings are indexed in a high-speed FAISS `IndexFlatIP` (Inner Product / Cosine Similarity) index for sub-millisecond candidate retrieval.

---

### Stage 5 & 6: Real-Time Recommender & Interest Profile Vector Engine
- **Interest Profile Vector (`profiler.py`)**: Tracks user preference weights normalized across categories (e.g., Aarti, Abhishekam, Bhajan, Pooja).
- **Gradual Exponential Decay Weight Updates**:
  $$\Delta w = \alpha \times \text{engagement\_weight} \times (1.0 - w_{\text{current}})$$
  Prevents aggressive weight blow-ups when a user likes or watches a video.
- **Feed Diversity & Category Alternation (`diversity.py`)**:
  - Enforces strict consecutive category suppression ($N_{\text{consecutive}} \le 2$).
  - Dynamically adjusts category mix to prevent filter bubbles.

---

## 🎬 3. Presentation & Demo Script

This script is structured for a **10-Minute Technical Demo / Stakeholder Walkthrough**.

```
[Target Audience: Technical Leadership, Product Managers, Engineers]
[Duration: 10 Minutes]
[Presenter Tools Required: Laptop running local DAIV Platform UI (localhost:5173), FastAPI server (localhost:8000), IDE code view]
```

---

### Segment 1: Introduction & Problem Overview (1.5 Mins)

**[SPEAKER CUE: Stand in front of screen displaying DAIV Platform Home UI at `http://localhost:5173`]**

> **Presenter:** "Good morning/afternoon everyone. Today, I am excited to demonstrate the **DAIV Recommendation Platform**—a multimodal AI system designed to solve content discovery for devotional and spiritual video platforms.
> 
> Conventional recommendation systems rely purely on text titles or metadata tags uploaded by users, which are often inaccurate, sparse, or missing entirely. In devotional content, misclassifying an *Aarti* (flame ritual) as an *Abhishekam* (liquid bath), or tagging milk offerings on a singing video, creates a poor user experience.
> 
> DAIV solves this by analyzing raw video frames, audio, and visual actions directly through AI, assigning accurate canonical metadata, and building a real-time personalized feed."

---

### Segment 2: Multimodal Content Intelligence Engine (2.5 Mins)

**[SPEAKER CUE: Navigate browser to the 'Multimodal Intelligence & CMREE' tab in the top navigation bar]**

> **Presenter:** "Let's take a look under the hood at how DAIV processes a raw video file.
> 
> When a video is uploaded or ingested, our **Content Intelligence Platform (CIP)** samples keyframes based on visual scene changes. It passes these keyframes concurrently through 5 specialized models:
> 
> 1. **VideoMAE** for detecting kinetic physical actions like liquid pouring or waving lamps.
> 2. **YOLO11** for detecting sacred objects like brass lamps, flowers, and kalash vessels.
> 3. **Whisper** for transcribing audio chants and mantras.
> 4. **EasyOCR** for reading embedded text or temple signage.
> 5. **MiniCPM Vision Language Model** for high-level semantic scene synthesis.
> 
> Once raw signals are extracted, our **Cross-Modal Reasoning & Entity Resolution Engine (CMREE)** applies cultural domain rules. 
> 
> For example: If active liquid pouring over a Lingam is detected, CMREE classifies the video as **Abhishekam**. If a waving lamp or camphor flame is detected, it is classified as **Aarti**, and offerings are sanitized to *Camphor & Flame*—ensuring milk is never incorrectly listed on flame rituals."

---

### Segment 3: Live Recommendation Feed & Dynamic Interest Profile Vector (3 Mins)

**[SPEAKER CUE: Navigate to 'Real-Time Recommendation Feed' tab. Direct attention to the right sidebar panel showing 'INTEREST PROFILE VECTOR']**

> **Presenter:** "Now let's see how this intelligence powers the **Real-Time Recommendation Feed**.
> 
> On the right side of the screen, you can see the user's **Interest Profile Vector**. Currently, user `user_1` has preference scores distributed across categories like *Pooja & Aarti* (11%) and *Abhishekam* (9%).
> 
> Watch what happens when I interact with the feed:
> 
> *(Presenter clicks the 'Like' heart button on an Abhishekam video)*
> 
> As soon as I click **Like**, the backend instantly recalculates the Interest Profile Vector using a bounded exponential decay formula. Instead of aggressively jumping to 100% and overwhelming the feed, the weight increases smoothly.
> 
> Furthermore, look at the terminal logs in the left panel—you can see **FAISS vector retrieval** re-ranking candidate videos in real-time, fetching fresh candidates matching the updated profile."

---

### Segment 4: Category Alternation & Diversity Guardrails (1.5 Mins)

**[SPEAKER CUE: Scroll down through 3-4 consecutive videos in the reels feed]**

> **Presenter:** "Notice the video progression as we scroll:
> - Video 1: **Abhishekam**
> - Video 2: **Aarti**
> - Video 3: **Bhajan**
> - Video 4: **Festival Processions**
> 
> Notice how the system never shows 3 videos of the exact same category in a row. Our **Diversity Engine** enforces a strict category alternation policy ($N_{\text{consecutive}} \le 2$). This prevents user fatigue and ensures users explore a rich variety of devotional content."

---

### Segment 5: Summary & Q&A (1.5 Mins)

**[SPEAKER CUE: Switch back to Architecture Summary slide or main dashboard view]**

> **Presenter:** "To summarize what we have demonstrated:
> 1. **100% Automated Multimodal Analysis** combining VideoMAE, YOLO11, Whisper, and MiniCPM-V.
> 2. **Cultural Taxonomy & Fallback Enforcement** across 13 standardized devotional categories.
> 3. **Sub-millisecond FAISS Candidate Retrieval** paired with a bounded, real-time Interest Vector engine.
> 4. **Smart Feed Diversity** ensuring zero content repetition and optimal user engagement.
> 
> Thank you for your time. I am now happy to take any questions!"

---

## 🛠️ 4. Quick Execution & Verification Commands

To run the complete system locally for a live demonstration:

```bash
# 1. Start FastAPI Backend Server
uvicorn backend.app:app --host 0.0.0.0 --port 8000

# 2. Start React Vite Frontend Application
cd frontend && npm run dev

# 3. Fast Catalog Re-Categorization & FAISS Index Build
python scripts/recategorize_catalog.py

# 4. Verify Live API Category Feed
python -c "import requests; print(requests.get('http://127.0.0.1:8000/feed?user_id=user_1&limit=100').json())"
```

---
*Report generated and validated for DAIV Devotional Recommendation Platform.*
