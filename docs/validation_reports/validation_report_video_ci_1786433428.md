# Video Intelligence Engine: Human Validation Report

## Video Asset Details
* **Video ID**: `video_ci_1786433428`
* **Duration**: `16.17 seconds`

---

## 👁️ Visual Timeline & Scenes
- **Scene [0.0s - 2.7s]**: Scene keyframe 0 displaying visual elements: {'name': 'Ornately decorated floral platform with deity figure and musicians playing instruments.'},
- **Scene [2.7s - 5.4s]**: Scene keyframe 1 displaying visual elements: {'name': 'Ornately decorated floral platform with deity figure and musicians playing instruments.'},
- **Scene [5.4s - 8.1s]**: Scene keyframe 2 displaying visual elements: {'name': 'Ornately decorated floral platform with deity figure and musicians playing instruments.'},
- **Scene [8.1s - 16.2s]**: Scene keyframe 3 displaying visual elements: {'name': 'Ornately decorated floral platform with deity figure and musicians playing instruments.'},

---

## 🎙️ Audio Transcript (Speech-to-Text)
> All right, let's go to the other side of the world.

---

## 🧠 Semantic Understanding (Generated Metadata)
* **Title**: Devotional Procession in a Cultural Festival
* **Summary**: The sequence of frames captures individuals participating in a devotional procession, likely part of a cultural festival. The central figure is seated on an ornately decorated platform adorned with flowers and traditional attire, accompanied by musicians playing instruments.
* **Category**: Pooja | **Subcategory**: Devotional Ritual & Worship
* **Primary Topic**: Religious Devotion during Cultural Celebration
* **Secondary Topics**: Traditional Music, Cultural Festivities
* **Language**: English
* **Mood**: Spiritual and Festive | **Emotion**: [{'name': 'Devotional'}, {'name': 'Happy'}]
* **Target Audience**: Religious followers, Cultural enthusiasts
* **Reasoning Explanation**: The visual elements such as the decorated platform, floral arrangements, and traditional attire indicate a religious procession during a cultural festival. The presence of musicians playing instruments suggests that music is an integral part of this celebration.

---

## 📊 Secondary Modality Evidence
* **OCR Screen Detections**:
  - `0` (Confidence: 0.37)
* **Visual Object Detections (YOLO/CLIP)**:
  - `person` (Confidence: 0.64)
  - `Temple, shrine, or devotional place` (Confidence: 0.41)
  - `Person talking to camerin reel or video` (Confidence: 0.33)
  - `Stage with music performance` (Confidence: 0.21)
* **Human Action Detections (VideoMAE)**:
  - *No actions classified.*
* **Audio Set Sound Events (AST)**:
  - `Music` (Confidence: 0.90)

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
