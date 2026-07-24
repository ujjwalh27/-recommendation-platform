import json
import base64
import urllib.request
import urllib.error
from typing import List, Dict, Any
from src.video_intelligence.config import OLLAMA_URL, VLM_MODEL
from src.video_intelligence.schemas import VLMResponseSchema

class MultimodalVLMClient:
    """Interfaces with local Ollama to send multi-modal keyframe sequences for global context extraction."""

    def __init__(self, ollama_url: str = None, model_name: str = None):
        self.ollama_url = ollama_url or OLLAMA_URL
        self.model_name = model_name or VLM_MODEL

    def analyze_keyframes(self, frame_paths: List[str], audio_transcript: str = "", evidence_summary: str = "") -> Dict[str, Any]:
        """
        Sends the keyframe images sequence and audio transcript to the Video-VLM.
        If the VLM query fails (likely due to text-only model limitations), 
        it falls back to a text-only reasoning prompt based on secondary evidence.
        """
        # 1. Base64-encode up to 3 representative keyframes (start, middle, end)
        selected_paths = [frame_paths[0], frame_paths[len(frame_paths)//2], frame_paths[-1]] if len(frame_paths) >= 3 else frame_paths
        base64_images = []
        for path in selected_paths:
            try:
                with open(path, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode("utf-8")
                    base64_images.append(b64)
            except Exception as e:
                print(f"[VLMClient] Error encoding frame {path}: {e}")

        # 2. Build detailed semantic reasoning prompt
        prompt = (
            "You are an expert Multi-Modal Video Analyst. You are given a sequence of chronological keyframe frames "
            "sampled from an uploaded video. Analyze these frames sequentially to understand the visual narrative.\n\n"
        )
        
        if audio_transcript:
            prompt += (
                f"Additionally, here is the audio transcription track extracted from the video:\n"
                f"\"\"\"\n{audio_transcript}\n\"\"\"\n\n"
            )

        if evidence_summary:
            prompt += (
                f"Here is the summarized evidence detected by secondary sensors (objects, environment, actions, sounds):\n"
                f"\"\"\"\n{evidence_summary}\n\"\"\"\n\n"
            )
            
        prompt += (
            "Based on the visual frames, audio transcript, and secondary sensor logs, produce a structured semantic analysis. "
            "You must return ONLY a raw JSON block matching this schema: (do not include markdown wrapping or explanation outside the JSON):\n"
            "{\n"
            "  \"title\": \"A concise, engaging title for the video (avoid generic names like Clip 102)\",\n"
            "  \"summary\": \"A short paragraph describing what happens, who is involved, where, and why\",\n"
            "  \"category\": \"Select from: Devotion, Entertainment, Tech, Food, Animal, Travel, Automobile, How-to, Music, Lifestyle\",\n"
            "  \"subcategory\": \"A specific subcategory string\",\n"
            "  \"primary_topic\": \"The primary conceptual topic of the video\",\n"
            "  \"secondary_topics\": [\"List of secondary concepts mentioned or visible\"],\n"
            "  \"entities\": [\"Important named people, organizations, books, or products\"],\n"
            "  \"people\": [\"List of specific known or generic people visible or speaking\"],\n"
            "  \"locations\": [\"Locations identified, e.g. temple, kitchen, outdoor road, office\"],\n"
            "  \"activities\": [\"List of physical activities happening in the video (e.g. chanting, cooking, driving)\"],\n"
            "  \"objects\": [\"Important items visible in the frames (e.g. microphone, plate, car, phone)\"],\n"
            "  \"events\": [\"Any events, ceremonies, gatherings, or tutorials\"],\n"
            "  \"keywords\": [\"6-10 keywords summarizing the semantic meaning\"],\n"
            "  \"recommendation_keywords\": [\"3-5 tags specifically optimized for recommendation discovery\"],\n"
            "  \"language\": \"Identify the language spoken (e.g. English, Hindi, Tamil)\",\n"
            "  \"mood\": \"The emotional vibe (e.g. Calm, Spiritual, Energetic, Informative)\",\n"
            "  \"emotion\": \"Primary emotions expressed (e.g. Devotional, Happy, Serious)\",\n"
            "  \"target_audience\": [\"Specific audience segments who would enjoy this video\"],\n"
            "  \"reasoning\": \"A short statement explaining what visual and speech cues led you to these metadata tags\"\n"
            "}"
        )

        # 3. Format Ollama chat payload
        payload = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                    "images": base64_images
                }
            ],
            "stream": False,
            "options": {
                "temperature": 0.1
            }
        }

        # 4. Make HTTP request to local Ollama
        try:
            from src.utils.pipeline_inspector import PipelineInspector
            inspector = PipelineInspector()
            inspector.dump_stage(9, "vlm_image_request_payload.json", {
                "url": self.ollama_url,
                "model": self.model_name,
                "prompt": prompt,
                "image_count": len(base64_images)
            })

            req = urllib.request.Request(
                self.ollama_url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=90) as response:
                res_body = response.read().decode("utf-8")
                res_json = json.loads(res_body)
                content = res_json["message"]["content"].strip()
                inspector.dump_stage(9, "vlm_image_response.json", res_json)
                return self._parse_json_response(content)
        except Exception as e:
            print(f"[VLMClient] VLM image query failed (HTTP 400 or model text-only: {e}). Retrying in Text-Only mode...")
            
            # Fallback retry: remove the images array to query as a text-only prompt
            text_payload = {
                "model": self.model_name,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt + "\n\nCRITICAL: Base your primary classification on the spoken transcript. Do NOT invent activities like pumpkin carving or office work unless explicitly spoken in transcript."
                    }
                ],
                "stream": False,
                "options": {
                    "temperature": 0.10
                }
            }
            try:
                from src.utils.pipeline_inspector import PipelineInspector
                inspector = PipelineInspector()
                inspector.dump_stage(9, "vlm_text_fallback_request.json", {
                    "url": self.ollama_url,
                    "model": self.model_name,
                    "prompt": prompt
                })

                req = urllib.request.Request(
                    self.ollama_url,
                    data=json.dumps(text_payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"}
                )
                with urllib.request.urlopen(req, timeout=45) as response:
                    res_body = response.read().decode("utf-8")
                    res_json = json.loads(res_body)
                    content = res_json["message"]["content"].strip()
                    inspector.dump_stage(9, "vlm_text_fallback_response.json", res_json)
                    return self._parse_json_response(content)
            except Exception as retry_err:
                print(f"[VLMClient] Text-only retry also failed: {retry_err}")
                return self._get_fallback_vlm_response(audio_transcript)

    def _parse_json_response(self, text: str) -> Dict[str, Any]:
        """Attempts to parse JSON from the Ollama response text, with cleaning heuristics."""
        # Find JSON boundaries in case LLM added surrounding markdown wrappers (e.g. ```json ... ```)
        start_idx = text.find("{")
        end_idx = text.rfind("}")
        if start_idx != -1 and end_idx != -1:
            text = text[start_idx:end_idx + 1]

        try:
            data = json.loads(text)
            
            # Coerce list-type fields to list if they are strings
            list_fields = [
                "secondary_topics", "entities", "people", "locations", 
                "activities", "objects", "events", "keywords", 
                "recommendation_keywords", "target_audience"
            ]
            for field in list_fields:
                if field in data:
                    val = data[field]
                    if isinstance(val, str):
                        # Split by comma
                        if "," in val:
                            data[field] = [item.strip() for item in val.split(",") if item.strip()]
                        elif val.strip():
                            data[field] = [val.strip()]
                        else:
                            data[field] = []
                    elif not isinstance(val, list):
                        data[field] = []
                else:
                    data[field] = []
                    
            return data
        except Exception as e:
            print(f"[VLMClient] Failed parsing JSON from raw text: {e}. Raw content: {text}")
            return self._get_fallback_vlm_response()

    def _get_fallback_vlm_response(self, transcript: str = "") -> Dict[str, Any]:
        """Returns a formatted fallback block to keep the pipeline alive during LLM or HTTP failures."""
        return {
            "title": "Unlabeled Video Asset",
            "summary": f"A video clip without manual descriptions. Speech transcript segment: '{transcript[:100]}...'" if transcript else "A video clip analyzed by the Content Intelligence platform.",
            "category": "Entertainment",
            "subcategory": "General Video",
            "primary_topic": "General Content",
            "secondary_topics": [],
            "entities": [],
            "people": [],
            "locations": [],
            "activities": [],
            "objects": [],
            "events": [],
            "keywords": ["video", "clip"],
            "recommendation_keywords": ["general"],
            "language": "English",
            "mood": "Normal",
            "emotion": "Neutral",
            "target_audience": ["General Demographics"],
            "reasoning": "Fallback metadata generated due to VLM model service timeout."
        }
