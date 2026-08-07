# Video Intelligence Engine: Human Validation Report

## Video Asset Details
* **Video ID**: `video_ci_1785825070`
* **Duration**: `30.12 seconds`

---

## 👁️ Visual Timeline & Scenes
- **Scene [0.0s - 5.0s]**: Scene keyframe 0 displaying visual elements: {'type': 'Vase', 'description': 'A large golden-colored vase used to pour milk'}, {'type': 'Statue',
- **Scene [5.0s - 21.0s]**: Scene keyframe 1 displaying visual elements: {'type': 'Vase', 'description': 'A large golden-colored vase used to pour milk'}, {'type': 'Statue',
- **Scene [21.0s - 25.0s]**: Scene keyframe 2 displaying visual elements: {'type': 'Vase', 'description': 'A large golden-colored vase used to pour milk'}, {'type': 'Statue',
- **Scene [25.0s - 30.1s]**: Scene keyframe 3 displaying visual elements: {'type': 'Vase', 'description': 'A large golden-colored vase used to pour milk'}, {'type': 'Statue',

---

## 🎙️ Audio Transcript (Speech-to-Text)
> Osofapiradaradarada na mohajai Ke shouli kutilasa Bintesavaja Shiradikutilasai Tezavaja Tehra de tehra Pera de shiradai 혼자 잃을테라 그때라봐라 그디라 그 쉴하네

---

## 🧠 Semantic Understanding (Generated Metadata)
* **Title**: Devotional Ceremony in a Temple
* **Summary**: The sequence of frames captures a vibrant devotional ceremony involving the pouring of milk, colored powders, and water over statues adorned with garlands. The audio includes chanting or prayers, enhancing the spiritual ambiance.
* **Category**: Devotion | **Subcategory**: Religious Ceremony
* **Primary Topic**: A religious ritual in progress at a temple shrine
* **Secondary Topics**: Chanting, Offerings
* **Language**: English
* **Mood**: Spiritual and Reverent | **Emotion**: ['Devotional', 'Serious']
* **Target Audience**: Religious followers of Hinduism, particularly those who participate in temple worship
* **Reasoning Explanation**: The visual elements such as the pouring of milk over statues, colorful powders being thrown at them, and the presence of musical instruments suggest a religious ceremony. The audio supports this interpretation with chanting or prayers.

---

## 📊 Secondary Modality Evidence
* **OCR Screen Detections**:
  - *No text blocks scanned.*
* **Visual Object Detections (YOLO/CLIP)**:
  - `person` (Confidence: 0.65)
  - `vase` (Confidence: 0.42)
  - `Temple, shrine, or devotional place` (Confidence: 0.39)
  - `Stage with music performance` (Confidence: 0.34)
* **Human Action Detections (VideoMAE)**:
  - *No actions classified.*
* **Audio Set Sound Events (AST)**:
  - `Music` (Confidence: 0.89)

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
