# Video Intelligence Engine: Human Validation Report

## Video Asset Details
* **Video ID**: `video_ci_1784804233`
* **Duration**: `12.00 seconds`

---

## 👁️ Visual Timeline & Scenes
- **Scene [0.0s - 3.0s]**: Scene keyframe 0 displaying visual elements: Car Dashboard, Steering Wheel
- **Scene [3.0s - 7.0s]**: Scene keyframe 1 displaying visual elements: Car Dashboard, Steering Wheel
- **Scene [7.0s - 12.0s]**: Scene keyframe 2 displaying visual elements: Car Dashboard, Steering Wheel

---

## 🎙️ Audio Transcript (Speech-to-Text)
> *No audio transcript detected.*

---

## 🧠 Semantic Understanding (Generated Metadata)
* **Title**: Driving Experience
* **Summary**: A person is driving a car, selecting settings and interacting with various controls.
* **Category**: Automobile | **Subcategory**: Tech
* **Primary Topic**: Driving Experience
* **Secondary Topics**: Car Settings, Driver Interaction
* **Language**: English
* **Mood**: Informative | **Emotion**: Neutral
* **Target Audience**: Automotive enthusiasts, drivers, and technology users
* **Reasoning Explanation**: The spoken transcript mentions 'Audi drive select' and 'Set individual', indicating a driving experience with car settings. The visual frames show the person in the driver's seat interacting with controls on the dashboard.

---

## 📊 Secondary Modality Evidence
* **OCR Screen Detections**:
  - `Audi drive select | Bordbuch | Anheben | incividual | Cynamic | Car Systeme | Set individual | Goosk` (Confidence: 0.84)
* **Visual Object Detections (YOLO/CLIP)**:
  - `person` (Confidence: 0.64)
  - `Person talking to camerin reel or video` (Confidence: 0.35)
  - `Computer screen or software ui` (Confidence: 0.25)
  - `Inside of car or vehicle` (Confidence: 0.23)
  - `Outdoor natural landscape` (Confidence: 0.10)
* **Human Action Detections (VideoMAE)**:
  - *No actions classified.*
* **Audio Set Sound Events (AST)**:
  - *No sound events detected.*

---

## 📈 Provenance & Confidence Evaluation
| Field Name | Confidence Score | Evidence Sources | Algorithmic Reason / Justification |
| :--- | :--- | :--- | :--- |
| **CATEGORY** | 0.95 | Foundation Model, Vision | YOLO detected vehicles or roads. |
| **SUBCATEGORY** | 0.90 | Foundation Model, Vision | Subcategory derived from category reasoning. YOLO detected vehicles or roads. |
| **TITLE** | 0.75 | Foundation Model | Inferred context from visual representation. |
| **SUMMARY** | 0.75 | Foundation Model | Inferred context from visual representation. |
| **PRIMARY_TOPIC** | 0.70 | Foundation Model | Inferred semantic category from keyframes. |
| **LANGUAGE** | 0.80 | Foundation Model | VLM visual projection of language context. |
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
