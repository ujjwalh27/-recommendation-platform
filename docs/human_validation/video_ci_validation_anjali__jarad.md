# Content Intelligence Validation Report: video_ci_validation_anjali__jarad

This report presents diagnostic validation metrics and the provenance hierarchy for `video_ci_validation_anjali__jarad.mp4`. 
It compiles raw modality evidence, expected ground truth comparisons, and hallucination detection checks.

---

## 🎥 Video Preview
*   **Video ID**: `video_ci_validation_anjali__jarad`
*   **Video File**: [Link to raw video](file:///Users/ujjwalhkumar/Downloads/daiv%20sample/anjali__jarad.mp4)
*   **Overall Processing Confidence**: `44.98%`

---

## 📊 Task 3: Module-by-Module Evaluation

| Module | Expected Target | Actual Output | Useful? | Confidence | Comments |
| --- | --- | --- | --- | --- | --- |
| **Speech** | Dialogue matching target: English | `"you Shri Swami Samarita, Shri Swami Samarita, Shri Swami Samarita, Shri Swami Samarita,"` | Yes | 92.0% | Whisper successfully captured key dialogs. |
| **OCR** | Overlay screen text | `""` | No | 0.0% | No screen text or failed reading. |
| **Objects** | Physical assets: swami, samarita, vlog | `"person, bowl, teddy bear, orange"` | Yes | 56.32% | YOLO detected physical anchors. |
| **Scenes** | Expected Scene: Entertainment | `"Stage with music performance, Kitchen cooking set, Office desk environment"` | Yes | 31.22% | CLIP classified environments correctly. |
| **Actions** | Expected Action: kissing | `"Kissing"` | Yes | 6.98% | VideoMAE kinetic actions recorded. |
| **Audio** | Ambient event detection | `"Silence, Music"` | Yes | 38.379999999999995% | AST detected ambient sounds. |
| **Fusion** | Structured Category: Entertainment | Title: "Swami Samarita's Devotional Kissing" | Yes | 85.0% | Qwen successfully combined inputs to generate description metadata. |

---

## 🧠 Task 4 & 5: Fusion Metadata Provenance & Hallucination Report

Every generated metadata field and its source evidence provenance are listed below.

### Field: `TITLE`
*   **Generated Value**: `Swami Samarita's Devotional Kissing`
*   **Derived From**: `Video ID: video_ci_validation_anjali__jarad, Transcript (Speech-to-Text): 'you Shri Swami Samarita, Shri Swami Samarita, Shri Swami Samarita, Shri Swami Samarita', Screen OCR text: 'No readable text on-screen', Detected Objects: person, bowl, teddy bear, orange, Detected Environment/Scenes: Stage with music performance, Kitchen cooking set, Office desk environment, Detected Motion/Actions: Kissing`
*   **LLM Reason**: *The video features Swami Samarita performing a devotional act of kissing multiple times.*
*   **Confidence**: `95.0%`
*   **Hallucination Status**: **Supported**

### Field: `SUMMARY`
*   **Generated Value**: `A series of videos showcasing Shri Swami Samarita performing a devotional kiss, likely in a religious or spiritual context.`
*   **Derived From**: `Video ID: video_ci_validation_anjali__jarad, Transcript (Speech-to-Text): 'you Shri Swami Samarita, Shri Swami Samarita, Shri Swami Samarita, Shri Swami Samarita', Screen OCR text: 'No readable text on-screen', Detected Objects: person, bowl, teddy bear, orange, Detected Environment/Scenes: Stage with music performance, Kitchen cooking set, Office desk environment, Detected Motion/Actions: Kissing`
*   **LLM Reason**: *The video content is focused on Swami Samarita performing a devotional kiss in various settings.*
*   **Confidence**: `95.0%`
*   **Hallucination Status**: **Partially Supported**

### Field: `TAGS`
*   **Generated Value**: `['Devotion', 'Religious Rituals', 'Spiritual Practice', 'Kissing Video']`
*   **Derived From**: `Video ID: video_ci_validation_anjali__jarad, Transcript (Speech-to-Text): 'you Shri Swami Samarita, Shri Swami Samarita, Shri Swami Samarita, Shri Swami Samarita', Screen OCR text: 'No readable text on-screen', Detected Objects: person, bowl, teddy bear, orange, Detected Environment/Scenes: Stage with music performance, Kitchen cooking set, Office desk environment, Detected Motion/Actions: Kissing`
*   **LLM Reason**: *Tags are derived from the video's content and context.*
*   **Confidence**: `95.0%`
*   **Hallucination Status**: **Partially Supported**

### Field: `CATEGORY`
*   **Generated Value**: `Devotion`
*   **Derived From**: `Video ID: video_ci_validation_anjali__jarad, Transcript (Speech-to-Text): 'you Shri Swami Samarita, Shri Swami Samarita, Shri Swami Samarita, Shri Swami Samarita', Screen OCR text: 'No readable text on-screen', Detected Objects: person, bowl, teddy bear, orange, Detected Environment/Scenes: Stage with music performance, Kitchen cooking set, Office desk environment, Detected Motion/Actions: Kissing`
*   **LLM Reason**: *The video's content is focused on religious and spiritual activities.*
*   **Confidence**: `95.0%`
*   **Hallucination Status**: **Unsupported**
  *   *Failed Module*: `Vision/Scene`
  *   *Why Appeared*: *The model hallucinated values unrelated to raw video frames or sound track cues.*
  *   *Missing Evidence*: *Missing explicit environmental layout cues in CLIP scene classification.*

### Field: `SUBCATEGORY`
*   **Generated Value**: `Devotional Rituals`
*   **Derived From**: `Video ID: video_ci_validation_anjali__jarad, Transcript (Speech-to-Text): 'you Shri Swami Samarita, Shri Swami Samarita, Shri Swami Samarita, Shri Swami Samarita', Screen OCR text: 'No readable text on-screen', Detected Objects: person, bowl, teddy bear, orange, Detected Environment/Scenes: Stage with music performance, Kitchen cooking set, Office desk environment, Detected Motion/Actions: Kissing`
*   **LLM Reason**: *The video's content is specifically about a devotional ritual involving kissing.*
*   **Confidence**: `95.0%`
*   **Hallucination Status**: **Unsupported**
  *   *Failed Module*: `Vision/Scene`
  *   *Why Appeared*: *The model hallucinated values unrelated to raw video frames or sound track cues.*
  *   *Missing Evidence*: *Missing explicit environmental layout cues in CLIP scene classification.*

### Field: `MOOD`
*   **Generated Value**: `Spiritual`
*   **Derived From**: `Video ID: video_ci_validation_anjali__jarad, Transcript (Speech-to-Text): 'you Shri Swami Samarita, Shri Swami Samarita, Shri Swami Samarita, Shri Swami Samarita', Screen OCR text: 'No readable text on-screen', Detected Objects: person, bowl, teddy bear, orange, Detected Environment/Scenes: Stage with music performance, Kitchen cooking set, Office desk environment, Detected Motion/Actions: Kissing`
*   **LLM Reason**: *The video's content is focused on religious and spiritual activities.*
*   **Confidence**: `95.0%`
*   **Hallucination Status**: **Unsupported**
  *   *Failed Module*: `Vision/Scene`
  *   *Why Appeared*: *The model hallucinated values unrelated to raw video frames or sound track cues.*
  *   *Missing Evidence*: *Missing explicit environmental layout cues in CLIP scene classification.*

### Field: `LANGUAGE`
*   **Generated Value**: `English`
*   **Derived From**: `Speech`
*   **LLM Reason**: *Inferred from multi-modal inputs.*
*   **Confidence**: `85.0%`
*   **Hallucination Status**: **Unsupported**
  *   *Failed Module*: `Fusion Reasoning`
  *   *Why Appeared*: *The model hallucinated values unrelated to raw video frames or sound track cues.*
  *   *Missing Evidence*: *No raw evidence tokens correspond to this output.*

### Field: `CONTENT_TYPE`
*   **Generated Value**: ``
*   **Derived From**: `Speech`
*   **LLM Reason**: *Recovered from LLM direct key-value fallback.*
*   **Confidence**: `80.0%`
*   **Hallucination Status**: **Supported**

### Field: `KEYWORDS`
*   **Generated Value**: `[]`
*   **Derived From**: `Speech`
*   **LLM Reason**: *Recovered from LLM direct key-value fallback.*
*   **Confidence**: `80.0%`
*   **Hallucination Status**: **Supported**

### Field: `ENTITIES`
*   **Generated Value**: `[]`
*   **Derived From**: `Speech`
*   **LLM Reason**: *Recovered from LLM direct key-value fallback.*
*   **Confidence**: `80.0%`
*   **Hallucination Status**: **Supported**

### Field: `EMBEDDING_TEXT`
*   **Generated Value**: ``
*   **Derived From**: `Speech`
*   **LLM Reason**: *Recovered from LLM direct key-value fallback.*
*   **Confidence**: `80.0%`
*   **Hallucination Status**: **Supported**

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
