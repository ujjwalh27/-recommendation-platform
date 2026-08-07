# Video Intelligence Engine: Human Validation Report

## Video Asset Details
* **Video ID**: `video_ci_1785824304`
* **Duration**: `10.80 seconds`

---

## 👁️ Visual Timeline & Scenes
- **Scene [0.0s - 1.8s]**: Scene keyframe 0 displaying visual elements: {'name': 'Bowl of food items'}, {'name': 'Bananas'}, {'name': 'Cup (possibly for liquid offerings)'}
- **Scene [1.8s - 3.6s]**: Scene keyframe 1 displaying visual elements: {'name': 'Bowl of food items'}, {'name': 'Bananas'}, {'name': 'Cup (possibly for liquid offerings)'}
- **Scene [3.6s - 5.4s]**: Scene keyframe 2 displaying visual elements: {'name': 'Bowl of food items'}, {'name': 'Bananas'}, {'name': 'Cup (possibly for liquid offerings)'}
- **Scene [5.4s - 10.8s]**: Scene keyframe 3 displaying visual elements: {'name': 'Bowl of food items'}, {'name': 'Bananas'}, {'name': 'Cup (possibly for liquid offerings)'}

---

## 🎙️ Audio Transcript (Speech-to-Text)
> If you're happy, if you're on the right side, you're not on the left side, and if you can't be happy, you are on the wrong side.

---

## 🧠 Semantic Understanding (Generated Metadata)
* **Title**: Devotional Ceremony in a Temple
* **Summary**: The sequence of frames captures an ongoing devotional ceremony involving the lighting of a sacred fire, offerings, and various ritualistic items. The audio suggests themes of happiness and right-side thinking.
* **Category**: Devotion | **Subcategory**: Religious Rituals
* **Primary Topic**: A religious or spiritual offering in progress
* **Secondary Topics**: Offerings, Fire Lighting Ceremony
* **Language**: English
* **Mood**: Solemn, Devotional | **Emotion**: Serious
* **Target Audience**: Devotees or followers of the religion being practiced
* **Reasoning Explanation**: The visual elements such as the sacred fire, offerings, and ritualistic items indicate a religious ceremony. The audio content reinforces themes associated with spirituality.

---

## 📊 Secondary Modality Evidence
* **OCR Screen Detections**:
  - *No text blocks scanned.*
* **Visual Object Detections (YOLO/CLIP)**:
  - `bowl` (Confidence: 0.52)
  - `banana` (Confidence: 0.52)
  - `cup` (Confidence: 0.36)
  - `Temple, shrine, or devotional place` (Confidence: 0.65)
  - `Kitchen cooking set` (Confidence: 0.24)
* **Human Action Detections (VideoMAE)**:
  - *No actions classified.*
* **Audio Set Sound Events (AST)**:
  - `Jingle bell` (Confidence: 0.36)
  - `Music` (Confidence: 0.35)
  - `Tambourine` (Confidence: 0.10)

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
| **OBJECTS** | 0.95 | Foundation Model, YOLO/CLIP | Verified 3/3 elements against YOLO/CLIP modality detections. |

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
