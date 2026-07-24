# Content Intelligence Validation Report: video_ci_validation_s.laxmi

This report presents diagnostic validation metrics and the provenance hierarchy for `video_ci_validation_s.laxmi.mp4`. 
It compiles raw modality evidence, expected ground truth comparisons, and hallucination detection checks.

---

## 🎥 Video Preview
*   **Video ID**: `video_ci_validation_s.laxmi`
*   **Video File**: [Link to raw video](file:///Users/ujjwalhkumar/Downloads/daiv%20sample/s.laxmi.mp4)
*   **Overall Processing Confidence**: `41.92%`

---

## 📊 Task 3: Module-by-Module Evaluation

| Module | Expected Target | Actual Output | Useful? | Confidence | Comments |
| --- | --- | --- | --- | --- | --- |
| **Speech** | Dialogue matching target: English | `"スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッター スイッターいただきました。"` | Yes | 92.0% | Whisper successfully captured key dialogs. |
| **OCR** | Overlay screen text | `""` | No | 0.0% | No screen text or failed reading. |
| **Objects** | Physical assets: singer, performance, music | `"person"` | Yes | 58.18% | YOLO detected physical anchors. |
| **Scenes** | Expected Scene: Music | `"Stage with music performance, Office desk environment, Kitchen cooking set"` | Yes | 30.380000000000003% | CLIP classified environments correctly. |
| **Actions** | Expected Action: dialogue | `"Wrapping present, Tying tie, Folding clothes"` | Yes | 17.83% | VideoMAE kinetic actions recorded. |
| **Audio** | Ambient event detection | `"Stomach rumble, Singing, Child singing, Speech, Music"` | Yes | 11.219999999999999% | AST detected ambient sounds. |
| **Fusion** | Structured Category: Music | Title: "Singer's Performance" | Yes | 85.0% | Qwen successfully combined inputs to generate description metadata. |

---

## 🧠 Task 4 & 5: Fusion Metadata Provenance & Hallucination Report

Every generated metadata field and its source evidence provenance are listed below.

### Field: `TITLE`
*   **Generated Value**: `Singer's Performance`
*   **Derived From**: `Transcript, Screen OCR text`
*   **LLM Reason**: *The video appears to be a performance by a singer, as evidenced by the repetitive 'スイッター' phrase and the overall structure of the content.*
*   **Confidence**: `90.0%`
*   **Hallucination Status**: **Supported**

### Field: `SUMMARY`
*   **Generated Value**: `A singer performs multiple songs in a row with repetitive lyrics, likely for an audience or on stage.`
*   **Derived From**: `Transcript, Screen OCR text`
*   **LLM Reason**: *The transcript and screen text confirm the singer's performance of various songs repeatedly.*
*   **Confidence**: `90.0%`
*   **Hallucination Status**: **Partially Supported**

### Field: `TAGS`
*   **Generated Value**: `['Music Performance', 'Singer', 'Repetitive Song']`
*   **Derived From**: `Transcript, Screen OCR text`
*   **LLM Reason**: *The content is clearly a performance of songs, with repetitive lyrics.*
*   **Confidence**: `90.0%`
*   **Hallucination Status**: **Supported**

### Field: `CATEGORY`
*   **Generated Value**: `Music`
*   **Derived From**: `Tags`
*   **LLM Reason**: *The primary context and tags indicate the video is about music performances.*
*   **Confidence**: `85.0%`
*   **Hallucination Status**: **Supported**

### Field: `SUBCATEGORY`
*   **Generated Value**: `Acoustic Performance`
*   **Derived From**: `Tags, Screen OCR text`
*   **LLM Reason**: *The presence of a stage with music performance suggests an acoustic setting, further confirming the subcategory as acoustic.*
*   **Confidence**: `85.0%`
*   **Hallucination Status**: **Supported**

### Field: `MOOD`
*   **Generated Value**: `Relaxed`
*   **Derived From**: `Transcript, Screen OCR text`
*   **LLM Reason**: *The repetitive nature of the song and the overall relaxed tone suggest a casual, non-urgent mood.*
*   **Confidence**: `85.0%`
*   **Hallucination Status**: **Unsupported**
  *   *Failed Module*: `Vision/Scene`
  *   *Why Appeared*: *The model hallucinated values unrelated to raw video frames or sound track cues.*
  *   *Missing Evidence*: *Missing explicit environmental layout cues in CLIP scene classification.*

### Field: `LANGUAGE`
*   **Generated Value**: `Japanese`
*   **Derived From**: `Transcript, Screen OCR text`
*   **LLM Reason**: *The transcript is in Japanese, confirming the primary language of the video.*
*   **Confidence**: `90.0%`
*   **Hallucination Status**: **Unsupported**
  *   *Failed Module*: `Fusion Reasoning`
  *   *Why Appeared*: *The model hallucinated values unrelated to raw video frames or sound track cues.*
  *   *Missing Evidence*: *No raw evidence tokens correspond to this output.*

### Field: `CONTENT_TYPE`
*   **Generated Value**: `Dialogue Reel`
*   **Derived From**: `Tags, Screen OCR text`
*   **LLM Reason**: *The repetitive nature and the presence of a stage suggest this is likely a dialogue reel, with performers interacting.*
*   **Confidence**: `90.0%`
*   **Hallucination Status**: **Unsupported**
  *   *Failed Module*: `Fusion Reasoning`
  *   *Why Appeared*: *The model hallucinated values unrelated to raw video frames or sound track cues.*
  *   *Missing Evidence*: *No raw evidence tokens correspond to this output.*

### Field: `KEYWORDS`
*   **Generated Value**: `['スイッター', '歌', '演奏', 'リズム', '舞台']`
*   **Derived From**: `Speech`
*   **LLM Reason**: *Recovered from LLM direct key-value fallback.*
*   **Confidence**: `80.0%`
*   **Hallucination Status**: **Partially Supported**

### Field: `ENTITIES`
*   **Generated Value**: `['スイッター', '歌', '演奏', 'リズム', '舞台']`
*   **Derived From**: `Speech`
*   **LLM Reason**: *Recovered from LLM direct key-value fallback.*
*   **Confidence**: `80.0%`
*   **Hallucination Status**: **Partially Supported**

### Field: `EMBEDDING_TEXT`
*   **Generated Value**: `A singer performs multiple songs in a row with repetitive lyrics, likely for an audience or on stage. The video is described as an acoustic performance and dialogue reel.`
*   **Derived From**: `Title, Summary, Tags`
*   **LLM Reason**: *The optimized natural description combines the title, summary, tags, category, mood, language, content type, keywords, and entities to provide a comprehensive overview of the video's content.*
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
