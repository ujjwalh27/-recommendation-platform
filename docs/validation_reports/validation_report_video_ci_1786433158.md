# Video Intelligence Engine: Human Validation Report

## Video Asset Details
* **Video ID**: `video_ci_1786433158`
* **Duration**: `22.03 seconds`

---

## 👁️ Visual Timeline & Scenes
- **Scene [0.0s - 14.0s]**: Scene keyframe 0 displaying visual elements: Bottle, Person in red attire
- **Scene [14.0s - 17.0s]**: Scene keyframe 1 displaying visual elements: Bottle, Person in red attire
- **Scene [17.0s - 18.0s]**: Scene keyframe 2 displaying visual elements: Bottle, Person in red attire
- **Scene [18.0s - 22.0s]**: Scene keyframe 3 displaying visual elements: Bottle, Person in red attire

---

## 🎙️ Audio Transcript (Speech-to-Text)
> Chari bazaar, Karoli kishori rahe Omaklipal saris karihamaari Omaklepal sarisarihamaani Parikaraya marali kishuri rahe Kari kaoya malori kishore rahe

---

## 🧠 Semantic Understanding (Generated Metadata)
* **Title**: Devotional Gathering at a Temple
* **Summary**: The video captures scenes from a large gathering in front of an ornate temple, where people are engaged in singing bhajans (devotional songs). The atmosphere is lively and spiritual. A close-up shot shows a colorful painting depicting Hindu deities, indicating the religious context. Another frame focuses on worshippers observing a decorated shrine with intricate decorations.
* **Category**: Bhajan | **Subcategory**: Devotional Hymns & Songs
* **Primary Topic**: Bhajan Singing at a Temple
* **Secondary Topics**: Hindu Devotional Songs, Temple Gathering
* **Language**: Hindi
* **Mood**: Spiritual and Energetic | **Emotion**: Devotional, Happy
* **Target Audience**: Individuals interested in Hindu devotional practices
* **Reasoning Explanation**: The video showcases a vibrant religious event with people actively participating in singing bhajans and observing temple rituals. The presence of the deity painting suggests that it is set within a Hindu context, emphasizing devotion.

---

## 📊 Secondary Modality Evidence
* **OCR Screen Detections**:
  - `THIS BHAJAN >>>>` (Confidence: 0.59)
  - `HERE` (Confidence: 0.48)
  - `MERE_RAM;` (Confidence: 0.64)
* **Visual Object Detections (YOLO/CLIP)**:
  - `bottle` (Confidence: 0.76)
  - `person` (Confidence: 0.64)
  - `Temple, shrine, or devotional place` (Confidence: 0.59)
  - `Stage with music performance` (Confidence: 0.33)
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
