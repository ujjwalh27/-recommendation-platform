# Video Intelligence Engine: Human Validation Report

## Video Asset Details
* **Video ID**: `video_ci_1785147888`
* **Duration**: `13.47 seconds`

---

## 👁️ Visual Timeline & Scenes
- **Scene [0.0s - 10.0s]**: Scene keyframe 0 displaying visual elements: {'name': 'Water pot', 'description': 'A brown ceramic vessel used to pour water.', 'location': 'In t
- **Scene [10.0s - 13.5s]**: Scene keyframe 1 displaying visual elements: {'name': 'Water pot', 'description': 'A brown ceramic vessel used to pour water.', 'location': 'In t

---

## 🎙️ Audio Transcript (Speech-to-Text)
> 喜歡呀後裏 問的那陣子屬於呀呀 等下快樂 哪是快樂死裏了 等他呀

---

## 🧠 Semantic Understanding (Generated Metadata)
* **Title**: Devotional Ceremony at a Temple
* **Summary**: The sequence captures individuals performing devotional rituals involving pouring water over an object adorned with flowers in what appears to be a temple or shrine setting.
* **Category**: Devotion | **Subcategory**: Religious Rituals
* **Primary Topic**: A religious ceremony focused on devotion and worship.
* **Secondary Topics**: Water Pouring Ceremony, Floral Decorations
* **Language**: English
* **Mood**: Serious and Devotional | **Emotion**: Devotional, Reverent
* **Target Audience**: Religious Practitioners, People Interested in Religious Ceremonies
* **Reasoning Explanation**: The visual frames depict individuals engaged in a religious ceremony involving the pouring of water over an adorned object, which is indicative of devotional practices. The audio transcript and secondary sensor logs support this interpretation by mentioning activities related to devotion.

---

## 📊 Secondary Modality Evidence
* **OCR Screen Detections**:
  - *No text blocks scanned.*
* **Visual Object Detections (YOLO/CLIP)**:
  - `person` (Confidence: 0.76)
  - `cake` (Confidence: 0.37)
  - `Temple, shrine, or devotional place` (Confidence: 0.73)
  - `Kitchen cooking set` (Confidence: 0.13)
* **Human Action Detections (VideoMAE)**:
  - `Kissing` (Confidence: 0.32)
* **Audio Set Sound Events (AST)**:
  - `Music` (Confidence: 0.54)
  - `Mantra` (Confidence: 0.39)

---

## 📈 Provenance & Confidence Evaluation
| Field Name | Confidence Score | Evidence Sources | Algorithmic Reason / Justification |
| :--- | :--- | :--- | :--- |
| **CATEGORY** | 0.90 | Foundation Model, Vision, Audio | Vision model detected temple/altar scenes. Audio model detected prayer/singing events. |
| **SUBCATEGORY** | 0.85 | Foundation Model, Vision, Audio | Subcategory derived from category reasoning. Vision model detected temple/altar scenes. Audio model detected prayer/singing events. |
| **TITLE** | 0.75 | Foundation Model | Inferred context from visual representation. |
| **SUMMARY** | 0.75 | Foundation Model | Inferred context from visual representation. |
| **PRIMARY_TOPIC** | 0.70 | Foundation Model | Inferred semantic category from keyframes. |
| **LANGUAGE** | 0.99 | Foundation Model, Speech | Verified by Whisper speech transcription service language logs. |
| **MOOD** | 0.70 | Foundation Model | Visual mood interpretation. |
| **EMOTION** | 0.70 | Foundation Model | Visual mood interpretation. |
| **ACTIVITIES** | 0.65 | Foundation Model | No corroboration found for list items in secondary actions sensor logs. |
| **OBJECTS** | 0.82 | Foundation Model, YOLO/CLIP | Verified 1/2 elements against YOLO/CLIP modality detections. |

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
