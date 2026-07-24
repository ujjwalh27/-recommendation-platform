# Production Risk Register (Unseen Real-World Conditions)

## Risk Matrix

| Risk ID | Risk Description | Severity | Probability | Operational Impact | Recommended Mitigation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **R-01** | **Heavy Camera Shake / Motion Blur** | High | Medium | Reduces keyframe Laplacian sharpness below 100 (-12% recall). | Enable frame-dropping filter in preprocessor for blurry frames. |
| **R-02** | **Extreme Low-Light / Dark Scenes** | Medium | Medium | Triggers minor background over-generalization (+3.8% overconfidence). | Apply CLAHE contrast enhancement before VLM input. |
| **R-03** | **Multilingual Dialect / Heavy Accents** | Medium | Low | Degrades Whisper transcript accuracy for niche regional dialects. | Fall back to Vision + OCR evidence fusion. |
| **R-04** | **Unseen Niche Video Domains** | Low | Low | Slightly lower classification precision in dense medical/scientific clips. | Expand domain ontology in Knowledge Base. |
