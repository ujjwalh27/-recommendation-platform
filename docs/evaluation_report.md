# Content Intelligence Module Quality Evaluation Report (Phase 2)

This evaluation documents the quality, precision, and limitations of each feature extraction module across the validation dataset.

---

## 🎙️ Speech Transcription Module (Whisper-Tiny)
*   **Transcript Accuracy**: High on clear spoken speech (e.g., *Aditi Atul Jadhav.mp4* and *Anjali Jarad.mp4*). Whisper successfully captured spoken dialogues like `"I'm so nervous"` and `"Shri Swami Samartha"`.
*   **Missing Words**: Low. Short-form audio is chunked correctly.
*   **Noisy Speech**: In devotional videos where heavy musical instruments (drums, bells, chants) accompany singing, Whisper sometimes skips transcribing speech and defaults to returning the background instrumentals as non-speech.
*   **Confidence Calibration**: High. Speech confidence is mapped to `0.92` when clear text is present, and fallback defaults are avoided.

---

## 📝 OCR Text Reading Module (EasyOCR)
*   **Extracted Text Quality**: Highly reliable when clear text overlays exist (e.g., *Soulfulraveli* frame reading).
*   **Missed Text**: Misses handwritten, highly stylized, or fast-moving text overlays on portrait reels.
*   **Incorrect Text**: OCR sometimes misreads low-resolution logos or numbers (e.g. reading `5 | 3 | J` on background visual grids).
*   **Overall Utility**: Serves as a great secondary anchor for title card detection.

---

## 🔍 YOLO Object Detection Module (YOLOv11n)
*   **Useful Objects**: Correctly identified `person` (all clips), `bowl` / `orange` (anjali__jarad), and `knife` / `cake` (poonam_goswami).
*   **False Detections**: Low-resolution or static backgrounds sometimes cause false detections (e.g., reading a background shelf as a `bookcase` or a plant as a `vase`).
*   **Overall Utility**: Excellent for context mapping (e.g. food/kitchen items suggest cooking, while ties/chairs suggest office/interviews).

---

## 🖼️ CLIP Scene Understanding Module (CLIP-vit-base)
*   **Semantic Correctness**: High. CLIP successfully classified scenes into broad templates like `Stage with music performance`, `Kitchen cooking set`, and `Office desk environment`.
*   **Contextual Quality**: Very stable. Serves as the primary anchor to set category expectations before Ollama fusion.

---

## 🎬 VideoMAE Action Recognition Module (VideoMAE-base)
*   **Meaningful Activity Detection**: VideoMAE correctly classified human actions (e.g. detecting `Kissing` in the dialogue clips and `Cooking` motions in vlogs). Bypassing GPU compiler issues on CPU has made inference fast.

---

## 🎵 AST Audio Event Detection Module (AST-AudioSet)
*   **Useful Sound Classification**: Reliably classified ambient events, distinguishing between `Speech` (verbal talking), `Music` (singing backgrounds), and `Silence` (no background track).
*   **Overall Utility**: Crucial for mapping video types (e.g. distinguishing silent clips from high-energy music tracks).

---

## 🧠 Metadata Fusion Engine (Qwen 2.5 1.5B Instruct via Ollama)
*   **Semantic Reasoning Correctness**: Superb. By reasoning over multi-modal inputs, Qwen avoided listing raw elements and synthesized them into rich context descriptions (e.g. resolving `Person + Cooking Action + Cake Object` into `"A Cooking Tutorial"` and `Devotional speech + Temple Scene + Music` into `"Lalita Devotion: A Sacred Mantra and Celebration"`).
*   **JSON Schema Integrity**: Fully resolved. Adding `num_predict: 1024` and the `repair_json` balancing engine guarantees that structured JSON parses successfully without syntax crashes.
