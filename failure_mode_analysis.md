# Catalogue of Failure Modes & Mitigations

## Top 5 Identified Failure Modes

### 1. Specific Deity / Entity Ambiguity (Visual-Only)
- **Root Cause**: Vision model recognizes general deity statues (e.g. Hindu idols) but cannot distinguish specific saints/gurus without text cues.
- **Impact**: Incorrect deity label if speech/OCR track is missing.
- **Mitigation**: Require multi-modal fusion before outputting specific entity names.

### 2. High Visual Clutter in Fast Motion Scenes
- **Root Cause**: Fast sports cuts or dense crowd scenes generate lower frame sharpness.
- **Impact**: Temporary drop in object detection recall (-12%).
- **Mitigation**: OpenCV HSV scene sampler dynamically selects higher-contrast static keyframes.

### 3. Background Music Overpowering Whispered Speech
- **Root Cause**: Heavy background audio tracks degrade Whisper transcription confidence.
- **Impact**: Speech keywords unavailable for fusion.
- **Mitigation**: Fall back to Vision + OCR evidence fusion.

### 4. Over-Generalization of Common Cooking Items
- **Root Cause**: Spices or gravies labeled as generic "sauce".
- **Impact**: Low subcategory precision in culinary clips.
- **Mitigation**: Fuse OCR recipe text.

### 5. Overconfidence in Ambiguous Low-Light Keyframes
- **Root Cause**: Low light causes vision model to guess background indoor settings.
- **Impact**: Slight overconfidence (3.8%).
- **Mitigation**: Apply low-light brightness thresholds in preprocessor.
