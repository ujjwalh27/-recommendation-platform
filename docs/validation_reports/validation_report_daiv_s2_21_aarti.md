# Video Intelligence Engine: Human Validation Report

## Video Asset Details
* **Video ID**: `daiv_s2_21_aarti`
* **Duration**: `12.27 seconds`

---

## 👁️ Visual Timeline & Scenes
- **Scene [0.0s - 7.0s]**: Scene keyframe 0 displaying visual elements: {'description': 'A lit lamp', 'location': 'In front of the idol'}, {'description': 'Flowers and garl
- **Scene [7.0s - 12.3s]**: Scene keyframe 1 displaying visual elements: {'description': 'A lit lamp', 'location': 'In front of the idol'}, {'description': 'Flowers and garl

---

## 🎙️ Audio Transcript (Speech-to-Text)
> Thank you very much for watching.

---

## 🧠 Semantic Understanding (Generated Metadata)
* **Title**: Devotional Worship in a Temple
* **Summary**: The sequence of frames captures the ritualistic worship within a temple, showcasing offerings being made before an idol adorned with flowers and jewelry. The audio includes thanks for watching, while secondary sensors detect religious ambiance through drumming sounds.
* **Category**: Religion | **Subcategory**: Devotion
* **Primary Topic**: Worship Rituals in a Temple
* **Secondary Topics**: Offerings, Idol Worship
* **Language**: English
* **Mood**: Spiritual and reverent | **Emotion**: ['Devotional', 'Respectful']
* **Target Audience**: Religious practitioners, People interested in cultural practices
* **Reasoning Explanation**: The visual elements of flowers, garlands, and an idol being worshipped along with the audio cues indicate a religious ceremony taking place within a temple. The secondary sensor data supports this interpretation by noting drumming sounds associated with such rituals.

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
