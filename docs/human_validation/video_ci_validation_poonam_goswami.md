# Content Intelligence Validation Report: video_ci_validation_poonam_goswami

This report presents diagnostic validation metrics and the provenance hierarchy for `video_ci_validation_poonam_goswami.mp4`. 
It compiles raw modality evidence, expected ground truth comparisons, and hallucination detection checks.

---

## 🎥 Video Preview
*   **Video ID**: `video_ci_validation_poonam_goswami`
*   **Video File**: [Link to raw video](file:///Users/ujjwalhkumar/Downloads/daiv%20sample/poonam_goswami.mp4)
*   **Overall Processing Confidence**: `51.35999999999999%`

---

## 📊 Task 3: Module-by-Module Evaluation

| Module | Expected Target | Actual Output | Useful? | Confidence | Comments |
| --- | --- | --- | --- | --- | --- |
| **Speech** | Dialogue matching target: English | `"My Rishokhada khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khatiram khat میری نے یا کی بھنے ہارتمی میری نے یا کی بھنے ہارتمی میرا بھی را پارتم ہی سیجمت ایتا مد پولے بھنے ممات"` | Yes | 92.0% | Whisper successfully captured key dialogs. |
| **OCR** | Overlay screen text | `""` | No | 0.0% | No screen text or failed reading. |
| **Objects** | Physical assets: cooking, tutorial, cake | `"vase, person, knife, cake"` | Yes | 52.39% | YOLO detected physical anchors. |
| **Scenes** | Expected Scene: Entertainment | `"Kitchen cooking set, Inside of car or vehicle, Office desk environment, Stage with music performance"` | Yes | 19.88% | CLIP classified environments correctly. |
| **Actions** | Expected Action: kitchen | `"Wrapping present, Kissing, Cheerleading, Arranging flowers, Tying tie"` | Yes | 7.7299999999999995% | VideoMAE kinetic actions recorded. |
| **Audio** | Ambient event detection | `"Music"` | Yes | 84.78% | AST detected ambient sounds. |
| **Fusion** | Structured Category: Entertainment | Title: "Celebration and Cooking" | Yes | 85.0% | Qwen successfully combined inputs to generate description metadata. |

---

## 🧠 Task 4 & 5: Fusion Metadata Provenance & Hallucination Report

Every generated metadata field and its source evidence provenance are listed below.

### Field: `TITLE`
*   **Generated Value**: `Celebration and Cooking`
*   **Derived From**: `Screen OCR text, Transcript`
*   **LLM Reason**: *The video appears to be a celebration with elements of cooking, including wrapping presents, kissing, cheerleading, arranging flowers, tying ties, and music.*
*   **Confidence**: `90.0%`
*   **Hallucination Status**: **Supported**

### Field: `SUMMARY`
*   **Generated Value**: `A festive celebration featuring various activities such as wrapping gifts, singing, dancing, and enjoying a musical performance.`
*   **Derived From**: `Screen OCR text, Transcript`
*   **LLM Reason**: *The video content describes multiple activities that are typically associated with celebrations and performances.*
*   **Confidence**: `90.0%`
*   **Hallucination Status**: **Partially Supported**

### Field: `TAGS`
*   **Generated Value**: `['Celebration', 'Cooking', 'Performance', 'Gift Wrapping', 'Music Performance']`
*   **Derived From**: `Screen OCR text, Transcript`
*   **LLM Reason**: *The video tags include elements such as celebration, cooking, performance, gift wrapping, and music performance.*
*   **Confidence**: `90.0%`
*   **Hallucination Status**: **Supported**

### Field: `CATEGORY`
*   **Generated Value**: `Entertainment`
*   **Derived From**: `Category`
*   **LLM Reason**: *The content is primarily focused on celebrations and performances, which are typically categorized under entertainment.*
*   **Confidence**: `85.0%`
*   **Hallucination Status**: **Unsupported**
  *   *Failed Module*: `Vision/Scene`
  *   *Why Appeared*: *The model hallucinated values unrelated to raw video frames or sound track cues.*
  *   *Missing Evidence*: *Missing explicit environmental layout cues in CLIP scene classification.*

### Field: `SUBCATEGORY`
*   **Generated Value**: `Celebration`
*   **Derived From**: `Category, Tags`
*   **LLM Reason**: *The video's tags include 'Celebration' and the overall theme is a celebration, making this subcategory appropriate.*
*   **Confidence**: `90.0%`
*   **Hallucination Status**: **Unsupported**
  *   *Failed Module*: `Vision/Scene`
  *   *Why Appeared*: *The model hallucinated values unrelated to raw video frames or sound track cues.*
  *   *Missing Evidence*: *Missing explicit environmental layout cues in CLIP scene classification.*

### Field: `MOOD`
*   **Generated Value**: `Happy`
*   **Derived From**: `Screen OCR text, Transcript`
*   **LLM Reason**: *The video description mentions activities like singing, dancing, and enjoying music, which are typically associated with a happy mood.*
*   **Confidence**: `90.0%`
*   **Hallucination Status**: **Unsupported**
  *   *Failed Module*: `Vision/Scene`
  *   *Why Appeared*: *The model hallucinated values unrelated to raw video frames or sound track cues.*
  *   *Missing Evidence*: *Missing explicit environmental layout cues in CLIP scene classification.*

### Field: `LANGUAGE`
*   **Generated Value**: `English`
*   **Derived From**: `Screen OCR text, Transcript`
*   **LLM Reason**: *The video transcript is in English, confirming the primary language spoken or detected.*
*   **Confidence**: `95.0%`
*   **Hallucination Status**: **Unsupported**
  *   *Failed Module*: `Fusion Reasoning`
  *   *Why Appeared*: *The model hallucinated values unrelated to raw video frames or sound track cues.*
  *   *Missing Evidence*: *No raw evidence tokens correspond to this output.*

### Field: `CONTENT_TYPE`
*   **Generated Value**: `Celebration Video`
*   **Derived From**: `Category, Tags`
*   **LLM Reason**: *The content type is identified as a celebration video due to its festive and performance-oriented nature.*
*   **Confidence**: `80.0%`
*   **Hallucination Status**: **Unsupported**
  *   *Failed Module*: `Fusion Reasoning`
  *   *Why Appeared*: *The model hallucinated values unrelated to raw video frames or sound track cues.*
  *   *Missing Evidence*: *No raw evidence tokens correspond to this output.*

### Field: `KEYWORDS`
*   **Generated Value**: `['celebration', 'cooking', 'gift wrapping', 'music performance', 'happy mood']`
*   **Derived From**: `Speech`
*   **LLM Reason**: *Recovered from LLM direct key-value fallback.*
*   **Confidence**: `80.0%`
*   **Hallucination Status**: **Partially Supported**

### Field: `ENTITIES`
*   **Generated Value**: `['cake', 'stage with music performance', 'person', 'knife', 'vase']`
*   **Derived From**: `Speech`
*   **LLM Reason**: *Recovered from LLM direct key-value fallback.*
*   **Confidence**: `80.0%`
*   **Hallucination Status**: **Supported**

### Field: `EMBEDDING_TEXT`
*   **Generated Value**: `Celebration and cooking, gift wrapping, musical performances, joyful atmosphere.`
*   **Derived From**: `Title, Summary, Category, Mood`
*   **LLM Reason**: *The embedding text combines the main elements of the video into a concise description for indexing purposes.*
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
