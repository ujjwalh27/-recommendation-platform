"""
Engineering Sprint: Live VLM Validation (LVV) – Live VLM Runner Engine
─────────────────────────────────────────────────────────────────────────────
STRICTLY LIVE INFERENCE ONLY.
NO SIMULATED METRICS, NO HARDCODED DICTIONARIES, NO FAKE OUTPUTS.
Queries local Ollama VLM models directly and records exact raw payloads,
wall-clock latencies, parsed JSON responses, and downstream evaluation.
"""

import os
import json
import time
import base64
import urllib.request
import urllib.error
from typing import List, Dict, Any, Tuple


class LiveVLMRunner:
    """
    Task 2 & 4 — Live VLM Execution Engine.
    Executes live multi-modal visual inference against models running in Ollama.
    """

    def __init__(self, ollama_url: str = "http://localhost:11434/api/chat"):
        self.ollama_url = ollama_url
        print(f"[LiveVLMRunner] Initialized. Ollama URL: {self.ollama_url}")

    def run_live_inference(
        self,
        video_id: str,
        model_name: str,
        frame_paths: List[str],
        audio_transcript: str = "",
        evidence_summary: str = "",
        prompt: str = ""
    ) -> Dict[str, Any]:
        """
        Executes a real live inference request against Ollama for a given model.
        Returns:
            {
                "status": "success" | "failed",
                "video_id": video_id,
                "model_name": model_name,
                "latency_ms": int,
                "raw_prompt": prompt,
                "raw_response": str,
                "parsed_json": dict or None,
                "parse_error": str or None,
                "frame_count": int
            }
        """
        # Encode frames to base64
        base64_images = []
        for path in frame_paths:
            try:
                with open(path, "rb") as f:
                    base64_images.append(base64.b64encode(f.read()).decode("utf-8"))
            except Exception as e:
                print(f"[LiveVLMRunner] Error reading frame {path}: {e}")

        # Construct payload
        payload = {
            "model": model_name,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                    "images": base64_images
                }
            ],
            "stream": False,
            "options": {
                "temperature": 0.10
            }
        }

        start_time = time.time()
        try:
            req = urllib.request.Request(
                self.ollama_url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=120) as resp:
                elapsed_ms = round((time.time() - start_time) * 1000)
                res_body = resp.read().decode("utf-8")
                res_json = json.loads(res_body)

                content = res_json.get("message", {}).get("content", "").strip()

                parsed_json, parse_err = self._parse_json_strictly(content)

                return {
                    "status": "success",
                    "video_id": video_id,
                    "model_name": model_name,
                    "latency_ms": elapsed_ms,
                    "raw_prompt": prompt,
                    "raw_response": content,
                    "parsed_json": parsed_json,
                    "parse_error": parse_err,
                    "frame_count": len(base64_images),
                    "eval_count": res_json.get("eval_count", 0),
                    "eval_duration_ns": res_json.get("eval_duration", 0)
                }
        except Exception as err:
            elapsed_ms = round((time.time() - start_time) * 1000)
            print(f"[LiveVLMRunner] Live inference FAILED for model '{model_name}' on video '{video_id}': {err}")
            return {
                "status": "failed",
                "video_id": video_id,
                "model_name": model_name,
                "latency_ms": elapsed_ms,
                "raw_prompt": prompt,
                "raw_response": f"ERROR: {str(err)}",
                "parsed_json": None,
                "parse_error": str(err),
                "frame_count": len(base64_images),
                "eval_count": 0,
                "eval_duration_ns": 0
            }

    def _parse_json_strictly(self, text: str) -> Tuple[Dict[str, Any], str]:
        """Strictly attempts to parse JSON from raw text without inventing fallback content."""
        if not text:
            return None, "Empty response text"

        # Find JSON boundaries
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            clean_text = text[start:end + 1]
        else:
            clean_text = text

        try:
            data = json.loads(clean_text)
            return data, None
        except Exception as e:
            return None, f"JSON parse error: {str(e)}"
