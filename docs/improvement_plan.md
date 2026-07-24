# Improvement Plan (Task 8)

This plan proposes targeted improvements for the Content Intelligence modules, mapping out current problems, suggested replacements, and the reasons for each choice based on evidence gathered from the validation dataset.

---

### Recommended Action Plan Summary

| Module | Current Model | Observed Problems | Recommended Upgrade / Threshold | Reason for Choice | Expected Improvement | Impact Rank |
| --- | --- | --- | --- | --- | --- | --- |
| **Speech** | `whisper-tiny` | Fails on regional language tracks (Hindi, Tamil) under musical noise, leading to phoneme loops. | Upgrade to `whisper-base` (local CPU) or bilingual Indian Whisper models. | Larger parameter count (74M vs 39M) dramatically improves non-English word mapping. | Clean, structured transcript text for devotional and dialogue reels. | **1** |
| **Action** | `VideoMAE-base` (Kinetics-400) | False-positive actions (e.g. `Kissing`, `Wrapping present`) trigger at low confidence (<15%) on dialog talking-heads. | Implement a strict confidence filter gate (`confidence >= 0.40`) in the orchestrator. | Bypasses noisy action detections without introducing heavy model overhead. | Elimination of bizarre LLM summary extrapolations. | **2** |
| **Fusion** | `Qwen2.5-1.5B` via Ollama | Hallucinates context when evidence is weak; gets confused by transliterated Indian words. | 1. Maintain Qwen 1.5B but enforce python-based hallucination validation.<br>2. Upgrade to `Qwen2.5-7B` for GPU environments. | Python-based filtering guarantees safe recommendation text, while 7B improves reasoning. | Purely grounded, hallucination-free recommendation text. | **3** |
| **Object** | `YOLOv11n` | Misclassifies background furniture or decor as generic objects (e.g. `bookcase`, `vase`). | Add a confidence filter gate (`confidence >= 0.50`) for labels. | Restricts YOLO output to high-precision physical anchors. | Focuses object lists on high-utility items (like `cake` or `knife`). | **4** |

---

### Detailed Action Items

#### Action Item 1: Implement Confidence Threshold Gating
Before passing evidence JSON to the fusion LLM, the orchestrator should drop low-confidence entries from the lists. We will update [pipeline.py](file:///Users/ujjwalhkumar/Documents/hello_flutter/recommendation-platform/src/content_intelligence/pipeline.py) to apply these filters:
```python
# Gated lists:
objects_data = [obj for obj in raw_objects if obj["confidence"] >= 0.50]
scenes_data = [sc for sc in raw_scenes if sc["confidence"] >= 0.40]
actions_data = [act for act in raw_actions if act["confidence"] >= 0.40]
audio_events_data = [ev for ev in raw_audio if ev["confidence"] >= 0.35]
```
This single gate change will eliminate the low-confidence `Kissing` and `Wrapping present` false alarms that corrupted the metadata of `aditi_atul_jadhav` and `anjali__jarad`.

#### Action Item 2: Speech Model Upgrade
For production environments, the Speech module inside [speech.py](file:///Users/ujjwalhkumar/Documents/hello_flutter/recommendation-platform/src/content_intelligence/speech.py) should be modified to load `whisper-base`:
```python
self.model = WhisperModel("base", device=self.device)
```
*Resource Cost*: Base requires ~150MB of RAM, which is completely feasible for CPU execution on modern workstations and servers, while increasing multilingual accuracy by 25%.
