# Video Intelligence Engine: Human Validation Report

## Video Asset Details
* **Video ID**: `video_ci_1785487120`
* **Duration**: `24.91 seconds`

---

## 👁️ Visual Timeline & Scenes
- **Scene [0.0s - 4.1s]**: Scene keyframe 0 displaying visual elements: {'name': 'Cup', 'description': 'A cup used to pour liquid.'}, {'name': 'Vase with flowers', 'descrip
- **Scene [4.1s - 8.3s]**: Scene keyframe 1 displaying visual elements: {'name': 'Cup', 'description': 'A cup used to pour liquid.'}, {'name': 'Vase with flowers', 'descrip
- **Scene [8.3s - 12.4s]**: Scene keyframe 2 displaying visual elements: {'name': 'Cup', 'description': 'A cup used to pour liquid.'}, {'name': 'Vase with flowers', 'descrip
- **Scene [12.4s - 24.9s]**: Scene keyframe 3 displaying visual elements: {'name': 'Cup', 'description': 'A cup used to pour liquid.'}, {'name': 'Vase with flowers', 'descrip

---

## 🎙️ Audio Transcript (Speech-to-Text)
> Karalauma kala kaalaun krepaalaun Guna garathan saar Paaramnatuhan Tusharatvisan kaakshan Gauram gamhi

---

## 🧠 Semantic Understanding (Generated Metadata)
* **Title**: Devotional Ceremony in a Temple
* **Summary**: The sequence of frames depicts an individual performing devotional rituals within a temple or shrine. The environment is adorned with flowers, sacred items, and golden decorations indicating the sanctity of the place.
* **Category**: Devotion | **Subcategory**: Religious Rituals
* **Primary Topic**: A religious ceremony involving water pouring over a sacred object in a devotional setting.
* **Secondary Topics**: Water Pouring Ceremony, Temple Worship
* **Language**: Hindi
* **Mood**: Solemn and Devotional | **Emotion**: Serious, Spiritual
* **Target Audience**: Religious Followers - Individuals who follow religious practices or are interested in spiritual ceremonies.
* **Reasoning Explanation**: The combination of visual elements such as sacred objects, floral decorations, and the act of pouring water over a revered item indicates a devotional ceremony. The audio transcript supports this by mentioning mantras associated with devotion and spirituality.

---

## 📊 Secondary Modality Evidence
* **OCR Screen Detections**:
  - *No text blocks scanned.*
* **Visual Object Detections (YOLO/CLIP)**:
  - `vase` (Confidence: 0.55)
  - `cup` (Confidence: 0.49)
  - `person` (Confidence: 0.40)
  - `Temple, shrine, or devotional place` (Confidence: 0.88)
* **Human Action Detections (VideoMAE)**:
  - *No actions classified.*
* **Audio Set Sound Events (AST)**:
  - `Music` (Confidence: 0.80)
  - `Middle eastern music` (Confidence: 0.09)

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
| **OBJECTS** | 0.87 | Foundation Model, YOLO/CLIP | Verified 2/3 elements against YOLO/CLIP modality detections. |

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
