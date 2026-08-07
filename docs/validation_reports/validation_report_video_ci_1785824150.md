# Video Intelligence Engine: Human Validation Report

## Video Asset Details
* **Video ID**: `video_ci_1785824150`
* **Duration**: `22.03 seconds`

---

## 👁️ Visual Timeline & Scenes
- **Scene [0.0s - 14.0s]**: Scene keyframe 0 displaying visual elements: {'name': 'Bottle'}, {'name': 'Camera or phone being used to record the event.'}
- **Scene [14.0s - 17.0s]**: Scene keyframe 1 displaying visual elements: {'name': 'Bottle'}, {'name': 'Camera or phone being used to record the event.'}
- **Scene [17.0s - 18.0s]**: Scene keyframe 2 displaying visual elements: {'name': 'Bottle'}, {'name': 'Camera or phone being used to record the event.'}
- **Scene [18.0s - 22.0s]**: Scene keyframe 3 displaying visual elements: {'name': 'Bottle'}, {'name': 'Camera or phone being used to record the event.'}

---

## 🎙️ Audio Transcript (Speech-to-Text)
> Chari bazaar, Karoli kishori rahe Omaklipal saris karihamaari Omaklepal sarisarihamaani Parikaraya marali kishuri rahe Kari kaoya malori kishore rahe

---

## 🧠 Semantic Understanding (Generated Metadata)
* **Title**: Devotional Gathering at a Temple
* **Summary**: The video captures scenes from an indoor temple where devotees gather for worship. The sequence includes close-ups of religious art, the main deity's idol, and people engaged in prayer or singing bhajans.
* **Category**: Religion | **Subcategory**: Devotion
* **Primary Topic**: Worship at a Hindu Temple
* **Secondary Topics**: Bhajan, Deity Worship
* **Language**: Hindi
* **Mood**: Calm and Spiritual | **Emotion**: Devotional, Reverent
* **Target Audience**: Hindu devotees
* **Reasoning Explanation**: The video showcases a religious event with people engaged in worship activities such as chanting bhajans and praying at an ornately decorated temple. The presence of specific deities' artwork, the main deity's idol, and the crowd indicates it is likely during a significant festival or regular devotion time.

---

## 📊 Secondary Modality Evidence
* **OCR Screen Detections**:
  - `HERE` (Confidence: 0.48)
  - `MERE_RAM;` (Confidence: 0.64)
* **Visual Object Detections (YOLO/CLIP)**:
  - `bottle` (Confidence: 0.76)
  - `person` (Confidence: 0.61)
  - `Temple, shrine, or devotional place` (Confidence: 0.58)
  - `Person talking to camerin reel or video` (Confidence: 0.22)
  - `Stage with music performance` (Confidence: 0.16)
* **Human Action Detections (VideoMAE)**:
  - *No actions classified.*
* **Audio Set Sound Events (AST)**:
  - `Music` (Confidence: 0.73)
  - `Folk music` (Confidence: 0.07)
  - `Music of bollywood` (Confidence: 0.06)

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
