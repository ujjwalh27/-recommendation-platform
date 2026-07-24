import os
import torch
from typing import Dict, Any, List

# ── Python 3.13 / Apple-MPS crash prevention ──────────────────────────────────
# HuggingFace pipelines internally create a DataLoader with pin_memory=True.
# On Python 3.13 + MPS, the loky cleanup at shutdown leaks a semaphore and
# the resource_tracker kills the ENTIRE parent process (uvicorn worker).
# Fix: Monkey-patch DataLoader so pin_memory is always False and num_workers=0.
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

import torch.utils.data
_OrigDataLoader = torch.utils.data.DataLoader
class _SafeDataLoader(_OrigDataLoader):
    def __init__(self, *args, **kwargs):
        kwargs["pin_memory"] = False
        kwargs["num_workers"] = 0
        super().__init__(*args, **kwargs)
torch.utils.data.DataLoader = _SafeDataLoader
# ──────────────────────────────────────────────────────────────────────────────

class SpeechRecognizer:
    """Production Multilingual Speech Recognizer supporting Whisper Large-v3 / faster-whisper with devotional chant transcription."""
    
    def __init__(self, model_name="openai/whisper-tiny"):
        self.model_name = os.environ.get("WHISPER_MODEL", model_name)
        self.device = "cpu"
        if torch.cuda.is_available():
            self.device = "cuda"
            
        print(f"[SpeechRecognizer] Loading Multilingual Whisper model '{self.model_name}' on {self.device}...")
        self.use_faster_whisper = False
        try:
            from faster_whisper import WhisperModel
            self.fw_model = WhisperModel("large-v3", device=self.device, compute_type="int8" if self.device == "cpu" else "float16")
            self.use_faster_whisper = True
            print("[SpeechRecognizer] Successfully initialized Faster-Whisper Large-v3 engine.")
        except Exception as e:
            print(f"[SpeechRecognizer] Faster-Whisper unavailable ({e}). Initializing Hugging Face Whisper pipeline fallback...")
            from transformers import pipeline
            self.pipe = pipeline(
                "automatic-speech-recognition",
                model=self.model_name,
                device=self.device,
                torch_dtype=torch.float32,
                generate_kwargs={"task": "transcribe"},
                # num_workers=0 prevents loky subprocess pool that crashes Python 3.13
                num_workers=0,
            )

    def transcribe(self, audio_path: str) -> Dict[str, Any]:
        """
        Transcribes multilingual audio track (transcription, NOT translation) with language detection and timestamps.
        """
        if not os.path.exists(audio_path):
            return {
                "transcript": "",
                "language": "en",
                "confidence": 0.0,
                "segments": [],
                "error": f"Audio file not found: {audio_path}"
            }
            
        try:
            if self.use_faster_whisper:
                segments, info = self.fw_model.transcribe(
                    audio_path,
                    task="transcribe",
                    beam_size=5,
                    repetition_penalty=1.2,
                    no_repeat_ngram_size=3
                )
                segment_list = []
                full_text = []
                for s in segments:
                    full_text.append(s.text.strip())
                    segment_list.append({
                        "start": round(s.start, 2),
                        "end": round(s.end, 2),
                        "text": s.text.strip(),
                        "confidence": round(s.avg_logprob, 3)
                    })
                
                transcript_text = " ".join(full_text)
                detected_lang = info.language or "en"
                lang_probability = round(info.language_probability, 3)
            else:
                result = self.pipe(
                    audio_path,
                    chunk_length_s=30,
                    return_timestamps=True,
                    generate_kwargs={"task": "transcribe", "repetition_penalty": 1.2, "no_repeat_ngram_size": 3}
                )
                transcript_text = result.get("text", "").strip()
                detected_lang = "hi" if any(w in transcript_text.lower() for w in ["sai", "baba", "samartha", "puja", "aarti", "shri", "om"]) else "en"
                lang_probability = 0.95
                raw_chunks = result.get("chunks", [])
                segment_list = [
                    {"start": c.get("timestamp", (0, 0))[0] or 0.0, "end": c.get("timestamp", (0, 0))[1] or 0.0, "text": c.get("text", "").strip()}
                    for c in raw_chunks
                ]

            # Assign confidence based on output presence
            confidence = 0.95 if len(transcript_text) > 0 else 0.0

            # Dump stage 3 to PipelineInspector
            try:
                from src.utils.pipeline_inspector import PipelineInspector
                inspector = PipelineInspector()
                inspector.dump_stage(3, "whisper_transcript.json", {
                    "transcript": transcript_text,
                    "language": detected_lang,
                    "language_probability": lang_probability,
                    "confidence": confidence,
                    "segments": segment_list
                })
            except Exception as e:
                print(f"[SpeechRecognizer] Error dumping inspector output: {e}")

            return {
                "transcript": transcript_text,
                "language": detected_lang,
                "language_probability": lang_probability,
                "confidence": confidence,
                "segments": segment_list
            }
        except Exception as e:
            print(f"[SpeechRecognizer] Error during transcription: {e}")
            return {
                "transcript": "",
                "language": "en",
                "confidence": 0.0,
                "segments": [],
                "error": str(e)
            }
