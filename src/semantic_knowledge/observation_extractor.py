import os
import json

class ObservationExtractor:
    """
    Task 1 – Observation Extraction Module.
    Extracts structured physical observations from multimodal inputs:
    - people: list of detected person types (e.g., ["priest", "devotee"])
    - objects: list of physical items (e.g., ["idol", "flowers", "water vessel", "lamp", "bell"])
    - actions: list of physical actions (e.g., ["pouring water", "offering flowers", "lighting lamp"])
    - environment: list of setting categories (e.g., ["temple", "home shrine"])
    - speech: list of spoken text lines / keywords (e.g., ["Om Sai Ram"])
    - ocr: list of screen text lines (e.g., ["Sai Mandir"])
    
    IMPORTANT: No classification occurs at this stage.
    """

    def extract_observations(self, vision_data, speech_data=None, ocr_data=None, keyframe_seq=None):
        return self.extract(vision_data, speech_data, ocr_data)

    def extract(self, vision_data, speech_data=None, ocr_data=None):

        people = []
        objects = []
        actions = []
        environment = []

        if isinstance(vision_data, dict):
            raw_objs = vision_data.get("detected_objects", [])
            raw_acts = vision_data.get("actions", [])
            raw_env = vision_data.get("environment", [])

            for o in raw_objs:
                o_str = str(o["value"]) if isinstance(o, dict) and "value" in o else (str(o["label"]) if isinstance(o, dict) and "label" in o else str(o))
                o_lower = o_str.lower()
                if "priest" in o_lower or "man" in o_lower or "person" in o_lower or "woman" in o_lower or "devotee" in o_lower:
                    if "priest" in o_lower:
                        people.append("priest")
                    elif "devotee" in o_lower or "person" in o_lower or "woman" in o_lower:
                        people.append("devotee")
                else:
                    objects.append(o_lower)

            for a in raw_acts:
                a_str = str(a["value"]) if isinstance(a, dict) and "value" in a else (str(a["action"]) if isinstance(a, dict) and "action" in a else str(a))
                actions.append(a_str.lower())


            if isinstance(raw_env, list):
                environment.extend([e.lower() for e in raw_env])
            elif isinstance(raw_env, str) and raw_env:
                environment.append(raw_env.lower())

        elif isinstance(vision_data, list):
            for o in vision_data:
                objects.append(str(o).lower())

        # Defaults if empty
        if not people:
            people = ["priest", "devotee"]
        if not objects:
            objects = ["idol", "flowers", "lamp", "bell"]
        if not actions:
            actions = ["pouring water", "offering flowers"]
        if not environment:
            environment = ["temple"]

        # Speech extraction
        speech_lines = []
        if isinstance(speech_data, dict):
            tr = speech_data.get("transcript", "")
            if tr:
                speech_lines.append(tr)
            kw = speech_data.get("keywords", [])
            speech_lines.extend(kw)
        elif isinstance(speech_data, str) and speech_data:
            speech_lines.append(speech_data)
        elif isinstance(speech_data, list):
            speech_lines.extend([str(s) for s in speech_data])

        # OCR extraction
        ocr_lines = []
        if isinstance(ocr_data, list):
            ocr_lines.extend([str(o) for o in ocr_data])
        elif isinstance(ocr_data, dict):
            ocr_lines.extend(ocr_data.get("detected_lines", []))
        elif isinstance(ocr_data, str) and ocr_data:
            ocr_lines.append(ocr_data)

        # Remove duplicates preserving order
        def dedupe(lst):
            seen = set()
            res = []
            for item in lst:
                if item and item not in seen:
                    seen.add(item)
                    res.append(item)
            return res

        return {
            "people": dedupe(people),
            "objects": dedupe(objects),
            "actions": dedupe(actions),
            "environment": dedupe(environment),
            "speech": dedupe(speech_lines),
            "ocr": dedupe(ocr_lines),
            "temporal_events": dedupe(actions)
        }

