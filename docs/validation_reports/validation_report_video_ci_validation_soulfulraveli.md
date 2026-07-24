# Video Intelligence Engine: Human Validation Report

## Video Asset Details
* **Video ID**: `video_ci_validation_soulfulraveli`
* **Duration**: `18.70 seconds`

---

## 👁️ Visual Timeline & Scenes
- **Scene [0.0s - 2.0s]**: Scene keyframe 0 displaying visual elements: Microphone, Bowl of water for ablutions
- **Scene [2.0s - 7.0s]**: Scene keyframe 1 displaying visual elements: Microphone, Bowl of water for ablutions
- **Scene [7.0s - 10.0s]**: Scene keyframe 2 displaying visual elements: Microphone, Bowl of water for ablutions
- **Scene [10.0s - 12.0s]**: Scene keyframe 3 displaying visual elements: Microphone, Bowl of water for ablutions
- **Scene [12.0s - 14.0s]**: Scene keyframe 4 displaying visual elements: Microphone, Bowl of water for ablutions
- **Scene [14.0s - 17.0s]**: Scene keyframe 5 displaying visual elements: Microphone, Bowl of water for ablutions
- **Scene [17.0s - 18.7s]**: Scene keyframe 6 displaying visual elements: Microphone, Bowl of water for ablutions

---

## 🎙️ Audio Transcript (Speech-to-Text)
> Saga sets varupan jidalan da kandam jagat sam bahvastana samhara hitam soabhati chayaman shandesh yantam

---

## 🧠 Semantic Understanding (Generated Metadata)
* **Title**: The Sacred Chant: A Devotional Performance
* **Summary**: In a serene stage setting, a man leads an audience in a devotional chant accompanied by music. The scene transitions from the office desk environment to a more spiritual atmosphere.
* **Category**: Lifestyle | **Subcategory**: Devotionals and Spiritual Practices
* **Primary Topic**: Chanting and Devotional Performances
* **Secondary Topics**: Office Environment, Music Performance
* **Language**: Hindi
* **Mood**: Calm and Devotional | **Emotion**: Devotional
* **Target Audience**: Religious Groups, Spiritual Seekers
* **Reasoning Explanation**: The visual cues of the man leading a chant in an office setting with music performance indicate this is likely a devotional performance aimed at religious or spiritual audiences.

---

## 📊 Secondary Modality Evidence
* **OCR Screen Detections**:
  - `8249.00` (Confidence: 0.70)
* **Visual Object Detections (YOLO/CLIP)**:
  - `bowl` (Confidence: 0.66)
  - `vase` (Confidence: 0.62)
  - `person` (Confidence: 0.60)
  - `knife` (Confidence: 0.55)
  - `teddy bear` (Confidence: 0.53)
  - `bottle` (Confidence: 0.47)
  - `potted plant` (Confidence: 0.46)
  - `fire hydrant` (Confidence: 0.40)
  - `Stage with music performance` (Confidence: 0.47)
  - `Office desk environment` (Confidence: 0.37)
* **Human Action Detections (VideoMAE)**:
  - *No actions classified.*
* **Audio Set Sound Events (AST)**:
  - `Music` (Confidence: 0.57)
  - `Mantra` (Confidence: 0.37)

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
