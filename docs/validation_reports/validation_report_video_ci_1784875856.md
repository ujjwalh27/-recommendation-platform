# Video Intelligence Engine: Human Validation Report

## Video Asset Details
* **Video ID**: `video_ci_1784875856`
* **Duration**: `16.00 seconds`

---

## 👁️ Visual Timeline & Scenes
- **Scene [0.0s - 2.6s]**: Scene keyframe 0 displaying visual elements: {'name': 'Table Tennis Table'}, {'name': 'Audience Seating Area'}
- **Scene [2.6s - 5.3s]**: Scene keyframe 1 displaying visual elements: {'name': 'Table Tennis Table'}, {'name': 'Audience Seating Area'}
- **Scene [5.3s - 8.0s]**: Scene keyframe 2 displaying visual elements: {'name': 'Table Tennis Table'}, {'name': 'Audience Seating Area'}
- **Scene [8.0s - 10.6s]**: Scene keyframe 3 displaying visual elements: {'name': 'Table Tennis Table'}, {'name': 'Audience Seating Area'}
- **Scene [10.6s - 13.3s]**: Scene keyframe 4 displaying visual elements: {'name': 'Table Tennis Table'}, {'name': 'Audience Seating Area'}
- **Scene [13.3s - 16.0s]**: Scene keyframe 5 displaying visual elements: {'name': 'Table Tennis Table'}, {'name': 'Audience Seating Area'}
- **Scene [16.0s - 16.0s]**: Scene keyframe 6 displaying visual elements: {'name': 'Table Tennis Table'}, {'name': 'Audience Seating Area'}

---

## 🎙️ Audio Transcript (Speech-to-Text)
> Il y a un petit peu de temps, c'est vrai que ça t'a fait très vite, ça va vite. C'est le point qu'il dépense à l'heure.

---

## 🧠 Semantic Understanding (Generated Metadata)
* **Title**: Table Tennis Match in a Gymnasium
* **Summary**: The video captures an intense table tennis match between two players, with one player executing a powerful serve. The environment is that of a professional indoor sports arena, complete with branding and audience presence.
* **Category**: Sports | **Subcategory**: Table Tennis Competition
* **Primary Topic**: Table Tennis Match
* **Secondary Topics**: Professional Sports, Indoor Gymnasium
* **Language**: English
* **Mood**: Energetic and Competitive | **Emotion**: Serious, Concentrated
* **Target Audience**: Table Tennis Enthusiasts, Sports Fans
* **Reasoning Explanation**: 

---

## 📊 Secondary Modality Evidence
* **OCR Screen Detections**:
  - `LIEBHERR | OPEL` (Confidence: 0.69)
* **Visual Object Detections (YOLO/CLIP)**:
  - `person` (Confidence: 0.70)
  - `bench` (Confidence: 0.53)
  - `backpack` (Confidence: 0.36)
  - `Gym or athletic field` (Confidence: 0.29)
  - `Audition or performance setup` (Confidence: 0.24)
  - `Stage with music performance` (Confidence: 0.22)
  - `Computer screen or software ui` (Confidence: 0.14)
* **Human Action Detections (VideoMAE)**:
  - *No actions classified.*
* **Audio Set Sound Events (AST)**:
  - `Speech` (Confidence: 0.60)
  - `Basketball bounce` (Confidence: 0.26)

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
