# Video Intelligence Engine: Human Validation Report

## Video Asset Details
* **Video ID**: `video_ci_1786619012`
* **Duration**: `24.91 seconds`

---

## 👁️ Visual Timeline & Scenes
- **Scene [0.0s - 4.1s]**: Scene keyframe 0 displaying visual elements: {'name': 'Cup', 'description': 'A metallic cup used for pouring liquid.'}, {'name': 'Vase', 'descrip
- **Scene [4.1s - 8.3s]**: Scene keyframe 1 displaying visual elements: {'name': 'Cup', 'description': 'A metallic cup used for pouring liquid.'}, {'name': 'Vase', 'descrip
- **Scene [8.3s - 12.4s]**: Scene keyframe 2 displaying visual elements: {'name': 'Cup', 'description': 'A metallic cup used for pouring liquid.'}, {'name': 'Vase', 'descrip
- **Scene [12.4s - 24.9s]**: Scene keyframe 3 displaying visual elements: {'name': 'Cup', 'description': 'A metallic cup used for pouring liquid.'}, {'name': 'Vase', 'descrip

---

## 🎙️ Audio Transcript (Speech-to-Text)
> Karalauma kala kaalaun krepaalaun Guna garathan saar Paaramnatuhan Tusharatvisan kaakshan Gauram gamhi

---

## 🧠 Semantic Understanding (Generated Metadata)
* **Title**: Devotional Ceremony in a Temple
* **Summary**: The sequence of frames captures an individual performing devotional rituals within a temple setting. The person is seen pouring water from a cup into a vase, surrounded by vibrant flower garlands and golden decorations.
* **Category**: Abhishekam | **Subcategory**: Milk / Panchamrutha / Water Abhishekam
* **Primary Topic**: A religious or spiritual ceremony taking place in a sacred space
* **Secondary Topics**: Water Pouring Ceremony, Flower Garland Display
* **Language**: Hindi
* **Mood**: Solemn and Devotional | **Emotion**: Serious, Devotional
* **Target Audience**: Religious Practitioners, Spiritual Seekers
* **Reasoning Explanation**: The visual elements such as the flower garlands and golden decorations indicate a religious or spiritual context, while the actions of pouring water into a vase suggest an offering ritual. The audio track adds to this interpretation with its mention of 'Guna Garathan' which is associated with Hindu devotional practices.

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
| **CATEGORY** | 0.70 | Foundation Model | Primary VLM classification. No matching secondary sensor logs to confirm. |
| **SUBCATEGORY** | 0.65 | Foundation Model | Subcategory derived from category reasoning. Primary VLM classification. No matching secondary sensor logs to confirm. |
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
