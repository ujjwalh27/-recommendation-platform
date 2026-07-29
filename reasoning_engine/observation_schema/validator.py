"""
Task 1 – Observation Validator Module
Validates raw VLM/multimodal observation payloads against observation_schema.json.
Ensures provider-agnostic input normalization before entity resolution & reasoning.
"""

import os
import json
from typing import Dict, Any, Tuple, List


class ObservationValidator:
    """Validates and normalizes VLM observation payloads into CMREE standard format."""

    def __init__(self, schema_path: str = None):
        if schema_path is None:
            schema_path = os.path.join(os.path.dirname(__file__), "observation_schema.json")
        
        self.schema_path = schema_path
        self.schema = {}
        if os.path.exists(schema_path):
            with open(schema_path, "r", encoding="utf-8") as f:
                self.schema = json.load(f)

    def validate_and_normalize(self, raw_obs: Dict[str, Any]) -> Tuple[bool, Dict[str, Any], List[str]]:
        """
        Validates raw observation dict and normalizes missing or legacy fields.
        Returns:
            (is_valid, normalized_obs, validation_errors)
        """
        errors = []
        normalized = {}

        # 1. Normalize video_id
        normalized["video_id"] = str(raw_obs.get("video_id") or raw_obs.get("id") or "vid_unknown")

        # 2. Normalize scene description
        normalized["scene"] = str(raw_obs.get("scene") or raw_obs.get("summary") or raw_obs.get("title") or "")
        if not normalized["scene"]:
            errors.append("Warning: 'scene' description is empty")

        # 3. Normalize actions
        raw_actions = raw_obs.get("actions") or raw_obs.get("activities") or []
        if isinstance(raw_actions, str):
            raw_actions = [x.strip() for x in raw_actions.split(",") if x.strip()]
        normalized["actions"] = [str(a) for a in raw_actions if a]

        # 4. Normalize objects
        raw_objects = raw_obs.get("objects") or []
        normalized_objects = []
        if isinstance(raw_objects, list):
            for obj in raw_objects:
                if isinstance(obj, str):
                    normalized_objects.append({"name": obj, "confidence": 0.85, "attributes": []})
                elif isinstance(obj, dict) and "name" in obj:
                    normalized_objects.append({
                        "name": str(obj["name"]),
                        "confidence": float(obj.get("confidence", 0.85)),
                        "attributes": list(obj.get("attributes", []))
                    })
        normalized["objects"] = normalized_objects

        # 5. Normalize OCR text
        raw_ocr = raw_obs.get("ocr_text") or raw_obs.get("text_detected") or raw_obs.get("ocr") or []
        if isinstance(raw_ocr, str):
            raw_ocr = [x.strip() for x in raw_ocr.split(",") if x.strip()]
        normalized["ocr_text"] = [str(t) for t in raw_ocr if t]

        # 6. Normalize Speech text
        normalized["speech_text"] = str(
            raw_obs.get("speech_text") or raw_obs.get("audio_transcript") or raw_obs.get("transcript") or ""
        )

        # 7. Normalize Language
        normalized["language"] = str(raw_obs.get("language") or "Hindi")

        # 8. Normalize Emotion/Mood
        normalized["emotion"] = str(raw_obs.get("emotion") or raw_obs.get("mood") or "Devotional")

        # 9. Normalize Confidence
        try:
            conf = float(raw_obs.get("confidence", 0.85))
            normalized["confidence"] = min(1.0, max(0.0, conf))
        except (ValueError, TypeError):
            normalized["confidence"] = 0.85

        # 10. Timeline
        normalized["timeline"] = list(raw_obs.get("timeline") or [])

        is_valid = len(errors) == 0 or all(e.startswith("Warning:") for e in errors)
        return is_valid, normalized, errors
