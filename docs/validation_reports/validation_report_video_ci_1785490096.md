# Video Intelligence Engine: Human Validation Report

## Video Asset Details
* **Video ID**: `video_ci_1785490096`
* **Duration**: `12.27 seconds`

---

## 👁️ Visual Timeline & Scenes
- **Scene [0.0s - 7.0s]**: Scene keyframe 0 displaying visual elements: {'description': 'A decorated idol with a crown', 'color': '#FF008C'}, {'description': 'Flowers in va
- **Scene [7.0s - 12.3s]**: Scene keyframe 1 displaying visual elements: {'description': 'A decorated idol with a crown', 'color': '#FF008C'}, {'description': 'Flowers in va

---

## 🎙️ Audio Transcript (Speech-to-Text)
> Thank you very much for watching.

---

## 🧠 Semantic Understanding (Generated Metadata)
* **Title**: Devotional Worship in a Temple
* **Summary**: The sequence of frames captures the ritualistic worship within a temple, showcasing offerings being made before an idol adorned with flowers. The audio includes music and percussion, enhancing the spiritual ambiance.
* **Category**: Devotion | **Subcategory**: Religious Rituals
* **Primary Topic**: Worship in a Temple
* **Secondary Topics**: Offerings, Idol Worship
* **Language**: English
* **Mood**: Spiritual and Devotional | **Emotion**: ['Devotional', 'Calm']
* **Target Audience**: Religious followers, devotees of Hinduism
* **Reasoning Explanation**: The visual elements such as the idol adorned with flowers, lit lamps, and traditional attire indicate a religious worship setting. The audio includes music and percussion which are commonly associated with temple rituals.

---

## 📊 Secondary Modality Evidence
* **OCR Screen Detections**:
  - `onkargaikwad` (Confidence: 0.89)
  - `onkargaikwad` (Confidence: 0.99)
* **Visual Object Detections (YOLO/CLIP)**:
  - `Temple, shrine, or devotional place` (Confidence: 0.99)
* **Human Action Detections (VideoMAE)**:
  - *No actions classified.*
* **Audio Set Sound Events (AST)**:
  - `Music` (Confidence: 0.38)
  - `Percussion` (Confidence: 0.14)
  - `Drum` (Confidence: 0.13)

---

## 📈 Provenance & Confidence Evaluation
| Field Name | Confidence Score | Evidence Sources | Algorithmic Reason / Justification |
| :--- | :--- | :--- | :--- |
| **CATEGORY** | 0.85 | Foundation Model, Vision | Vision model detected temple/altar scenes. |
| **SUBCATEGORY** | 0.80 | Foundation Model, Vision | Subcategory derived from category reasoning. Vision model detected temple/altar scenes. |
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
