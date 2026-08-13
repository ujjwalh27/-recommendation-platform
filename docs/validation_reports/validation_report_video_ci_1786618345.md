# Video Intelligence Engine: Human Validation Report

## Video Asset Details
* **Video ID**: `video_ci_1786618345`
* **Duration**: `29.20 seconds`

---

## 👁️ Visual Timeline & Scenes
- **Scene [0.0s - 1.0s]**: Scene keyframe 0 displaying visual elements: {'name': 'Ornate idol of a deity, adorned with jewelry and floral garlands'}, {'name': 'Decorative f
- **Scene [1.0s - 16.0s]**: Scene keyframe 1 displaying visual elements: {'name': 'Ornate idol of a deity, adorned with jewelry and floral garlands'}, {'name': 'Decorative f
- **Scene [16.0s - 17.0s]**: Scene keyframe 2 displaying visual elements: {'name': 'Ornate idol of a deity, adorned with jewelry and floral garlands'}, {'name': 'Decorative f
- **Scene [17.0s - 29.2s]**: Scene keyframe 3 displaying visual elements: {'name': 'Ornate idol of a deity, adorned with jewelry and floral garlands'}, {'name': 'Decorative f

---

## 🎙️ Audio Transcript (Speech-to-Text)
> پل پل مجھے دو غائی جاتے ہیں جاقتے ہے جا تجید جید ہارو یہ اپنان پر آن برایڈ جاہتے ہو جایتے گا جا چیدی دو خارویی اپناان پروڈ

---

## 🧠 Semantic Understanding (Generated Metadata)
* **Title**: Devotional Celebration at a Temple
* **Summary**: The sequence of frames captures a vibrant devotional celebration taking place in front of an ornately decorated shrine. Individuals are seen participating in the ceremony, holding lit candles and engaging with offerings such as sweets and flowers.
* **Category**: Pooja | **Subcategory**: Devotional Ritual & Worship
* **Primary Topic**: A religious or spiritual event centered around a deity's idol at a temple.
* **Secondary Topics**: Celebration, Offerings
* **Language**: English
* **Mood**: Spiritual and Devotional | **Emotion**: Serious, Reverent
* **Target Audience**: Religious Followers, Cultural Enthusiasts
* **Reasoning Explanation**: The visual elements such as the decorated shrine and participants holding lit candles indicate a religious celebration, while the audio transcription suggests singing or chanting associated with devotion.

---

## 📊 Secondary Modality Evidence
* **OCR Screen Detections**:
  - *No text blocks scanned.*
* **Visual Object Detections (YOLO/CLIP)**:
  - `bowl` (Confidence: 0.61)
  - `person` (Confidence: 0.51)
  - `dining table` (Confidence: 0.48)
  - `Temple, shrine, or devotional place` (Confidence: 0.89)
  - `Stage with music performance` (Confidence: 0.10)
* **Human Action Detections (VideoMAE)**:
  - `Celebrating` (Confidence: 0.33)
* **Audio Set Sound Events (AST)**:
  - `Music` (Confidence: 0.83)
  - `Singing` (Confidence: 0.06)

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
| **ACTIVITIES** | 0.78 | Foundation Model, VideoMAE | Verified 1/3 elements against VideoMAE modality detections. |
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
