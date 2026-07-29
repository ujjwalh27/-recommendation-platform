"""
Task 1 – VLM Provider Registry
Configurable multi-backend VLM client that reads from vlm_model_config.yaml.
Supports MiniCPM-V, Qwen2.5-VL, InternVL3, and any Ollama-compatible model.
The downstream SRCDE, HRCE, and taxonomy pipeline remain completely unchanged.
"""
import os
import json
import base64
import urllib.request
from typing import List, Dict, Any

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "config", "vlm_model_config.yaml")


def load_vlm_config() -> Dict[str, Any]:
    """Loads the active VLM configuration from vlm_model_config.yaml."""
    if YAML_AVAILABLE and os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            return yaml.safe_load(f) or {}
    # Fallback defaults if YAML not available
    return {
        "vision_model": {
            "provider": "qwen",
            "model": "Qwen2.5-VL-7B",
            "ollama_url": "http://localhost:11434/api/chat",
            "temperature": 0.10,
            "timeout_sec": 120,
            "max_frames": 7
        }
    }


# ─────────────────────────────────────────────────────────────────────────────
# Prompt Templates (from VLM-CEF Prompt Library)
# ─────────────────────────────────────────────────────────────────────────────

PROMPT_B_SYSTEM = (
    "You are a precise visual observation extractor. Report ONLY what you can directly observe "
    "in the frames. Do NOT infer ritual names or categories. Return ONLY valid JSON."
)

PROMPT_B_USER = """Analyze the video frames and return a JSON object with exactly these fields:
{
  "idol_visible": "<description or null>",
  "people_count": <integer>,
  "liquids_visible": ["<liquid types observed>"],
  "flowers_visible": <true/false>,
  "lamp_visible": <true/false>,
  "fire_visible": <true/false>,
  "pouring_action": <true/false>,
  "offering_flowers": <true/false>,
  "chanting_visible": <true/false>,
  "musical_instruments": ["<instruments observed>"],
  "text_detected": ["<screen text observed>"],
  "confidence": <0.0-1.0>
}"""

PROMPT_C_USER = """Analyze these video frames showing Hindu devotional content and return a JSON classification:
{
  "content_type": "<Ritual|Music|Discourse|Temple|Festival|Unknown>",
  "primary_class": "<Abhishekam|Aarti|Pooja|Archana|Bhajan|Pravachan|Temple Darshan|Festival Procession|Unknown>",
  "secondary_classes": ["<additional activities observed>"],
  "confidence": <0.0-1.0>,
  "reasoning": ["<step 1>", "<step 2>", "<step 3>"]
}"""

LEGACY_PROMPT = """Based on the visual frames, audio transcript, and secondary sensor logs, produce a structured semantic analysis. You must return ONLY a raw JSON block matching this schema:
{
  "title": "...", "summary": "...", "category": "...", "subcategory": "...",
  "primary_topic": "...", "secondary_topics": [], "entities": [], "people": [],
  "locations": [], "activities": [], "objects": [], "events": [], "keywords": [],
  "recommendation_keywords": [], "language": "...", "mood": "...", "emotion": "...",
  "target_audience": [], "reasoning": "..."
}"""


class VLMProviderClient:
    """
    Task 1 – Configurable VLM Provider Client.
    
    Reads provider and model from vlm_model_config.yaml.
    Supports: minicpm, qwen, internvl, and any Ollama-compatible backend.
    The downstream SRCDE pipeline receives identical observation dicts regardless of provider.
    """

    def __init__(self, use_baseline: bool = False):
        cfg = load_vlm_config()
        key = "vision_model_baseline" if use_baseline else "vision_model"
        model_cfg = cfg.get(key, cfg.get("vision_model", {}))

        self.provider = model_cfg.get("provider", "qwen")
        self.model_name = model_cfg.get("model", "Qwen2.5-VL-7B")
        self.ollama_url = model_cfg.get("ollama_url", "http://localhost:11434/api/chat")
        self.temperature = model_cfg.get("temperature", 0.10)
        self.timeout_sec = model_cfg.get("timeout_sec", 120)
        self.max_frames = model_cfg.get("max_frames", 7)
        self.is_baseline = use_baseline

        print(f"[VLMProvider] Initialized: provider={self.provider}, model={self.model_name}, baseline={use_baseline}")

    def analyze_keyframes(
        self,
        frame_paths: List[str],
        audio_transcript: str = "",
        evidence_summary: str = "",
        prompt_mode: str = "legacy"
    ) -> Dict[str, Any]:
        """
        Main entry point: send keyframes + evidence to the configured VLM.
        prompt_mode: 'legacy' | 'structured_observation' | 'domain_classification'
        """
        selected = self._select_frames(frame_paths)
        b64_images = self._encode_frames(selected)
        prompt = self._build_prompt(prompt_mode, audio_transcript, evidence_summary)

        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt, "images": b64_images}],
            "stream": False,
            "options": {"temperature": self.temperature}
        }

        try:
            req = urllib.request.Request(
                self.ollama_url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=self.timeout_sec) as resp:
                raw = json.loads(resp.read().decode("utf-8"))
                content = raw["message"]["content"].strip()
                return self._parse(content)
        except Exception as e:
            print(f"[VLMProvider] {self.model_name} image query failed: {e}. Retrying text-only…")
            return self._text_only_fallback(payload, audio_transcript)

    def _select_frames(self, frame_paths: List[str]) -> List[str]:
        if len(frame_paths) <= self.max_frames:
            return frame_paths
        step = len(frame_paths) / self.max_frames
        return [frame_paths[int(i * step)] for i in range(self.max_frames)]

    def _encode_frames(self, paths: List[str]) -> List[str]:
        images = []
        for p in paths:
            try:
                with open(p, "rb") as f:
                    images.append(base64.b64encode(f.read()).decode("utf-8"))
            except Exception:
                pass
        return images

    def _build_prompt(self, mode: str, transcript: str, evidence: str) -> str:
        if mode == "structured_observation":
            base = PROMPT_B_SYSTEM + "\n\n" + PROMPT_B_USER
        elif mode == "domain_classification":
            base = PROMPT_C_USER
        else:
            base = LEGACY_PROMPT

        if transcript:
            base += f'\n\nAudio Transcript:\n"""\n{transcript}\n"""'
        if evidence:
            base += f'\n\nSecondary Sensor Evidence:\n"""\n{evidence}\n"""'
        return base

    def _parse(self, text: str) -> Dict[str, Any]:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            text = text[start:end + 1]
        try:
            data = json.loads(text)
            # Coerce list fields
            for field in ["secondary_topics", "entities", "people", "locations",
                          "activities", "objects", "events", "keywords",
                          "recommendation_keywords", "target_audience",
                          "liquids_visible", "musical_instruments", "text_detected",
                          "secondary_classes", "reasoning"]:
                if field in data and isinstance(data[field], str):
                    data[field] = [x.strip() for x in data[field].split(",") if x.strip()]
                elif field not in data:
                    data[field] = []
            return data
        except Exception as e:
            print(f"[VLMProvider] JSON parse failed: {e}")
            return self._fallback(text)

    def _text_only_fallback(self, payload: dict, transcript: str) -> Dict[str, Any]:
        text_payload = dict(payload)
        text_payload["messages"] = [{"role": "user", "content": payload["messages"][0]["content"]}]
        try:
            req = urllib.request.Request(
                self.ollama_url,
                data=json.dumps(text_payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                raw = json.loads(resp.read().decode("utf-8"))
                return self._parse(raw["message"]["content"].strip())
        except Exception as e:
            print(f"[VLMProvider] Text-only fallback also failed: {e}")
            return self._fallback(transcript)

    def _fallback(self, transcript: str = "") -> Dict[str, Any]:
        return {
            "title": "Devotional Content Video",
            "summary": f"Hindu devotional video. Transcript: '{transcript[:80]}...'" if transcript else "Devotional content analyzed.",
            "category": "Devotion",
            "subcategory": "Religious Ceremony",
            "primary_topic": "Hindu Devotional Practices",
            "secondary_topics": [],
            "entities": [], "people": [], "locations": [], "activities": [],
            "objects": [], "events": [], "keywords": ["devotional", "ritual"],
            "recommendation_keywords": ["devotional"],
            "language": "Hindi", "mood": "Spiritual", "emotion": "Devotional",
            "target_audience": ["Devotional Content Viewers"],
            "reasoning": f"Fallback metadata from {self.model_name} service timeout."
        }
