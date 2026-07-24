# Content Intelligence Validation Report: video_ci_validation_iamshwetagopal

This report presents diagnostic validation metrics and the provenance hierarchy for `video_ci_validation_iamshwetagopal.mp4`. 
It compiles raw modality evidence, expected ground truth comparisons, and hallucination detection checks.

---

## 🎥 Video Preview
*   **Video ID**: `video_ci_validation_iamshwetagopal`
*   **Video File**: [Link to raw video](file:///Users/ujjwalhkumar/Downloads/daiv%20sample/iamshwetagopal.mp4)
*   **Overall Processing Confidence**: `44.36%`

---

## 📊 Task 3: Module-by-Module Evaluation

| Module | Expected Target | Actual Output | Useful? | Confidence | Comments |
| --- | --- | --- | --- | --- | --- |
| **Speech** | Dialogue matching target: Hindi | `"Asya shri lalita sahasra namas tu atramala mantrasya bashingya rivati vatarsya ya ha Anush tu chanda ha Shri lalita parami shwet shwet shwet shwet shwet shwet shwet shwuntati shaktihi Shakti kuntati ki lakam Shri Lalita mahatri kurasundali prasada sittik dwarah Chintitaphan Abhapthya Kti Japi Vinayoga Ha Jyanam"` | Yes | 92.0% | Whisper successfully captured key dialogs. |
| **OCR** | Overlay screen text | `""` | No | 0.0% | No screen text or failed reading. |
| **Objects** | Physical assets: lalita, devotion, sacred | `"bowl, cake, dining table, person"` | Yes | 46.01% | YOLO detected physical anchors. |
| **Scenes** | Expected Scene: Devotion | `"Kitchen cooking set, Office desk environment, Stage with music performance"` | Yes | 29.56% | CLIP classified environments correctly. |
| **Actions** | Expected Action: temple | `"Decorating the christmas tree, Knitting, Setting table"` | Yes | 7.359999999999999% | VideoMAE kinetic actions recorded. |
| **Audio** | Ambient event detection | `"Mantra, Music"` | Yes | 46.86% | AST detected ambient sounds. |
| **Fusion** | Structured Category: Devotion | Title: "Lalita Devotion: A Sacred Mantra Performance" | Yes | 85.0% | Qwen successfully combined inputs to generate description metadata. |

---

## 🧠 Task 4 & 5: Fusion Metadata Provenance & Hallucination Report

Every generated metadata field and its source evidence provenance are listed below.

### Field: `TITLE`
*   **Generated Value**: `Lalita Devotion: A Sacred Mantra Performance`
*   **Derived From**: `Video ID, Transcript`
*   **LLM Reason**: *The title is derived from the video's content, focusing on Lalita and a sacred mantra performance.*
*   **Confidence**: `90.0%`
*   **Hallucination Status**: **Supported**

### Field: `SUMMARY`
*   **Generated Value**: `A devotional performance featuring Lalita, a Lakshmi form, with mantras and music.`
*   **Derived From**: `Video ID, Transcript`
*   **LLM Reason**: *The summary captures the essence of the video content based on the provided information.*
*   **Confidence**: `90.0%`
*   **Hallucination Status**: **Partially Supported**

### Field: `TAGS`
*   **Generated Value**: `['Lakshmi Devotion', 'Mantra Performance', 'Sacred Music', 'Devotional Ritual']`
*   **Derived From**: `Transcript`
*   **LLM Reason**: *Tags are derived from the content of the transcript, focusing on Lalita and mantras.*
*   **Confidence**: `90.0%`
*   **Hallucination Status**: **Partially Supported**

### Field: `CATEGORY`
*   **Generated Value**: `Devotion`
*   **Derived From**: `Video ID, Transcript`
*   **LLM Reason**: *The category is determined by the overall theme of the video content.*
*   **Confidence**: `90.0%`
*   **Hallucination Status**: **Unsupported**
  *   *Failed Module*: `Vision/Scene`
  *   *Why Appeared*: *The model hallucinated values unrelated to raw video frames or sound track cues.*
  *   *Missing Evidence*: *Missing explicit environmental layout cues in CLIP scene classification.*

### Field: `SUBCATEGORY`
*   **Generated Value**: `Lakshmi Devotion`
*   **Derived From**: `Tags`
*   **LLM Reason**: *Subcategory is derived from specific tags related to the devotional theme.*
*   **Confidence**: `90.0%`
*   **Hallucination Status**: **Unsupported**
  *   *Failed Module*: `Vision/Scene`
  *   *Why Appeared*: *The model hallucinated values unrelated to raw video frames or sound track cues.*
  *   *Missing Evidence*: *Missing explicit environmental layout cues in CLIP scene classification.*

### Field: `MOOD`
*   **Generated Value**: `Spiritual`
*   **Derived From**: `Transcript`
*   **LLM Reason**: *The mood is inferred from the content of the transcript, focusing on spiritual themes.*
*   **Confidence**: `90.0%`
*   **Hallucination Status**: **Unsupported**
  *   *Failed Module*: `Vision/Scene`
  *   *Why Appeared*: *The model hallucinated values unrelated to raw video frames or sound track cues.*
  *   *Missing Evidence*: *Missing explicit environmental layout cues in CLIP scene classification.*

### Field: `LANGUAGE`
*   **Generated Value**: `Hindi`
*   **Derived From**: `Video ID, Transcript`
*   **LLM Reason**: *Language is determined by the video's title and content, which are in Hindi.*
*   **Confidence**: `90.0%`
*   **Hallucination Status**: **Unsupported**
  *   *Failed Module*: `Fusion Reasoning`
  *   *Why Appeared*: *The model hallucinated values unrelated to raw video frames or sound track cues.*
  *   *Missing Evidence*: *No raw evidence tokens correspond to this output.*

### Field: `CONTENT_TYPE`
*   **Generated Value**: `Devotional Performance`
*   **Derived From**: `Transcript`
*   **LLM Reason**: *Content type is derived from the nature of the performance described in the transcript.*
*   **Confidence**: `90.0%`
*   **Hallucination Status**: **Unsupported**
  *   *Failed Module*: `Fusion Reasoning`
  *   *Why Appeared*: *The model hallucinated values unrelated to raw video frames or sound track cues.*
  *   *Missing Evidence*: *No raw evidence tokens correspond to this output.*

### Field: `KEYWORDS`
*   **Generated Value**: `['Lalita', 'Lakshmi', 'Mantra', 'Music', 'Sacred Devotion']`
*   **Derived From**: `Speech`
*   **LLM Reason**: *Recovered from LLM direct key-value fallback.*
*   **Confidence**: `80.0%`
*   **Hallucination Status**: **Supported**

### Field: `ENTITIES`
*   **Generated Value**: `['Lalita', 'Lakshmi', 'Shri Lalita Parami Shwet Shwet Shwet Shwet Shwet Shwet Shwuntati Shaktihi Shakti Kuntati Ki Lakam Shri Lalita Mahatri Kurasundali Prasada Sittik Dwarah Chintitaphan Abhapthya Kti Japi Vinayoga Ha Jyanam']`
*   **Derived From**: `Speech`
*   **LLM Reason**: *Recovered from LLM direct key-value fallback.*
*   **Confidence**: `80.0%`
*   **Hallucination Status**: **Supported**

### Field: `EMBEDDING_TEXT`
*   **Generated Value**: `A sacred performance featuring Lalita, a Lakshmi form, with mantras and music.`
*   **Derived From**: `Title, Summary, Category`
*   **LLM Reason**: *The embedding text combines the title, summary, category, and key entities for indexing purposes.*
*   **Confidence**: `90.0%`
*   **Hallucination Status**: **Partially Supported**

---

## 📝 Task 6: Human Validation Review

Provide a manual verification review below by editing the checkbox markers.

### Section 1: Modality Inputs
*   [ ] **Correct**  [ ] **Partially Correct**  [ ] **Incorrect**  - Speech Transcription
*   [ ] **Correct**  [ ] **Partially Correct**  [ ] **Incorrect**  - Screen OCR text
*   [ ] **Correct**  [ ] **Partially Correct**  [ ] **Incorrect**  - Object detection
*   [ ] **Correct**  [ ] **Partially Correct**  [ ] **Incorrect**  - Scene classification
*   [ ] **Correct**  [ ] **Partially Correct**  [ ] **Incorrect**  - Action recognition
*   [ ] **Correct**  [ ] **Partially Correct**  [ ] **Incorrect**  - Audio event detection

### Section 2: Generated Metadata
*   [ ] **Correct**  [ ] **Partially Correct**  [ ] **Incorrect**  - Generated Title
*   [ ] **Correct**  [ ] **Partially Correct**  [ ] **Incorrect**  - Generated Summary
*   [ ] **Correct**  [ ] **Partially Correct**  [ ] **Incorrect**  - Generated Tags
*   [ ] **Correct**  [ ] **Partially Correct**  [ ] **Incorrect**  - Generated Category
*   [ ] **Correct**  [ ] **Partially Correct**  [ ] **Incorrect**  - Generated Mood
*   [ ] **Correct**  [ ] **Partially Correct**  [ ] **Incorrect**  - Embedding Text

### Manual Reviewer Comments:
```text
[Enter review notes, quality details, and feedback here]
```
