# Video Intelligence Engine: Human Validation Report

## Video Asset Details
* **Video ID**: `video_ci_1786431074`
* **Duration**: `12.10 seconds`

---

## 👁️ Visual Timeline & Scenes
- **Scene [0.0s - 7.0s]**: Scene keyframe 0 displaying visual elements: {'name': 'Ceremonial vessels with flames', 'description': 'Metal containers filled with burning oil,
- **Scene [7.0s - 10.0s]**: Scene keyframe 1 displaying visual elements: {'name': 'Ceremonial vessels with flames', 'description': 'Metal containers filled with burning oil,
- **Scene [10.0s - 12.0s]**: Scene keyframe 2 displaying visual elements: {'name': 'Ceremonial vessels with flames', 'description': 'Metal containers filled with burning oil,
- **Scene [12.0s - 12.1s]**: Scene keyframe 3 displaying visual elements: {'name': 'Ceremonial vessels with flames', 'description': 'Metal containers filled with burning oil,

---

## 🎙️ Audio Transcript (Speech-to-Text)
> I'm close and I'll tell you what's behind you, I'm out and I won't take it off the ground. I'm in your arms and I'm lost with you.

---

## 🧠 Semantic Understanding (Generated Metadata)
* **Title**: Devotional Ceremony at Night
* **Summary**: The sequence captures an individual performing in a devotional ceremony involving fire rituals. The environment suggests it's taking place outdoors during nighttime with many attendees present.
* **Category**: Devotion | **Subcategory**: Religious Rituals
* **Primary Topic**: Fire Worship Ceremony
* **Secondary Topics**: Nighttime Ceremonies, Outdoor Religious Events
* **Language**: English
* **Mood**: Spiritual and Reverent | **Emotion**: [{'name': 'Devotional'}, {'name': 'Serious'}]
* **Target Audience**: Religious followers, Cultural enthusiasts
* **Reasoning Explanation**: The visual cues such as the ceremonial objects, flames, and crowd participation indicate a religious ceremony. The audio mentions music which is often associated with devotional events.

---

## 📊 Secondary Modality Evidence
* **OCR Screen Detections**:
  - *No text blocks scanned.*
* **Visual Object Detections (YOLO/CLIP)**:
  - `person` (Confidence: 0.54)
  - `Stage with music performance` (Confidence: 0.23)
  - `Temple, shrine, or devotional place` (Confidence: 0.22)
  - `Computer screen or software ui` (Confidence: 0.16)
  - `Audition or performance setup` (Confidence: 0.12)
  - `Person talking to camerin reel or video` (Confidence: 0.10)
* **Human Action Detections (VideoMAE)**:
  - *No actions classified.*
* **Audio Set Sound Events (AST)**:
  - `Music` (Confidence: 0.78)

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
