# Video Intelligence Engine: Human Validation Report

## Video Asset Details
* **Video ID**: `video_ci_1785736417`
* **Duration**: `16.17 seconds`

---

## 👁️ Visual Timeline & Scenes
- **Scene [0.0s - 2.7s]**: Scene keyframe 0 displaying visual elements: {'name': 'Ornately decorated shrine', 'description': 'The shrine is adorned with flowers, fabric, an
- **Scene [2.7s - 5.4s]**: Scene keyframe 1 displaying visual elements: {'name': 'Ornately decorated shrine', 'description': 'The shrine is adorned with flowers, fabric, an
- **Scene [5.4s - 8.1s]**: Scene keyframe 2 displaying visual elements: {'name': 'Ornately decorated shrine', 'description': 'The shrine is adorned with flowers, fabric, an
- **Scene [8.1s - 16.2s]**: Scene keyframe 3 displaying visual elements: {'name': 'Ornately decorated shrine', 'description': 'The shrine is adorned with flowers, fabric, an

---

## 🎙️ Audio Transcript (Speech-to-Text)
> All right, let's go to the other side of the world.

---

## 🧠 Semantic Understanding (Generated Metadata)
* **Title**: Devotional Procession in a Religious Context
* **Summary**: The video captures a vibrant devotional procession involving individuals dressed in traditional attire, carrying an ornately decorated shrine. The setting appears to be outside of a temple or religious site with participants engaged in musical performances and ceremonial activities.
* **Category**: Devotion | **Subcategory**: Religious Procession
* **Primary Topic**: A spiritual event centered around the worship of deities through procession and music.
* **Secondary Topics**: Traditional attire, Ornate shrine decoration
* **Language**: English
* **Mood**: Energetic and Devotional | **Emotion**: ['Devotion', 'Calmness']
* **Target Audience**: Religious followers, particularly those who participate in Hindu festivals and processions
* **Reasoning Explanation**: The video showcases a religious procession with participants dressed traditionally while carrying an ornately decorated shrine. The setting appears to be outside of a temple or devotional site where musical performances are part of the ceremony.

---

## 📊 Secondary Modality Evidence
* **OCR Screen Detections**:
  - `0` (Confidence: 0.37)
* **Visual Object Detections (YOLO/CLIP)**:
  - `car` (Confidence: 0.72)
  - `person` (Confidence: 0.70)
  - `Temple, shrine, or devotional place` (Confidence: 0.64)
  - `Stage with music performance` (Confidence: 0.15)
  - `Person talking to camerin reel or video` (Confidence: 0.12)
* **Human Action Detections (VideoMAE)**:
  - *No actions classified.*
* **Audio Set Sound Events (AST)**:
  - `Music` (Confidence: 0.90)

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
