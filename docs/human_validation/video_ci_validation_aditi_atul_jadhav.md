# Content Intelligence Validation Report: video_ci_validation_aditi_atul_jadhav

This report presents diagnostic validation metrics and the provenance hierarchy for `video_ci_validation_aditi_atul_jadhav.mp4`. 
It compiles raw modality evidence, expected ground truth comparisons, and hallucination detection checks.

---

## 🎥 Video Preview
*   **Video ID**: `video_ci_validation_aditi_atul_jadhav`
*   **Video File**: [Link to raw video](file:///Users/ujjwalhkumar/Downloads/daiv%20sample/aditi_atul_jadhav.mp4)
*   **Overall Processing Confidence**: `44.769999999999996%`

---

## 📊 Task 3: Module-by-Module Evaluation

| Module | Expected Target | Actual Output | Useful? | Confidence | Comments |
| --- | --- | --- | --- | --- | --- |
| **Speech** | Dialogue matching target: English | `"She's so beautiful, she's so beautiful, she's so beautiful, she's so beautiful, she's so beautiful, she's so beautiful, she's so beautiful, she's so beautiful, she's so beautiful, she's so beautiful, she's so beautiful, she's so beautiful, she's so beautiful, she's so beautiful, she's so beautiful, she's so beautiful, she's so beautiful, she's so beautiful, she's so beautiful, she's so beautiful, she's so beautiful, she's so beautiful, she's so beautiful, she's so beautiful, she's so beautiful, she's so beautiful, she's so beautiful, she's so beautiful, she's so beautiful, she's so beautiful, she's so beautiful, she's so beautiful, she's so beautiful, she's so beautiful, she's so beautiful, she's so beautiful, she's so beautiful, she's so beautiful, she's so beautiful, she's so beautiful, she's so beautiful, she's so beautiful, she's so beautiful, she's so beautiful, she's so nervous. I'm so nervous. I'm so nervous. I'm so nervous. I'm so nervous. I'm so nervous. I'm so nervous. I'm so nervous. I'm so nervous. I'm so nervous. I'm so nervous. I'm so nervous. I'm so nervous. I'm so nervous. I'm so nervous. I'm so nervous. I'm so nervous. I'm so nervous. I'm so nervous. I'm so nervous. I'm so nervous. I'm so nervous. I'm so nervous. I'm so nervous. I'm so nervous. I'm so nervous. I'm so nervous. I'm so nervous. I'm so nervous. I'm so nervous. I'm so nervous. I'm so nervous. I'm so nervous. I'm so nervous. I'm so nervous. I'm so nervous. I'm so nervous. I'm so nervous. I'm so nervous. I'm so nervous. I'm so nervous. I'm so nervous. I'm so nervous. I'm so nervous. I'm so nervous Thank you very much."` | Yes | 92.0% | Whisper successfully captured key dialogs. |
| **OCR** | Overlay screen text | `"5 | 3 | J | 3 | 3"` | Yes | 52.61% | OCR overlay captured. |
| **Objects** | Physical assets: performer, performance, nervous | `"person, bowl, vase"` | Yes | 57.010000000000005% | YOLO detected physical anchors. |
| **Scenes** | Expected Scene: Entertainment | `"Stage with music performance, Kitchen cooking set, Office desk environment"` | Yes | 28.470000000000002% | CLIP classified environments correctly. |
| **Actions** | Expected Action: beautiful | `"Kissing, Playing saxophone"` | Yes | 9.700000000000001% | VideoMAE kinetic actions recorded. |
| **Audio** | Ambient event detection | `"Speech, Music"` | Yes | 28.82% | AST detected ambient sounds. |
| **Fusion** | Structured Category: Entertainment | Title: "Beautiful Performer Kissing" | Yes | 85.0% | Qwen successfully combined inputs to generate description metadata. |

---

## 🧠 Task 4 & 5: Fusion Metadata Provenance & Hallucination Report

Every generated metadata field and its source evidence provenance are listed below.

### Field: `TITLE`
*   **Generated Value**: `Beautiful Performer Kissing`
*   **Derived From**: `Screen OCR text, Detected Motion/Actions`
*   **LLM Reason**: *The video appears to be a performance of someone kissing, which is visually described in the Screen OCR text and motion detected as kissing.*
*   **Confidence**: `95.0%`
*   **Hallucination Status**: **Supported**

### Field: `SUMMARY`
*   **Generated Value**: `A performer is passionately kissing another person on stage, likely for an audience or music performance.`
*   **Derived From**: `Screen OCR text, Detected Motion/Actions`
*   **LLM Reason**: *The video content describes a kiss and the performer's nervousness, which are key elements of the summary.*
*   **Confidence**: `95.0%`
*   **Hallucination Status**: **Supported**

### Field: `TAGS`
*   **Generated Value**: `['Performance', 'Kissing Scene', 'Music Performance']`
*   **Derived From**: `Screen OCR text, Detected Motion/Actions`
*   **LLM Reason**: *The tags are derived from the described motion and performance elements.*
*   **Confidence**: `95.0%`
*   **Hallucination Status**: **Supported**

### Field: `CATEGORY`
*   **Generated Value**: `Entertainment`
*   **Derived From**: `Category`
*   **LLM Reason**: *The video is primarily about a performer's kiss, which falls under entertainment content.*
*   **Confidence**: `95.0%`
*   **Hallucination Status**: **Unsupported**
  *   *Failed Module*: `Vision/Scene`
  *   *Why Appeared*: *The model hallucinated values unrelated to raw video frames or sound track cues.*
  *   *Missing Evidence*: *Missing explicit environmental layout cues in CLIP scene classification.*

### Field: `SUBCATEGORY`
*   **Generated Value**: `Acoustic Performance`
*   **Derived From**: `Screen OCR text, Detected Motion/Actions`
*   **LLM Reason**: *The performance includes kissing and is likely an acoustic music performance, as indicated by the Screen OCR text.*
*   **Confidence**: `95.0%`
*   **Hallucination Status**: **Supported**

### Field: `MOOD`
*   **Generated Value**: `Playful`
*   **Derived From**: `Screen OCR text, Detected Motion/Actions`
*   **LLM Reason**: *The video is described with playful language and motion, indicating a light-hearted mood.*
*   **Confidence**: `95.0%`
*   **Hallucination Status**: **Unsupported**
  *   *Failed Module*: `Vision/Scene`
  *   *Why Appeared*: *The model hallucinated values unrelated to raw video frames or sound track cues.*
  *   *Missing Evidence*: *Missing explicit environmental layout cues in CLIP scene classification.*

### Field: `LANGUAGE`
*   **Generated Value**: `English`
*   **Derived From**: `Transcript (Speech-to-Text)`
*   **LLM Reason**: *The primary language used in the video is English as it matches the speech-to-text transcript.*
*   **Confidence**: `95.0%`
*   **Hallucination Status**: **Unsupported**
  *   *Failed Module*: `Fusion Reasoning`
  *   *Why Appeared*: *The model hallucinated values unrelated to raw video frames or sound track cues.*
  *   *Missing Evidence*: *No raw evidence tokens correspond to this output.*

### Field: `CONTENT_TYPE`
*   **Generated Value**: `Dialogue Reel`
*   **Derived From**: `Transcript (Speech-to-Text)`
*   **LLM Reason**: *The content type is determined by the speech-to-text transcription, which describes a dialogue or conversation.*
*   **Confidence**: `95.0%`
*   **Hallucination Status**: **Unsupported**
  *   *Failed Module*: `Fusion Reasoning`
  *   *Why Appeared*: *The model hallucinated values unrelated to raw video frames or sound track cues.*
  *   *Missing Evidence*: *No raw evidence tokens correspond to this output.*

### Field: `KEYWORDS`
*   **Generated Value**: `['kissing', 'performer', 'beautiful', 'nervous']`
*   **Derived From**: `Transcript (Speech-to-Text), Screen OCR text`
*   **LLM Reason**: *Key words are derived from the video's content, including kissing, performer, beauty, and nervousness.*
*   **Confidence**: `95.0%`
*   **Hallucination Status**: **Supported**

### Field: `ENTITIES`
*   **Generated Value**: `['person', 'kissing', 'performer']`
*   **Derived From**: `Screen OCR text, Detected Motion/Actions`
*   **LLM Reason**: *Named entities are derived from the described motion and performance elements.*
*   **Confidence**: `95.0%`
*   **Hallucination Status**: **Supported**

### Field: `EMBEDDING_TEXT`
*   **Generated Value**: `A performer passionately kisses another person on stage, likely for an audience or music performance.`
*   **Derived From**: `Title, Summary`
*   **LLM Reason**: *The embedding text combines the title and summary to provide a concise description of the video's content.*
*   **Confidence**: `95.0%`
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
