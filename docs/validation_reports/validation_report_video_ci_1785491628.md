# Video Intelligence Engine: Human Validation Report

## Video Asset Details
* **Video ID**: `video_ci_1785491628`
* **Duration**: `22.03 seconds`

---

## 👁️ Visual Timeline & Scenes
- **Scene [0.0s - 14.0s]**: Scene keyframe 0 displaying visual elements: {'type': 'Bottle', 'location': "On the floor near a person's feet"}
- **Scene [14.0s - 17.0s]**: Scene keyframe 1 displaying visual elements: {'type': 'Bottle', 'location': "On the floor near a person's feet"}
- **Scene [17.0s - 18.0s]**: Scene keyframe 2 displaying visual elements: {'type': 'Bottle', 'location': "On the floor near a person's feet"}
- **Scene [18.0s - 22.0s]**: Scene keyframe 3 displaying visual elements: {'type': 'Bottle', 'location': "On the floor near a person's feet"}

---

## 🎙️ Audio Transcript (Speech-to-Text)
> Chari bazaar, Karoli kishori rahe Omaklipal saris karihamaari Omaklepal sarisarihamaani Parikaraya marali kishuri rahe Kari kaoya malori kishore rahe

---

## 🧠 Semantic Understanding (Generated Metadata)
* **Title**: Devotional Gathering at a Temple
* **Summary**: The video captures a large gathering of people in front of an ornate shrine, likely within a temple. The crowd is engaged in worship or prayer, with many individuals raising their hands and some taking photos on their phones.
* **Category**: Devotion | **Subcategory**: Religious Worship Gathering
* **Primary Topic**: A religious event at a Hindu temple involving Bhajans (devotional songs)
* **Secondary Topics**: Bhajan performance, Temple worship
* **Language**: Hindi
* **Mood**: Spiritual and Reverent | **Emotion**: Devotional, Reverence
* **Target Audience**: Individuals interested in Hindu religious practices
* **Reasoning Explanation**: The video showcases a large gathering of people engaged in worship at a temple. The presence of Bhajans and the ornate shrine suggest that this event is centered around devotional activities.

---

## 📊 Secondary Modality Evidence
* **OCR Screen Detections**:
  - `MERE_RAM;` (Confidence: 0.64)
* **Visual Object Detections (YOLO/CLIP)**:
  - `bottle` (Confidence: 0.76)
  - `person` (Confidence: 0.53)
  - `Temple, shrine, or devotional place` (Confidence: 0.58)
  - `Person talking to camerin reel or video` (Confidence: 0.25)
  - `Stage with music performance` (Confidence: 0.14)
* **Human Action Detections (VideoMAE)**:
  - *No actions classified.*
* **Audio Set Sound Events (AST)**:
  - `Music` (Confidence: 0.73)
  - `Folk music` (Confidence: 0.07)
  - `Music of bollywood` (Confidence: 0.06)

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
| **OBJECTS** | 0.95 | Foundation Model, YOLO/CLIP | Verified 1/1 elements against YOLO/CLIP modality detections. |

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
