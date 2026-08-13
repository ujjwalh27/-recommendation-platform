# Video Intelligence Engine: Human Validation Report

## Video Asset Details
* **Video ID**: `video_ci_1786440913`
* **Duration**: `13.47 seconds`

---

## 👁️ Visual Timeline & Scenes
- **Scene [0.0s - 10.0s]**: Scene keyframe 0 displaying visual elements: {'name': 'Clay pot', 'description': 'Used for pouring water during the ceremony.'}, {'name': 'Stone 
- **Scene [10.0s - 13.5s]**: Scene keyframe 1 displaying visual elements: {'name': 'Clay pot', 'description': 'Used for pouring water during the ceremony.'}, {'name': 'Stone 

---

## 🎙️ Audio Transcript (Speech-to-Text)
> 喜歡呀後裏 問的那陣子屬於呀呀 等下快樂 哪是快樂死裏了 等他呀

---

## 🧠 Semantic Understanding (Generated Metadata)
* **Title**: Devotional Ceremony at a Shrine
* **Summary**: The video captures individuals performing a devotional ceremony involving pouring water and placing flowers around a stone structure in what appears to be a temple or shrine setting.
* **Category**: Pooja | **Subcategory**: Devotional Ritual & Worship
* **Primary Topic**: A religious ritual at a sacred site
* **Secondary Topics**: Water Pouring Ceremony, Offerings
* **Language**: English
* **Mood**: Solemn and Devotional | **Emotion**: ['Devotional', 'Serious']
* **Target Audience**: Individuals interested in religious practices and ceremonies
* **Reasoning Explanation**: The visual cues of pouring water, placing flowers around a sacred stone structure, along with the audio content mentioning devotion and rituals indicate that this video captures a moment from a devotional ceremony at a temple or shrine.

---

## 📊 Secondary Modality Evidence
* **OCR Screen Detections**:
  - *No text blocks scanned.*
* **Visual Object Detections (YOLO/CLIP)**:
  - `person` (Confidence: 0.74)
  - `cake` (Confidence: 0.37)
  - `Temple, shrine, or devotional place` (Confidence: 0.73)
  - `Person talking to camerin reel or video` (Confidence: 0.16)
* **Human Action Detections (VideoMAE)**:
  - *No actions classified.*
* **Audio Set Sound Events (AST)**:
  - `Music` (Confidence: 0.54)
  - `Mantra` (Confidence: 0.39)

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
