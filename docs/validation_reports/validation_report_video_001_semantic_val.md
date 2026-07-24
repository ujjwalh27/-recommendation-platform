# Video Intelligence Engine: Human Validation Report

## Video Asset Details
* **Video ID**: `video_001_semantic_val`
* **Duration**: `63.67 seconds`

---

## 👁️ Visual Timeline & Scenes
- **Scene [0.0s - 16.0s]**: Scene keyframe 0 displaying visual elements: Bird, Bowl
- **Scene [16.0s - 22.0s]**: Scene keyframe 1 displaying visual elements: Bird, Bowl
- **Scene [22.0s - 27.0s]**: Scene keyframe 2 displaying visual elements: Bird, Bowl
- **Scene [27.0s - 31.0s]**: Scene keyframe 3 displaying visual elements: Bird, Bowl
- **Scene [31.0s - 37.0s]**: Scene keyframe 4 displaying visual elements: Bird, Bowl
- **Scene [37.0s - 43.0s]**: Scene keyframe 5 displaying visual elements: Bird, Bowl
- **Scene [43.0s - 63.7s]**: Scene keyframe 6 displaying visual elements: Bird, Bowl

---

## 🎙️ Audio Transcript (Speech-to-Text)
> I'm going to show you how to make a video for the first time in my life, but I'm not sure if I can do it or not, but it's just a little bit more fun than I thought I would be able to do it. She is a hunter, she is a hunting, she's a hunter She is the hunter I'm so nervous, so I'm feeling so much better. I feel so nervous. I to this song, thank you.

---

## 🧠 Semantic Understanding (Generated Metadata)
* **Title**: The Hunter's Journey
* **Summary**: A young woman embarks on a journey of self-discovery and adventure, learning to hunt for the first time.
* **Category**: Entertainment | **Subcategory**: How-to
* **Primary Topic**: Hunting
* **Secondary Topics**: Self-Discovery, Adventure
* **Language**: English
* **Mood**: Calm and Energetic | **Emotion**: Devotional and Happy
* **Target Audience**: Adventurers, Hunters, and those interested in learning new skills
* **Reasoning Explanation**: The spoken transcript indicates the woman is learning to hunt for the first time, which aligns with a 'How-to' category. The emotional tone suggests it's a positive experience.

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
| **CATEGORY** | 0.70 | Foundation Model | Primary VLM classification. No matching secondary sensor logs to confirm. |
| **SUBCATEGORY** | 0.65 | Foundation Model | Subcategory derived from category reasoning. Primary VLM classification. No matching secondary sensor logs to confirm. |
| **TITLE** | 0.75 | Foundation Model | Inferred context from visual representation. |
| **SUMMARY** | 0.87 | Foundation Model, Speech | Text aligns with spoken transcripts. |
| **PRIMARY_TOPIC** | 0.88 | Foundation Model, Speech | Topic 'Hunting' is spoken in the audio. |
| **LANGUAGE** | 0.99 | Foundation Model, Speech | Verified by Whisper speech transcription service language logs. |
| **MOOD** | 0.70 | Foundation Model | Visual mood interpretation. |
| **EMOTION** | 0.70 | Foundation Model | Visual mood interpretation. |
| **ACTIVITIES** | 0.65 | Foundation Model | No corroboration found for list items in secondary actions sensor logs. |
| **OBJECTS** | 0.95 | Foundation Model, YOLO/CLIP | Verified 2/2 elements against YOLO/CLIP modality detections. |

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
