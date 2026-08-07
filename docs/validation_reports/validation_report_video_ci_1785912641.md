# Video Intelligence Engine: Human Validation Report

## Video Asset Details
* **Video ID**: `video_ci_1785912641`
* **Duration**: `16.02 seconds`

---

## 👁️ Visual Timeline & Scenes
- **Scene [0.0s - 7.7s]**: Scene keyframe 0 displaying visual elements: {'name': 'Trophy', 'description': 'A golden trophy held by players'}, {'microphone': 'Media micropho
- **Scene [7.7s - 16.0s]**: Scene keyframe 1 displaying visual elements: {'name': 'Trophy', 'description': 'A golden trophy held by players'}, {'microphone': 'Media micropho

---

## 🎙️ Audio Transcript (Speech-to-Text)
> I was just so happy and everyone, it just was such a good feeling. Everything was coming together. Everything was just right and that doesn't happen all the time. So that feeling, I'll never forget.

---

## 🧠 Semantic Understanding (Generated Metadata)
* **Title**: Celebration of a Women's Soccer Victory
* **Summary**: The sequence captures the joyous celebration following a women's soccer victory, with players holding up trophies amidst confetti. An interview is also shown where one player expresses her happiness and gratitude for the moment.
* **Category**: Sports | **Subcategory**: Soccer
* **Primary Topic**: Women's Soccer Victory Celebration
* **Secondary Topics**: Team Unity, Achievement
* **Language**: English
* **Mood**: Energetic | **Emotion**: [{'description': 'Happiness and Gratitude'}]
* **Target Audience**: Soccer Fans, Sports Enthusiasts
* **Reasoning Explanation**: 

---

## 📊 Secondary Modality Evidence
* **OCR Screen Detections**:
  - *No text blocks scanned.*
* **Visual Object Detections (YOLO/CLIP)**:
  - `person` (Confidence: 0.56)
  - `Gym or athletic field` (Confidence: 0.58)
  - `Person talking to camerin reel or video` (Confidence: 0.40)
* **Human Action Detections (VideoMAE)**:
  - *No actions classified.*
* **Audio Set Sound Events (AST)**:
  - `Speech` (Confidence: 0.77)

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
