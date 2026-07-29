# Video Intelligence Engine: Human Validation Report

## Video Asset Details
* **Video ID**: `test_run_aditi`
* **Duration**: `63.67 seconds`

---

## 👁️ Visual Timeline & Scenes
- **Scene [0.0s - 16.0s]**: Scene keyframe 0 displaying visual elements: {'description': 'A bowl filled with yellow marigold flowers.', 'role': 'Offering'}, {'description': 
- **Scene [16.0s - 22.0s]**: Scene keyframe 1 displaying visual elements: {'description': 'A bowl filled with yellow marigold flowers.', 'role': 'Offering'}, {'description': 
- **Scene [22.0s - 27.0s]**: Scene keyframe 2 displaying visual elements: {'description': 'A bowl filled with yellow marigold flowers.', 'role': 'Offering'}, {'description': 
- **Scene [27.0s - 31.0s]**: Scene keyframe 3 displaying visual elements: {'description': 'A bowl filled with yellow marigold flowers.', 'role': 'Offering'}, {'description': 
- **Scene [31.0s - 37.0s]**: Scene keyframe 4 displaying visual elements: {'description': 'A bowl filled with yellow marigold flowers.', 'role': 'Offering'}, {'description': 
- **Scene [37.0s - 43.0s]**: Scene keyframe 5 displaying visual elements: {'description': 'A bowl filled with yellow marigold flowers.', 'role': 'Offering'}, {'description': 
- **Scene [43.0s - 63.7s]**: Scene keyframe 6 displaying visual elements: {'description': 'A bowl filled with yellow marigold flowers.', 'role': 'Offering'}, {'description': 

---

## 🎙️ Audio Transcript (Speech-to-Text)
> I'm going to show you how to make a video for the first time in my life, but I'm not sure if I can do it or not, but it's just a little bit more fun than I thought I would be able to do it. She is a hunter, she is a hunting, she's a hunter She is the hunter I'm so nervous, so I'm feeling so much better. I feel so nervous. I to this song, thank you.

---

## 🧠 Semantic Understanding (Generated Metadata)
* **Title**: Devotional Ceremony at a Hindu Temple
* **Summary**: The sequence of frames depicts an individual performing devotional rituals in front of a temple altar, adorned with various religious items. The person is seen offering flowers and incense as part of the ceremony.
* **Category**: Devotion | **Subcategory**: Religious Ceremony
* **Primary Topic**: Hindu Devotional Practices
* **Secondary Topics**: Offering Flowers, Incense Burning
* **Language**: English
* **Mood**: Calm and Spiritual | **Emotion**: Serious, Devotional
* **Target Audience**: Individuals interested in Hindu religious practices.
* **Reasoning Explanation**: The video captures a moment of devotion with the woman performing rituals at an altar adorned with various religious items. The audio and visual elements suggest a serene, spiritual atmosphere focused on devotional activities within a temple setting.

---

## 📊 Secondary Modality Evidence
* **OCR Screen Detections**:
  - `4 | 0 | 3` (Confidence: 0.59)
* **Visual Object Detections (YOLO/CLIP)**:
  - `person` (Confidence: 0.65)
  - `bowl` (Confidence: 0.52)
  - `bird` (Confidence: 0.47)
  - `Temple, shrine, or devotional place` (Confidence: 0.70)
  - `Kitchen cooking set` (Confidence: 0.13)
* **Human Action Detections (VideoMAE)**:
  - *No actions classified.*
* **Audio Set Sound Events (AST)**:
  - `Speech` (Confidence: 0.30)
  - `Music` (Confidence: 0.27)

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
| **OBJECTS** | 0.78 | Foundation Model, YOLO/CLIP | Verified 1/3 elements against YOLO/CLIP modality detections. |

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
