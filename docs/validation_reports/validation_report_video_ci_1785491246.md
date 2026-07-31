# Video Intelligence Engine: Human Validation Report

## Video Asset Details
* **Video ID**: `video_ci_1785491246`
* **Duration**: `30.07 seconds`

---

## 👁️ Visual Timeline & Scenes
- **Scene [0.0s - 5.0s]**: Scene keyframe 0 displaying visual elements: {'description': 'A large lamp being filled with oil by a person', 'location': 'Center of the frame'}
- **Scene [5.0s - 16.0s]**: Scene keyframe 1 displaying visual elements: {'description': 'A large lamp being filled with oil by a person', 'location': 'Center of the frame'}
- **Scene [16.0s - 20.0s]**: Scene keyframe 2 displaying visual elements: {'description': 'A large lamp being filled with oil by a person', 'location': 'Center of the frame'}
- **Scene [20.0s - 30.1s]**: Scene keyframe 3 displaying visual elements: {'description': 'A large lamp being filled with oil by a person', 'location': 'Center of the frame'}

---

## 🎙️ Audio Transcript (Speech-to-Text)
> சடாட்ட வீகலைத்தில் பிரமாக வீதுச் சென்றி, கலை வளம் விலம் மிதம் உங்களுக்கு மாலைக் காண்டும் தமாற்றாம் கிடம் நீ நாத்வாக் தமரு வையம் காரைச்ச் செல்லதான் உங்களுக்கும் தன்றுவிட்டு வந்து நாம் கேட்வாக வேண்டாம்.

---

## 🧠 Semantic Understanding (Generated Metadata)
* **Title**: Devotional Ceremony in a Temple
* **Summary**: The sequence of frames depicts individuals participating in a devotional ceremony at a temple, involving rituals with sacred objects such as lamps and offerings. The audio suggests that the video is part of a larger spiritual or religious event.
* **Category**: Devotion | **Subcategory**: Religious Ceremony
* **Primary Topic**: A ceremonial ritual taking place inside a temple
* **Secondary Topics**: Temple rituals, Offerings
* **Language**: English
* **Mood**: Spiritual and reverent | **Emotion**: ['Devotional']
* **Target Audience**: Religious practitioners, devotees of Hinduism
* **Reasoning Explanation**: The visual elements such as the sacred object being anointed with oil, individuals in traditional attire performing prayers, and ornate decorations indicate a religious ceremony. The audio content reinforces this by mentioning devotion and rituals.

---

## 📊 Secondary Modality Evidence
* **OCR Screen Detections**:
  - *No text blocks scanned.*
* **Visual Object Detections (YOLO/CLIP)**:
  - `Temple, shrine, or devotional place` (Confidence: 0.64)
  - `Person talking to camerin reel or video` (Confidence: 0.13)
  - `Kitchen cooking set` (Confidence: 0.11)
* **Human Action Detections (VideoMAE)**:
  - *No actions classified.*
* **Audio Set Sound Events (AST)**:
  - `Music` (Confidence: 0.74)
  - `Folk music` (Confidence: 0.10)

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
