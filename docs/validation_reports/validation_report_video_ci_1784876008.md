# Video Intelligence Engine: Human Validation Report

## Video Asset Details
* **Video ID**: `video_ci_1784876008`
* **Duration**: `12.01 seconds`

---

## 👁️ Visual Timeline & Scenes
- **Scene [0.0s - 3.9s]**: Scene keyframe 0 displaying visual elements: {'name': 'Nestea Beverages', 'type': 'Product'}, {'name': '#JustKeepDrinking', 'type': 'Text Overlay
- **Scene [3.9s - 6.8s]**: Scene keyframe 1 displaying visual elements: {'name': 'Nestea Beverages', 'type': 'Product'}, {'name': '#JustKeepDrinking', 'type': 'Text Overlay
- **Scene [6.8s - 12.0s]**: Scene keyframe 2 displaying visual elements: {'name': 'Nestea Beverages', 'type': 'Product'}, {'name': '#JustKeepDrinking', 'type': 'Text Overlay

---

## 🎙️ Audio Transcript (Speech-to-Text)
> Just keep drinking, next tip, now in a king can only 99 cents.

---

## 🧠 Semantic Understanding (Generated Metadata)
* **Title**: Advertisement for Nestea Beverages
* **Summary**: The sequence of frames depicts a promotional advertisement featuring two individuals, likely in an outdoor setting. The focus is on promoting the consumption of Nestea beverages with text overlays encouraging viewers to subscribe and follow related content.
* **Category**: Entertainment | **Subcategory**: Advertising
* **Primary Topic**: Nestea Beverages Promotion
* **Secondary Topics**: Subscribe, Follow Content
* **Language**: Hindi
* **Mood**: Informative | **Emotion**: Neutral
* **Target Audience**: General Audience
* **Reasoning Explanation**: The video includes visual cues such as product display and text overlays to promote Nestea beverages, along with a call-to-action for viewers to subscribe or follow related content.

---

## 📊 Secondary Modality Evidence
* **OCR Screen Detections**:
  - `#JustKeepDrinking` (Confidence: 1.00)
* **Visual Object Detections (YOLO/CLIP)**:
  - `person` (Confidence: 0.92)
  - `Person talking to camerin reel or video` (Confidence: 0.37)
  - `Computer screen or software ui` (Confidence: 0.26)
  - `Audition or performance setup` (Confidence: 0.11)
* **Human Action Detections (VideoMAE)**:
  - *No actions classified.*
* **Audio Set Sound Events (AST)**:
  - `Music` (Confidence: 0.32)
  - `Speech` (Confidence: 0.22)
  - `Environmental noise` (Confidence: 0.13)
  - `Bird vocalization, bird call, bird song` (Confidence: 0.07)
  - `Chirp, tweet` (Confidence: 0.06)

---

## 📈 Provenance & Confidence Evaluation
| Field Name | Confidence Score | Evidence Sources | Algorithmic Reason / Justification |
| :--- | :--- | :--- | :--- |
| **CATEGORY** | 0.70 | Foundation Model | Primary VLM classification. No matching secondary sensor logs to confirm. |
| **SUBCATEGORY** | 0.65 | Foundation Model | Subcategory derived from category reasoning. Primary VLM classification. No matching secondary sensor logs to confirm. |
| **TITLE** | 0.75 | Foundation Model | Inferred context from visual representation. |
| **SUMMARY** | 0.75 | Foundation Model | Inferred context from visual representation. |
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
