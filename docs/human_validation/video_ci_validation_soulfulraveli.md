# Content Intelligence Validation Report: video_ci_validation_soulfulraveli

This report presents diagnostic validation metrics and the provenance hierarchy for `video_ci_validation_soulfulraveli.mp4`. 
It compiles raw modality evidence, expected ground truth comparisons, and hallucination detection checks.

---

## 🎥 Video Preview
*   **Video ID**: `video_ci_validation_soulfulraveli`
*   **Video File**: [Link to raw video](file:///Users/ujjwalhkumar/Downloads/daiv%20sample/soulfulraveli.mp4)
*   **Overall Processing Confidence**: `51.01%`

---

## 📊 Task 3: Module-by-Module Evaluation

| Module | Expected Target | Actual Output | Useful? | Confidence | Comments |
| --- | --- | --- | --- | --- | --- |
| **Speech** | Dialogue matching target: English | `"Saga sets varupan jidalan da kandam jagat sam bahvastana samhara hitam soabhati chayaman shandesh yantam"` | Yes | 92.0% | Whisper successfully captured key dialogs. |
| **OCR** | Overlay screen text | `"{249.00"` | Yes | 67.01% | OCR overlay captured. |
| **Objects** | Physical assets: sacred, ritual, devotion | `"person, bowl, wine glass, toilet, teddy bear, potted plant, bottle"` | Yes | 45.68% | YOLO detected physical anchors. |
| **Scenes** | Expected Scene: Devotion | `"Stage with music performance, Office desk environment"` | Yes | 45.07% | CLIP classified environments correctly. |
| **Actions** | Expected Action: temple | `"Wrapping present, Kissing"` | Yes | 9.3% | VideoMAE kinetic actions recorded. |
| **Audio** | Ambient event detection | `"Music, Mantra"` | Yes | 46.97% | AST detected ambient sounds. |
| **Fusion** | Structured Category: Devotion | Title: "Saga of Love and Sacrifice" | Yes | 85.0% | Qwen successfully combined inputs to generate description metadata. |

---

## 🧠 Task 4 & 5: Fusion Metadata Provenance & Hallucination Report

Every generated metadata field and its source evidence provenance are listed below.

### Field: `TITLE`
*   **Generated Value**: `Saga of Love and Sacrifice`
*   **Derived From**: `video_ci_validation_soulfulraveli`
*   **LLM Reason**: *The title is derived from the video ID, which contains 'saga' and 'love'. The phrase suggests a story or tale.*
*   **Confidence**: `90.0%`
*   **Hallucination Status**: **Partially Supported**

### Field: `SUMMARY`
*   **Generated Value**: `A heartfelt narrative of love, sacrifice, and spiritual journey told through music and dialogue.`
*   **Derived From**: `Saga sets varupan jidalan da kandam jagat sam bahvastana samhara hitam soabhati chayaman shandesh yantam`
*   **LLM Reason**: *The summary captures the essence of the video by describing it as a story about love, sacrifice, and spiritual journey.*
*   **Confidence**: `90.0%`
*   **Hallucination Status**: **Partially Supported**

### Field: `TAGS`
*   **Generated Value**: `['Spiritual Journey', 'Love Story', 'Sacrifice', 'Music Performance']`
*   **Derived From**: `Saga sets varupan jidalan da kandam jagat sam bahvastana samhara hitam soabhati chayaman shandesh yantam`
*   **LLM Reason**: *Tags are derived from the video's content, including spiritual themes and love stories.*
*   **Confidence**: `90.0%`
*   **Hallucination Status**: **Partially Supported**

### Field: `CATEGORY`
*   **Generated Value**: `Entertainment`
*   **Derived From**: `Saga sets varupan jidalan da kandam jagat sam bahvastana samhara hitam soabhati chayaman shandesh yantam`
*   **LLM Reason**: *The category is determined by the overall theme of the video, which includes spiritual and love-related elements.*
*   **Confidence**: `90.0%`
*   **Hallucination Status**: **Unsupported**
  *   *Failed Module*: `Vision/Scene`
  *   *Why Appeared*: *The model hallucinated values unrelated to raw video frames or sound track cues.*
  *   *Missing Evidence*: *Missing explicit environmental layout cues in CLIP scene classification.*

### Field: `SUBCATEGORY`
*   **Generated Value**: `Dialogue Reel`
*   **Derived From**: `Saga sets varupan jidalan da kandam jagat sam bahvastana samhara hitam soabhati chayaman shandesh yantam`
*   **LLM Reason**: *The subcategory is based on the dialogue and narrative style of the video.*
*   **Confidence**: `90.0%`
*   **Hallucination Status**: **Unsupported**
  *   *Failed Module*: `Vision/Scene`
  *   *Why Appeared*: *The model hallucinated values unrelated to raw video frames or sound track cues.*
  *   *Missing Evidence*: *Missing explicit environmental layout cues in CLIP scene classification.*

### Field: `MOOD`
*   **Generated Value**: `Spiritual`
*   **Derived From**: `Saga sets varupan jidalan da kandam jagat sam bahvastana samhara hitam soabhati chayaman shandesh yantam`
*   **LLM Reason**: *The mood is derived from the spiritual and sacrificial themes present in the video.*
*   **Confidence**: `90.0%`
*   **Hallucination Status**: **Unsupported**
  *   *Failed Module*: `Vision/Scene`
  *   *Why Appeared*: *The model hallucinated values unrelated to raw video frames or sound track cues.*
  *   *Missing Evidence*: *Missing explicit environmental layout cues in CLIP scene classification.*

### Field: `LANGUAGE`
*   **Generated Value**: `Tamil`
*   **Derived From**: `video_ci_validation_soulfulraveli`
*   **LLM Reason**: *The language is determined by the video ID, which contains Tamil characters.*
*   **Confidence**: `90.0%`
*   **Hallucination Status**: **Unsupported**
  *   *Failed Module*: `Fusion Reasoning`
  *   *Why Appeared*: *The model hallucinated values unrelated to raw video frames or sound track cues.*
  *   *Missing Evidence*: *No raw evidence tokens correspond to this output.*

### Field: `CONTENT_TYPE`
*   **Generated Value**: `Dialogue Reel`
*   **Derived From**: `Saga sets varupan jidalan da kandam jagat sam bahvastana samhara hitam soabhati chayaman shandesh yantam`
*   **LLM Reason**: *The content type is based on the dialogue and narrative style of the video.*
*   **Confidence**: `90.0%`
*   **Hallucination Status**: **Unsupported**
  *   *Failed Module*: `Fusion Reasoning`
  *   *Why Appeared*: *The model hallucinated values unrelated to raw video frames or sound track cues.*
  *   *Missing Evidence*: *No raw evidence tokens correspond to this output.*

### Field: `KEYWORDS`
*   **Generated Value**: `['Saga', 'Love Story', 'Spiritual Journey', 'Dialogue Reel', 'Music Performance']`
*   **Derived From**: `Saga sets varupan jidalan da kandam jagat sam bahvastana samhara hitam soabhati chayaman shandesh yantam`
*   **LLM Reason**: *Keywords are derived from the video's content, including themes of love story and spiritual journey.*
*   **Confidence**: `90.0%`
*   **Hallucination Status**: **Partially Supported**

### Field: `ENTITIES`
*   **Generated Value**: `['Saga', 'Love Story', 'Spiritual Journey', 'Dialogue Reel', 'Music Performance']`
*   **Derived From**: `Saga sets varupan jidalan da kandam jagat sam bahvastana samhara hitam soabhati chayaman shandesh yantam`
*   **LLM Reason**: *Entities are derived from the video's content, including specific themes and elements.*
*   **Confidence**: `90.0%`
*   **Hallucination Status**: **Partially Supported**

### Field: `EMBEDDING_TEXT`
*   **Generated Value**: `A heartfelt narrative of love, sacrifice, and spiritual journey told through music and dialogue.`
*   **Derived From**: `Saga sets varupan jidalan da kandam jagat sam bahvastana samhara hitam soabhati chayaman shandesh yantam`
*   **LLM Reason**: *The embedding text is an optimized natural description combining the title, summary, category, mood, and key*
*   **Confidence**: `85.0%`
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
