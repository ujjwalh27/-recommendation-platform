import json
import urllib.request
import urllib.error

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
            
        # Re-tally to handle balanced brackets closure correctly
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

class MetadataFusionEngine:
    """Metadata Fusion Engine utilizing local Ollama server to synthesize multimodal inputs."""
    
    def __init__(self, ollama_url="http://localhost:11434/api/chat", model_name="minicpm-v"):
        self.ollama_url = ollama_url
        self.model_name = model_name

    def fuse_metadata(self, extracted_data: dict) -> dict:
        """Sends extracted features to local Qwen LLM to perform semantic reasoning and output structured data."""
        
        video_id = extracted_data.get("video_id", "Unknown")
        transcript = extracted_data.get("transcript", "No speech detected")
        
        # Format textual descriptions of detected items
        ocr_lines = [item["text"] for item in extracted_data.get("ocr", [])]
        ocr_text = " | ".join(ocr_lines) if ocr_lines else "No readable text on-screen"
        
        objects = ", ".join([f"{item['label']}" for item in extracted_data.get("objects", [])]) or "No distinct objects detected"
        scenes = ", ".join([item["concept"] for item in extracted_data.get("scenes", [])]) or "Generic scene"
        actions = ", ".join([item["action"] for item in extracted_data.get("actions", [])]) or "No clear motion actions"
        audio_events = ", ".join([item["event"] for item in extracted_data.get("audio_events", [])]) or "Ambient noise"
        
        prompt = f"""You are a content analysis assistant for a short video platform.
Analyze the following multi-modal extractions from an uploaded video:

- Video ID: {video_id}
- Transcript (Speech-to-Text): "{transcript}"
- Screen OCR text: "{ocr_text}"
- Detected Objects: {objects}
- Detected Environment/Scenes: {scenes}
- Detected Motion/Actions: {actions}
- Audio Events: {audio_events}

Using these raw inputs, perform deep reasoning to determine the semantic meaning of the video content. Do not merely list or concatenate the extractions.
For every field you generate, you must record its provenance (what evidence supports it), a justification reason, and a confidence score.

Generate:
1. title: A clean, descriptive title (maximum 8 words).
2. summary: A detailed one-sentence summary of the video content (maximum 30 words).
3. tags: 4 to 6 highly relevant, specific tags.
4. category: A high-level category matching the platform content (e.g. Music, Devotion, Food, Travel, Tech, Comedy, Sports, Gamer, Entertainment).
5. subcategory: A specific subcategory (e.g. Acoustic Performance, Temple Ritual, Street Food, Vlog, Tutorial).
6. mood: The tone or feeling of the video (e.g. Spiritual, Energetic, Peaceful, Playful, Funny, Normal).
7. language: The primary language spoken or detected (e.g. Hindi, English, Kannada, Telugu, Tamil).
8. content_type: The style of the video (e.g. Singing Video, Dialogue Reel, Cooking Vlog, Travel Clip).
9. keywords: 5 to 10 key concepts mentioned or visible.
10. entities: A flat list of strings representing named entities (e.g. people, places, deities, festivals, or landmarks) confidently identified or inferred. Do NOT output objects; only use plain strings.
11. embedding_text: An optimized natural description combining Title, Summary, Category, Mood, and key Entities for indexing.

You MUST respond with valid JSON ONLY. Do not wrap your response in markdown code blocks. Do not add any conversational text.
CRITICAL: Do NOT use unescaped double quotes inside JSON string values. Use single quotes (e.g. 'quote') if you need to wrap any words.

Required JSON Format:
{{
  "title": {{
    "value": "",
    "derived_from": [],
    "reason": "",
    "confidence": 0.0
  }},
  "summary": {{
    "value": "",
    "derived_from": [],
    "reason": "",
    "confidence": 0.0
  }},
  "tags": {{
    "value": [],
    "derived_from": [],
    "reason": "",
    "confidence": 0.0
  }},
  "category": {{
    "value": "",
    "derived_from": [],
    "reason": "",
    "confidence": 0.0
  }},
  "subcategory": {{
    "value": "",
    "derived_from": [],
    "reason": "",
    "confidence": 0.0
  }},
  "mood": {{
    "value": "",
    "derived_from": [],
    "reason": "",
    "confidence": 0.0
  }},
  "language": {{
    "value": "",
    "derived_from": [],
    "reason": "",
    "confidence": 0.0
  }},
  "content_type": {{
    "value": "",
    "derived_from": [],
    "reason": "",
    "confidence": 0.0
  }},
  "keywords": {{
    "value": [],
    "derived_from": [],
    "reason": "",
    "confidence": 0.0
  }},
  "entities": {{
    "value": [],
    "derived_from": [],
    "reason": "",
    "confidence": 0.0
  }},
  "embedding_text": {{
    "value": "",
    "derived_from": [],
    "reason": "",
    "confidence": 0.0
  }}
}}"""

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
                "temperature": 0.25,
                "num_predict": 1024
            }
        }
        
        try:
            req = urllib.request.Request(
                self.ollama_url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=40) as res:
                response = json.loads(res.read().decode("utf-8"))
                
            content = response.get("message", {}).get("content", "").strip()
            
            # Clean potential Markdown syntax wrapping the JSON output
            if content.startswith("```"):
                lines = content.split("\n")
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines[-1].strip() == "```":
                    lines = lines[:-1]
                content = "\n".join(lines).strip()
                
            # Auto-recover/balance truncated JSON structures using repair_json helper
            content = repair_json(content)
                
            # Robust JSON boundary search to extract raw JSON block
            first_brace = content.find("{")
            last_brace = content.rfind("}")
            if first_brace != -1 and last_brace != -1:
                content = content[first_brace : last_brace + 1]
                
            # Run JSON repair again on sliced segment to balance inner lists/objects safely
            content = repair_json(content)
            fused = json.loads(content)
            
            # Normalize and ensure schema compliance for each field
            expected_fields = ["title", "summary", "tags", "category", "subcategory", "mood", "language", "content_type", "keywords", "entities", "embedding_text"]
            for field in expected_fields:
                if field not in fused or not isinstance(fused[field], dict):
                    val = fused.get(field, "")
                    fused[field] = {
                        "value": val,
                        "derived_from": ["Scene" if field in ["category", "subcategory"] else "Speech"],
                        "reason": "Recovered from LLM direct key-value fallback.",
                        "confidence": 0.8
                    }
                nested = fused[field]
                if "value" not in nested:
                    nested["value"] = ""
                if "derived_from" not in nested or not isinstance(nested["derived_from"], list):
                    nested["derived_from"] = ["Speech"]
                if "reason" not in nested:
                    nested["reason"] = "Inferred from multi-modal inputs."
                if "confidence" not in nested:
                    nested["confidence"] = 0.85
                    
                # Normalize tags, keywords, entities value as list
                if field in ["tags", "keywords", "entities"]:
                    if not isinstance(nested["value"], list):
                        if nested["value"]:
                            nested["value"] = [str(nested["value"])]
                        else:
                            nested["value"] = []
                            
            return fused
            
        except Exception as e:
            raw_content = locals().get("content", "")
            print(f"[MetadataFusionEngine] Ollama query failed: {e}.\nRaw Content was:\n{raw_content}\nFalling back to default heuristics.")
            fallback_tags = [item["concept"] for item in extracted_data.get("scenes", [])[:3]] or ["Video", "Clip"]
            fallback = {}
            fallback["title"] = {
                "value": f"Analyzed Clip {video_id}",
                "derived_from": ["Scene"],
                "reason": "Default fallback based on video ID.",
                "confidence": 0.5
            }
            fallback["summary"] = {
                "value": f"Video featuring {actions or 'motion'} in a {scenes or 'scene'} setting.",
                "derived_from": ["Action", "Scene"],
                "reason": "Synthesized setting and activity from visual modules.",
                "confidence": 0.5
            }
            fallback["tags"] = {
                "value": fallback_tags,
                "derived_from": ["Scene"],
                "reason": "Primary scene concepts.",
                "confidence": 0.5
            }
            fallback["category"] = {
                "value": "Entertainment",
                "derived_from": ["Scene"],
                "reason": "Broad base category selection.",
                "confidence": 0.5
            }
            fallback["subcategory"] = {
                "value": "General Video",
                "derived_from": ["Scene"],
                "reason": "Generic subcategory classification.",
                "confidence": 0.5
            }
            fallback["mood"] = {
                "value": "Normal",
                "derived_from": ["Audio"],
                "reason": "Assumed default mood.",
                "confidence": 0.5
            }
            fallback["language"] = {
                "value": "English",
                "derived_from": ["Speech"],
                "reason": "Default language prediction.",
                "confidence": 0.5
            }
            fallback["content_type"] = {
                "value": "Video Clip",
                "derived_from": ["Scene"],
                "reason": "Default video layout style.",
                "confidence": 0.5
            }
            fallback["keywords"] = {
                "value": fallback_tags,
                "derived_from": ["Scene"],
                "reason": "Primary visual tags.",
                "confidence": 0.5
            }
            fallback["entities"] = {
                "value": [],
                "derived_from": ["Speech"],
                "reason": "No entities detected in fallback.",
                "confidence": 0.5
            }
            fallback["embedding_text"] = {
                "value": f"Analyzed Clip {video_id}. Video featuring {actions} in a {scenes} setting.",
                "derived_from": ["Action", "Scene"],
                "reason": "Concatenated visual metadata.",
                "confidence": 0.5
            }
            return fallback
