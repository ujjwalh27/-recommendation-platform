# Video Intelligence Engine: Human Validation Report

## Video Asset Details
* **Video ID**: `daiv_s2_27_anjali__jarad`
* **Duration**: `48.07 seconds`

---

## 👁️ Visual Timeline & Scenes
- **Scene [0.0s - 37.0s]**: Scene keyframe 0 displaying visual elements: {'name': 'Lamp'}, {'name': 'Flowers'}, {'name': 'Bowl of water with marigold petals'}
- **Scene [37.0s - 42.0s]**: Scene keyframe 1 displaying visual elements: {'name': 'Lamp'}, {'name': 'Flowers'}, {'name': 'Bowl of water with marigold petals'}
- **Scene [42.0s - 45.0s]**: Scene keyframe 2 displaying visual elements: {'name': 'Lamp'}, {'name': 'Flowers'}, {'name': 'Bowl of water with marigold petals'}
- **Scene [45.0s - 48.1s]**: Scene keyframe 3 displaying visual elements: {'name': 'Lamp'}, {'name': 'Flowers'}, {'name': 'Bowl of water with marigold petals'}

---

## 🎙️ Audio Transcript (Speech-to-Text)
> You Shri Swami Samarita, Shri Slami Samartha, Shree Slamisamartha It's so wonderful!

---

## 🧠 Semantic Understanding (Generated Metadata)
* **Title**: Devotional Worship in a Temple Setting
* **Summary**: The sequence of frames depicts an individual engaged in devotional worship within a temple or shrine environment. The person is seen lighting a lamp, offering flowers, and praying with devotion.
* **Category**: Devotion | **Subcategory**: Religious Ceremony
* **Primary Topic**: Worship Rituals
* **Secondary Topics**: Offering Flowers, Lighting Lamps
* **Language**: Hindi
* **Mood**: Serious and Devotional | **Emotion**: Devotional, Spiritual
* **Target Audience**: Individuals interested in religious practices or spiritual rituals.
* **Reasoning Explanation**: The visual elements such as the lit lamp, flowers, and shrine setup indicate a devotional worship scene. The audio transcription supports this by mentioning 'Shri Swami Samarita' which is likely associated with the ritual being performed.

---

## 📊 Secondary Modality Evidence
* **OCR Screen Detections**:
  - *No text blocks scanned.*
* **Visual Object Detections (YOLO/CLIP)**:
  - `person` (Confidence: 0.92)
  - `bowl` (Confidence: 0.51)
  - `Person talking to camerin reel or video` (Confidence: 0.65)
  - `Temple, shrine, or devotional place` (Confidence: 0.22)
* **Human Action Detections (VideoMAE)**:
  - *No actions classified.*
* **Audio Set Sound Events (AST)**:
  - `Silence` (Confidence: 0.45)
  - `Music` (Confidence: 0.31)

---

## 📈 Provenance & Confidence Evaluation
| Field Name | Confidence Score | Evidence Sources | Algorithmic Reason / Justification |
| :--- | :--- | :--- | :--- |
| **CATEGORY** | 0.95 | Foundation Model, Speech, Vision | Speech contains devotional keywords/scriptures. Vision model detected temple/altar scenes. |
| **SUBCATEGORY** | 0.90 | Foundation Model, Speech, Vision | Subcategory derived from category reasoning. Speech contains devotional keywords/scriptures. Vision model detected temple/altar scenes. |
| **TITLE** | 0.75 | Foundation Model | Inferred context from visual representation. |
| **SUMMARY** | 0.75 | Foundation Model | Inferred context from visual representation. |
| **PRIMARY_TOPIC** | 0.70 | Foundation Model | Inferred semantic category from keyframes. |
| **LANGUAGE** | 0.99 | Foundation Model, Speech | Verified by Whisper speech transcription service language logs. |
| **MOOD** | 0.70 | Foundation Model | Visual mood interpretation. |
| **EMOTION** | 0.70 | Foundation Model | Visual mood interpretation. |
| **ACTIVITIES** | 0.65 | Foundation Model | No corroboration found for list items in secondary actions sensor logs. |
| **OBJECTS** | 0.78 | Foundation Model, YOLO/CLIP | Verified 1/3 elements against YOLO/CLIP modality detections. |

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
