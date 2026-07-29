# Video Intelligence Engine: Human Validation Report

## Video Asset Details
* **Video ID**: `video_ci_1784876210`
* **Duration**: `12.00 seconds`

---

## 👁️ Visual Timeline & Scenes
- **Scene [0.0s - 2.0s]**: Scene keyframe 0 displaying visual elements: {'description': 'A white object held by Tom, possibly related to their discussion.'}
- **Scene [2.0s - 4.0s]**: Scene keyframe 1 displaying visual elements: {'description': 'A white object held by Tom, possibly related to their discussion.'}
- **Scene [4.0s - 6.0s]**: Scene keyframe 2 displaying visual elements: {'description': 'A white object held by Tom, possibly related to their discussion.'}
- **Scene [6.0s - 8.0s]**: Scene keyframe 3 displaying visual elements: {'description': 'A white object held by Tom, possibly related to their discussion.'}
- **Scene [8.0s - 10.0s]**: Scene keyframe 4 displaying visual elements: {'description': 'A white object held by Tom, possibly related to their discussion.'}
- **Scene [10.0s - 12.0s]**: Scene keyframe 5 displaying visual elements: {'description': 'A white object held by Tom, possibly related to their discussion.'}
- **Scene [12.0s - 12.0s]**: Scene keyframe 6 displaying visual elements: {'description': 'A white object held by Tom, possibly related to their discussion.'}

---

## 🎙️ Audio Transcript (Speech-to-Text)
> My name is Tom, originally from Vietnam, if you're wondering, if your wondering if he's Japanese, how do I do this? Show me how to wait. Yes.

---

## 🧠 Semantic Understanding (Generated Metadata)
* **Title**: Vietnamese-American Interaction in a Cultural Setting
* **Summary**: In the sequence of frames, an individual named Tom from Vietnam is seen engaging with another person. They appear to be discussing cultural practices or traditions as indicated by their gestures and expressions.
* **Category**: Devotion | **Subcategory**: Cultural Exchange
* **Primary Topic**: Cultural Interaction
* **Secondary Topics**: Vietnamese-American Cultural Exchange, Traditional Practices
* **Language**: English
* **Mood**: Informative | **Emotion**: Serious
* **Target Audience**: Individuals interested in cultural exchanges between Vietnamese-Americans and other cultures.
* **Reasoning Explanation**: The visual cues such as the traditional decorations, attire of Tom, and their interaction suggest a focus on cultural practices. The audio transcript indicates they are discussing how to wait or perform an action related to culture.

---

## 📊 Secondary Modality Evidence
* **OCR Screen Detections**:
  - `1` (Confidence: 0.62)
  - `1 | 2` (Confidence: 0.57)
  - `1` (Confidence: 0.86)
  - `7 | 1 | 2` (Confidence: 0.63)
  - `1 | 62 | 2` (Confidence: 0.62)
* **Visual Object Detections (YOLO/CLIP)**:
  - `person` (Confidence: 0.90)
  - `chair` (Confidence: 0.44)
  - `Person talking to camerin reel or video` (Confidence: 0.93)
* **Human Action Detections (VideoMAE)**:
  - *No actions classified.*
* **Audio Set Sound Events (AST)**:
  - `Speech` (Confidence: 0.62)
  - `Music` (Confidence: 0.24)

---

## 📈 Provenance & Confidence Evaluation
| Field Name | Confidence Score | Evidence Sources | Algorithmic Reason / Justification |
| :--- | :--- | :--- | :--- |
| **CATEGORY** | 0.70 | Foundation Model | Primary VLM classification. No matching secondary sensor logs to confirm. |
| **SUBCATEGORY** | 0.65 | Foundation Model | Subcategory derived from category reasoning. Primary VLM classification. No matching secondary sensor logs to confirm. |
| **TITLE** | 0.75 | Foundation Model | Inferred context from visual representation. |
| **SUMMARY** | 0.87 | Foundation Model, Speech | Text aligns with spoken transcripts. |
| **PRIMARY_TOPIC** | 0.70 | Foundation Model | Inferred semantic category from keyframes. |
| **LANGUAGE** | 0.99 | Foundation Model, Speech | Verified by Whisper speech transcription service language logs. |
| **MOOD** | 0.70 | Foundation Model | Visual mood interpretation. |
| **EMOTION** | 0.70 | Foundation Model | Visual mood interpretation. |
| **ACTIVITIES** | 0.65 | Foundation Model | No corroboration found for list items in secondary actions sensor logs. |
| **OBJECTS** | 0.65 | Foundation Model | No corroboration found for list items in secondary vision sensor logs. |

---

## ✍️ Human Auditor Review Feedback
*Please fill out this block to track semantic alignment performance:*

* **Title Accuracy**: [ ] Correct  |  [ ] Partially Correct  |  [ ] Incorrect
* **Summary Accuracy**: [ ] Correct  |  [ ] Partially Correct  |  [ ] Incorrect
* **Topic & Tag Relevance**: [ ] Correct  |  [ ] Partially Correct  |  [ ] Incorrect
* **Category Classification**: [ ] Correct  |  [ ] Partially Correct  |  [ ] Incorrect

### Review Comments & Notes
```text
[Enter feedback details, discrepancies, or notes here]
```

**Auditor Name**: \_\_\_\_\_\_\_\_\_\_\_\_  
**Date Evaluated**: \_\_\_\_\_\_\_\_\_\_\_\_
