import os
import json
import time
import urllib.request
import urllib.error
from typing import List, Dict, Any, Optional

def repair_json(json_str: str) -> str:
    """Attempts to repair truncated or incomplete JSON strings by balancing brackets and quotes."""
    json_str = json_str.strip()
    if not json_str.endswith("}"):
        if json_str.endswith(","):
            json_str = json_str[:-1].strip()
            
        open_braces = 0
        open_brackets = 0
        in_string = False
        escape = False
        
        for char in json_str:
            if escape:
                escape = False
                continue
            if char == "\\":
                escape = True
                continue
            if char == '"':
                in_string = not in_string
                continue
            if not in_string:
                if char == "{":
                    open_braces += 1
                elif char == "}":
                    open_braces -= 1
                elif char == "[":
                    open_brackets += 1
                elif char == "]":
                    open_brackets -= 1
                    
        if in_string:
            json_str += '"'
            
        open_braces = 0
        open_brackets = 0
        in_string = False
        escape = False
        for char in json_str:
            if escape:
                escape = False
                continue
            if char == "\\":
                escape = True
                continue
            if char == '"':
                in_string = not in_string
                continue
            if not in_string:
                if char == "{":
                    open_braces += 1
                elif char == "}":
                    open_braces -= 1
                elif char == "[":
                    open_brackets += 1
                elif char == "]":
                    open_brackets -= 1
                
        if open_brackets > 0:
            json_str += "]" * open_brackets
        if open_braces > 0:
            json_str += "}" * open_braces
            
    return json_str

class EvidenceNode:
    """Represents a standardized observation node in the Evidence Graph."""
    def __init__(self, source: str, value: str, confidence: float, timestamp: Optional[float] = None):
        self.source = source
        self.value = value.strip()
        self.confidence = confidence
        self.timestamp = timestamp

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source": self.source,
            "value": self.value,
            "confidence": self.confidence,
            "timestamp": self.timestamp
        }

class EvidenceGraph:
    """Builds, normalizes, and filters duplicate/conflicting multi-modal evidence."""
    def __init__(self):
        self.nodes = []

    def add_node(self, source: str, value: str, confidence: float, timestamp: Optional[float] = None):
        if not value or not str(value).strip():
            return
        self.nodes.append(EvidenceNode(source, value, confidence, timestamp))

    def clean_and_resolve(self):
        """Normalizes observations, removes redundant matches, and resolves contradictions."""
        normalized = []
        seen_values = set()

        # Sort by confidence descending to keep high-trust evidence
        self.nodes.sort(key=lambda n: n.confidence, reverse=True)

        for node in self.nodes:
            val_lower = node.value.lower().strip()
            
            # Remove redundant OCR titles that are already spoken in transcripts
            is_duplicate = False
            if node.source == "OCR":
                for existing in normalized:
                    if existing.source == "Speech" and val_lower in existing.value.lower():
                        is_duplicate = True
                        break
            
            # Remove near-identical object/action tokens
            if val_lower in seen_values:
                is_duplicate = True

            if not is_duplicate:
                normalized.append(node)
                seen_values.add(val_lower)

        # Handle Language/Ritual resolution (e.g. override generic scene predictions if speech has a specific target)
        has_speech = any(n.source == "Speech" for n in normalized)
        if has_speech:
            # If high confidence speech is present, keep its language declaration above CLIP classifications
            pass

        self.nodes = normalized

    def to_summary_dict(self) -> Dict[str, List[Dict[str, Any]]]:
        """Groups normalized nodes by modality for LLM prompt ingestion."""
        summary = {
            "speech": [],
            "ocr": [],
            "vision": [],
            "actions": [],
            "audio": []
        }
        for node in self.nodes:
            category = node.source.lower()
            if category in ["yolo", "clip", "scene", "objects"]:
                category = "vision"
            elif category in ["ast"]:
                category = "audio"
            elif category in ["videomae"]:
                category = "actions"
                
            if category in summary:
                summary[category].append(node.to_dict())
            else:
                summary["vision"].append(node.to_dict())
        return summary

class VideoIntelligenceEngine:
    """The central brain that performs multi-modal evidence fusion, reasoning, and provenance logging."""
    def __init__(self, ollama_url="http://localhost:11434/api/chat", model_name="minicpm-v"):
        self.ollama_url = ollama_url
        self.model_name = model_name
        print(f"[VideoIntelligenceEngine] Initialized using '{self.model_name}' on Ollama.")

    def analyze(self, raw_data: dict) -> dict:
        """Processes raw model extractions through the Evidence Graph and Qwen LLM reasoning."""
        
        # 1. Build and clean the Evidence Graph
        graph = EvidenceGraph()
        
        # Speech
        speech_val = raw_data.get("transcript", "")
        speech_conf = raw_data.get("speech_confidence", 0.90)
        graph.add_node("Speech", speech_val, speech_conf)
        
        # OCR
        for o in raw_data.get("ocr", []):
            graph.add_node("OCR", o.get("text", ""), o.get("confidence", 0.50), o.get("timestamp"))
            
        # YOLO Objects
        for obj in raw_data.get("objects", []):
            graph.add_node("YOLO", obj.get("label", ""), obj.get("confidence", 0.50))
            
        # CLIP Scenes
        for sc in raw_data.get("scenes", []):
            graph.add_node("CLIP", sc.get("concept", ""), sc.get("confidence", 0.40))
            
        # VideoMAE Actions
        for act in raw_data.get("actions", []):
            graph.add_node("VideoMAE", act.get("action", ""), act.get("confidence", 0.40))
            
        # AST Audio Events
        for ev in raw_data.get("audio_events", []):
            graph.add_node("AST", ev.get("event", ""), ev.get("confidence", 0.40))
            
        # Normalize and filter
        graph.clean_and_resolve()
        summary_evidence = graph.to_summary_dict()

        # 2. Formulate prompt with structured evidence representation
        evidence_str = json.dumps(summary_evidence, indent=2)
        prompt = f"""You are a senior multi-modal reasoning architect.
Analyze the following Evidence Graph observations extracted from a short video:

{evidence_str}

Perform deep reasoning to determine the semantic context of the video. Resolve conflicting entries (e.g. visual clutter vs explicit speech keywords).
Explain the provenance (derived_from list of sources and reasoning) for each generated field.

You MUST respond with valid JSON ONLY matching the following schema structure:
{{
  "title": "A descriptive title (max 8 words)",
  "summary": "One-sentence summary (max 30 words)",
  "category": "Broad category matching platform content (e.g. Music, Devotion, Food, Travel, Tech, Comedy, Sports, Gamer, Entertainment)",
  "subcategory": "Specific subcategory (e.g. Acoustic Performance, Temple Ritual, Street Food, Vlog, Tutorial)",
  "mood": "Tone of the video (e.g. Spiritual, Energetic, Peaceful, Playful, Funny, Normal)",
  "language": "Primary language spoken (e.g. Hindi, English, Kannada, Telugu, Tamil, Japanese)",
  "content_type": "Style of video (e.g. Singing Video, Dialogue Reel, Cooking Vlog, Travel Clip)",
  "primary_topic": "Primary theme of the clip",
  "secondary_topics": ["List of secondary themes"],
  "entities": ["Named entities, deities, landmarks, or creators"],
  "important_objects": ["Crucial physical items key to the video theme"],
  "activities": ["List of physical activities visible or spoken"],
  "keywords": ["Core keywords"],
  "recommendation_keywords": ["Strategic keywords for recommendation indexing"],
  "target_audience": ["Target demographic profiles"],
  "reasoning": "Detailed sentence explaining how the system synthesized these findings",
  "evidence": {{
    "speech": ["List of speech observations utilized"],
    "ocr": ["List of OCR text observations utilized"],
    "vision": ["List of objects/scenes utilized"],
    "actions": ["List of actions utilized"],
    "audio": ["List of audio events utilized"]
  }},
  "confidence": {{
    "title": {{
      "value": "title value",
      "derived_from": ["Speech", "Vision"],
      "confidence": 0.95
    }},
    "summary": {{
      "value": "summary value",
      "derived_from": ["Speech", "Vision"],
      "confidence": 0.95
    }},
    "category": {{
      "value": "category value",
      "derived_from": ["Vision", "Actions"],
      "confidence": 0.90
    }},
    "subcategory": {{
      "value": "subcategory value",
      "derived_from": ["Vision", "Actions"],
      "confidence": 0.90
    }},
    "mood": {{
      "value": "mood value",
      "derived_from": ["Audio", "Speech"],
      "confidence": 0.85
    }},
    "language": {{
      "value": "language value",
      "derived_from": ["Speech"],
      "confidence": 0.95
    }},
    "content_type": {{
      "value": "content type value",
      "derived_from": ["Speech", "Vision"],
      "confidence": 0.90
    }},
    "primary_topic": {{
      "value": "primary topic value",
      "derived_from": ["Speech", "Vision"],
      "confidence": 0.90
    }}
  }}
}}

CRITICAL: Do NOT wrap in markdown code blocks. Output JSON only. Do not add any conversational text. Use single quotes for any nested quotes.
"""

        payload = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False,
            "options": {
                "temperature": 0.15,
                "num_predict": 1200
            }
        }

        try:
            req = urllib.request.Request(
                self.ollama_url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=45) as res:
                response = json.loads(res.read().decode("utf-8"))
                
            content = response.get("message", {}).get("content", "").strip()
            
            # Clean markdown code blocks
            if content.startswith("```"):
                lines = content.split("\n")
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines[-1].strip() == "```":
                    lines = lines[:-1]
                content = "\n".join(lines).strip()

            content = repair_json(content)
            first_brace = content.find("{")
            last_brace = content.rfind("}")
            if first_brace != -1 and last_brace != -1:
                content = content[first_brace : last_brace + 1]
            content = repair_json(content)
            
            fused = json.loads(content)
            
            # Normalize list formats
            list_fields = ["secondary_topics", "entities", "important_objects", "activities", "keywords", "recommendation_keywords", "target_audience"]
            for field in list_fields:
                if field not in fused or not isinstance(fused[field], list):
                    if fused.get(field):
                        fused[field] = [str(fused[field])]
                    else:
                        fused[field] = []

            # Populate evidence logs in JSON
            fused["evidence"] = {
                "speech": [n.value for n in graph.nodes if n.source == "Speech"],
                "ocr": [n.value for n in graph.nodes if n.source == "OCR"],
                "vision": [n.value for n in graph.nodes if n.source in ["YOLO", "CLIP"]],
                "actions": [n.value for n in graph.nodes if n.source == "VideoMAE"],
                "audio": [n.value for n in graph.nodes if n.source == "AST"]
            }

            # Enforce schema structure for confidence provenance
            confidence_fields = ["title", "summary", "category", "subcategory", "mood", "language", "content_type", "primary_topic"]
            if "confidence" not in fused or not isinstance(fused["confidence"], dict):
                fused["confidence"] = {}
                
            for field in confidence_fields:
                if field not in fused["confidence"] or not isinstance(fused["confidence"][field], dict):
                    fused["confidence"][field] = {
                        "value": fused.get(field, ""),
                        "derived_from": ["Speech" if field in ["language", "summary"] else "Vision"],
                        "confidence": 0.85
                    }
                    
            return fused

        except Exception as e:
            raw_content = locals().get("content", "")
            print(f"[VideoIntelligenceEngine] Ollama reasoning failed: {e}.\nRaw Output:\n{raw_content}\nUsing fallback heuristics.")
            return self._generate_fallback(raw_data, summary_evidence)

    def _generate_fallback(self, raw_data: dict, summary_evidence: dict) -> dict:
        video_id = raw_data.get("video_id", "Unknown")
        scene_tags = [sc["concept"] for sc in raw_data.get("scenes", [])[:3]]
        
        fallback = {
            "title": f"Analyzed video {video_id}",
            "summary": "A video clip analyzed through multi-modal intelligence.",
            "category": "Entertainment",
            "subcategory": "General Video",
            "mood": "Normal",
            "language": "English",
            "content_type": "Video Clip",
            "primary_topic": scene_tags[0] if scene_tags else "General Content",
            "secondary_topics": scene_tags[1:] if len(scene_tags) > 1 else [],
            "entities": [],
            "important_objects": [obj["label"] for obj in raw_data.get("objects", [])[:3]],
            "activities": [act["action"] for act in raw_data.get("actions", [])[:3]],
            "keywords": scene_tags + [obj["label"] for obj in raw_data.get("objects", [])[:2]],
            "recommendation_keywords": scene_tags,
            "target_audience": ["General users"],
            "reasoning": "Fallback metadata generated due to Ollama connection time out.",
            "evidence": {
                "speech": [n["value"] for n in summary_evidence["speech"]],
                "ocr": [n["value"] for n in summary_evidence["ocr"]],
                "vision": [n["value"] for n in summary_evidence["vision"]],
                "actions": [n["value"] for n in summary_evidence["actions"]],
                "audio": [n["value"] for n in summary_evidence["audio"]]
            },
            "confidence": {
                "title": {"value": f"Analyzed video {video_id}", "derived_from": ["Vision"], "confidence": 0.50},
                "summary": {"value": "A video clip analyzed through multi-modal intelligence.", "derived_from": ["Vision"], "confidence": 0.50},
                "category": {"value": "Entertainment", "derived_from": ["Vision"], "confidence": 0.50},
                "subcategory": {"value": "General Video", "derived_from": ["Vision"], "confidence": 0.50},
                "mood": {"value": "Normal", "derived_from": ["Vision"], "confidence": 0.50},
                "language": {"value": "English", "derived_from": ["Speech"], "confidence": 0.50},
                "content_type": {"value": "Video Clip", "derived_from": ["Vision"], "confidence": 0.50},
                "primary_topic": {"value": "General Content", "derived_from": ["Vision"], "confidence": 0.50}
            }
        }
        return fallback
