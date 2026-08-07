import re
from typing import Dict, Any, List


class EvidenceCollector:
    """
    Collects and structures evidence signals from all perception models:
    MiniCPM, YOLO, VideoMAE, Whisper, AST, OCR, and CLIP.
    """

    def collect(self, observation: Dict[str, Any], raw_report: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Extracts structured signals from observation layer outputs into a unified Evidence Document.
        """
        raw_report = raw_report or {}
        hierarchy = raw_report.get("hierarchy", {})
        metadata = raw_report.get("metadata", {})

        # Extract text components
        ocr_list = observation.get("ocr_text", [])
        if isinstance(ocr_list, str):
            ocr_list = [ocr_list]
        ocr_text = " ".join([str(o) for o in ocr_list if o])
        speech_text = str(observation.get("speech_text", ""))
        scene_summary = str(observation.get("scene", metadata.get("summary", "")))
        title_str = str(metadata.get("title", ""))

        # 1. YOLO Signals (Visual objects, counts)
        raw_objects = observation.get("objects", []) or metadata.get("objects", [])
        objects_list = [str(o).lower() for o in raw_objects if o]

        object_counts = {}
        for obj in objects_list:
            object_counts[obj] = object_counts.get(obj, 0) + 1

        person_count = sum(c for k, c in object_counts.items() if any(p in k for p in ["person", "priest", "devotee", "man", "woman", "child"]))
        lamp_count = sum(c for k, c in object_counts.items() if any(l in k for l in ["lamp", "diya", "flame", "candle", "light"]))
        flower_count = sum(c for k, c in object_counts.items() if any(f in k for f in ["flower", "garland", "petal", "rose"]))
        vessel_count = sum(c for k, c in object_counts.items() if any(v in k for v in ["vessel", "kalash", "pot", "container", "cup", "bowl"]))
        idol_detected = any(any(i in k for i in ["idol", "statue", "lingam", "deity", "shrine", "sculpture"]) for k in objects_list) or "idol" in scene_summary.lower()

        visual_signals = {
            "objects": objects_list,
            "object_counts": object_counts,
            "person_count": person_count,
            "lamp_count": lamp_count,
            "flower_count": flower_count,
            "vessel_count": vessel_count,
            "idol_detected": idol_detected,
            "raw_count": len(objects_list)
        }

        # 2. VideoMAE Signals (Action & Motion)
        raw_actions = observation.get("actions", []) or metadata.get("activities", [])
        actions_list = [str(a).lower() for a in raw_actions if a]
        actions_text = " ".join(actions_list)

        if any(m in actions_text for m in ["dancing", "running", "marching", "waving flame", "pouring stream"]):
            motion_level = "High"
        elif any(m in actions_text for m in ["walking", "pouring", "waving", "singing", "holding"]):
            motion_level = "Medium"
        elif any(m in actions_text for m in ["seated", "sitting", "meditating", "standing", "still"]):
            motion_level = "Low"
        else:
            motion_level = "Medium" if ("pouring" in scene_summary.lower() or "flame" in scene_summary.lower()) else "Low"

        videomae_signals = {
            "actions": actions_list,
            "motion_level": motion_level,
            "action_count": len(actions_list)
        }

        # 3. Whisper Signals (Audio transcript & speech)
        speech_speed = "slow" if len(speech_text.split()) < 10 else ("fast" if len(speech_text.split()) > 30 else "normal")
        has_chants = any(c in speech_text.lower() for c in ["om", "namah", "shanti", "mantra", "hare krishna", "govinda", "swaha", "sloka"])
        
        whisper_signals = {
            "transcript": speech_text,
            "speech_speed": speech_speed,
            "has_chants": has_chants,
            "word_count": len(speech_text.split())
        }

        # 4. AST Signals (Audio events)
        audio_nodes = hierarchy.get("evidence", {}).get("audio", [])
        audio_events = [str(a.get("value", a) if isinstance(a, dict) else a).lower() for a in audio_nodes]
        audio_text = " ".join(audio_events) + " " + speech_text.lower()

        ast_signals = {
            "audio_events": audio_events,
            "bells": any(b in audio_text for b in ["bell", "bells", "chime", "ringing"]),
            "drums": any(d in audio_text for d in ["drum", "drums", "dhol", "tabla", "percussion", "chenda"]),
            "chanting": any(c in audio_text for c in ["chanting", "chant", "singing", "hymn", "mantra", "choir"]) or has_chants,
            "crowd_noise": any(c in audio_text for c in ["cheering", "crowd", "applause", "shouting", "noise"]),
            "music": any(m in audio_text for m in ["music", "singing", "harmonium", "instrument", "melody"]),
            "silence": len(audio_text.strip()) == 0 or "silent" in audio_text
        }

        # 5. OCR Signals (Textual banners, temple names)
        ocr_terms = [t for t in ocr_text.split("|") if t.strip()]
        temple_names = [t.strip() for t in ocr_terms if any(k in t.lower() for k in ["temple", "mandir", "shrine", "tirupati", "iskcon", "dham", "peeth"])]
        
        ocr_signals = {
            "ocr_terms": ocr_terms,
            "raw_text": ocr_text,
            "temple_names": temple_names
        }

        # 6. CLIP Signals (Scene environment classification)
        vision_nodes = hierarchy.get("evidence", {}).get("vision", [])
        clip_labels = [str(v.get("value", v) if isinstance(v, dict) else v).lower() for v in vision_nodes]
        all_text = f"{scene_summary} {title_str} {' '.join(clip_labels)}".lower()

        if any(e in all_text for e in ["street", "procession", "yatra", "road", "outdoor", "river", "ghat"]):
            clip_env = "outdoor_procession" if "procession" in all_text else "outdoor_sacred"
        elif any(e in all_text for e in ["sanctum", "garbhagriha", "altar", "inner shrine", "temple"]):
            clip_env = "temple_sanctum"
        elif any(e in all_text for e in ["home", "domestic", "living room", "personal shrine"]):
            clip_env = "home_shrine"
        else:
            clip_env = "indoor_sacred_space"

        clip_signals = {
            "clip_labels": clip_labels,
            "environment": clip_env
        }

        # 7. MiniCPM Signals (VLM narrative summary)
        minicpm_signals = {
            "summary": scene_summary,
            "narrative": metadata.get("reasoning", scene_summary),
            "ritual_description": metadata.get("primary_topic", scene_summary),
            "inferred_objects": metadata.get("objects", [])
        }

        # Consolidate Evidence Document
        evidence_doc = {
            "visual": visual_signals,
            "videomae": videomae_signals,
            "audio": ast_signals,
            "whisper": whisper_signals,
            "text": ocr_signals,
            "clip": clip_signals,
            "vlm": minicpm_signals,
            "metadata_context": {
                "title": title_str,
                "language": metadata.get("language", "Hindi"),
                "mood": metadata.get("mood", "Normal")
            }
        }

        return evidence_doc
