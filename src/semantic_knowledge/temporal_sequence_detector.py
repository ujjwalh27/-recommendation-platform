import os
import json

class TemporalSequenceDetector:
    """
    Temporal Sequence Detector for HRCE.
    Tracks ritual progression across chronological keyframes:
    Cleaning Idol -> Milk Abhishekam -> Water Rinse -> Decoration (Alankaram) -> Aarti -> Parikrama
    """

    def analyze_sequence(self, temporal_events, observations):
        events_list = temporal_events if isinstance(temporal_events, list) else []
        objs_list = observations.get("objects", []) if "objects" in observations else observations.get("vision", {}).get("objects", [])
        ocr_list = observations.get("ocr", []) if "ocr" in observations else observations.get("ocr", {}).get("detected_lines", [])
        
        all_text = " ".join([str(x) for x in (events_list + objs_list + ocr_list)]).lower()

        
        sequence_stages = []
        missing_stages = []

        # Stage 1: Preparation / Cleaning
        if "clean" in all_text or "preparation" in all_text or "setup" in all_text:
            sequence_stages.append("Idol Cleaning & Preparation")
        else:
            sequence_stages.append("Initial Shrine Setup")

        # Stage 2: Liquid Abhishekam / Offering
        if "milk" in all_text or "doodh" in all_text:
            sequence_stages.append("Milk Abhishekam Pouring")
        elif "water" in all_text or "jal" in all_text:
            sequence_stages.append("Water Rinse Pouring")
        elif "flower" in all_text or "garland" in all_text:
            sequence_stages.append("Flower Offering (Archana)")
        elif "singing" in all_text or "bhajan" in all_text:
            sequence_stages.append("Devotional Song Chanting")
        elif "lecture" in all_text or "gita" in all_text or "pravachan" in all_text:
            sequence_stages.append("Scripture Exposition")
        else:
            sequence_stages.append("Main Action Execution")

        # Stage 3: Decoration / Alankaram
        if "flower" in all_text or "garland" in all_text or "dress" in all_text:
            sequence_stages.append("Alankaram (Deity Decoration)")

        # Stage 4: Aarti / Flame Rotation
        if "aarti" in all_text or "lamp" in all_text or "camphor" in all_text or "deepa" in all_text:
            sequence_stages.append("Aarti & Flame Rotation")

        return {
            "detected_sequence": sequence_stages,
            "progression_status": "Complete Ritual Progression" if len(sequence_stages) >= 3 else "Partial Sequence",
            "missing_stages": missing_stages
        }
