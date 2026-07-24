import os
import json
import torch
import time
from sentence_transformers import SentenceTransformer
from src.content_intelligence.utils import extract_audio, extract_frames
from src.content_intelligence.speech import SpeechRecognizer
from src.content_intelligence.ocr import OCRDetector
from src.content_intelligence.vision import ObjectDetector
from src.content_intelligence.scene import SceneUnderstander
from src.content_intelligence.action import ActionRecognizer
from src.content_intelligence.audio import AudioEventDetector
from src.video_intelligence import VideoIntelligenceEngine
from src.content_intelligence.database import IntelligenceDatabase
from src.utils.paths import get_path

def detect_hallucinations(fused: dict, evidence_json: dict) -> dict:
    """Programmatically measures the semantic overlap between LLM generated fields and raw extracted evidence."""
    # Build raw evidence word bag
    bag = []
    if evidence_json.get("speech"):
        bag.extend(str(evidence_json["speech"]).lower().split())
    for text in evidence_json.get("ocr", []):
        bag.extend(str(text).lower().split())
    for obj in evidence_json.get("objects", []):
        bag.extend(str(obj).lower().split())
    if evidence_json.get("scene_description"):
        bag.extend(str(evidence_json["scene_description"]).lower().split())
    for act in evidence_json.get("actions", []):
        bag.extend(str(act).lower().split())
    for ev in evidence_json.get("audio_events", []):
        bag.extend(str(ev).lower().split())
        
    cleaned_bag = set()
    for word in bag:
        w = "".join([c for c in word if c.isalnum()])
        if w:
            cleaned_bag.add(w)
            
    stop_words = {"the", "a", "an", "is", "are", "of", "in", "on", "at", "for", "to", "with", "and", "or", "by", "this", "video", "featuring", "showing", "clip", "present"}
    hallucinations = {}
    
    fields_to_check = ["title", "summary", "category", "subcategory", "mood", "language", "content_type", "primary_topic"]
    for field in fields_to_check:
        val = fused.get(field, "")
        check_words = []
        if isinstance(val, list):
            for item in val:
                check_words.extend(str(item).lower().split())
        else:
            check_words.extend(str(val).lower().split())
            
        cleaned_check = []
        for word in check_words:
            w = "".join([c for c in word if c.isalnum()])
            if w and w not in stop_words:
                cleaned_check.append(w)
                
        if not cleaned_check:
            hallucinations[field] = {
                "classification": "Supported",
                "failed_module": None,
                "why_appeared": None,
                "missing_evidence": None
            }
            continue
            
        matches = [w for w in cleaned_check if w in cleaned_bag]
        overlap_ratio = len(matches) / len(cleaned_check) if cleaned_check else 1.0
        
        # Mapping rules matching Task 5 criteria
        if overlap_ratio >= 0.40:
            classification = "Supported"
            failed_module = None
            why_appeared = None
            missing_evidence = None
        elif overlap_ratio >= 0.05:
            classification = "Partially Supported"
            failed_module = None
            why_appeared = "LLM extrapolated broader context from weak visual/speech cues."
            missing_evidence = "Missing explicit confirming spoken words or direct visual actions in OCR/Speech."
        else:
            classification = "Unsupported"
            # Attempt to pinpoint failing module based on field context
            if field in ["category", "subcategory", "mood"]:
                failed_module = "Vision/Scene"
                missing_evidence = "Missing explicit environmental layout cues in CLIP scene classification."
            elif field in ["entities"]:
                failed_module = "Speech/OCR"
                missing_evidence = "Missing proper noun matches in speech transcription and screen OCR text."
            else:
                failed_module = "Fusion Reasoning"
                missing_evidence = "No raw evidence tokens correspond to this output."
                
            why_appeared = f"The model hallucinated values unrelated to raw video frames or sound track cues."
            
        hallucinations[field] = {
            "classification": classification,
            "failed_module": failed_module,
            "why_appeared": why_appeared,
            "missing_evidence": missing_evidence
        }
        
    return hallucinations

class ContentIntelligencePipeline:
    """Orchestrator pipeline that loads modules lazily and runs end-to-end video classification."""
    
    def __init__(self, db_path=None):
        self.db = IntelligenceDatabase(db_path)
        
        # Lazily instantiate modules on first demand to preserve RAM
        self._speech_rec = None
        self._ocr_det = None
        self._obj_det = None
        self._scene_und = None
        self._act_rec = None
        self._aud_det = None
        self._intelligence_engine = None
        self._embedding_model = None

    @property
    def speech_rec(self):
        if not self._speech_rec:
            self._speech_rec = SpeechRecognizer()
        return self._speech_rec

    @property
    def ocr_det(self):
        if not self._ocr_det:
            self._ocr_det = OCRDetector()
        return self._ocr_det

    @property
    def obj_det(self):
        if not self._obj_det:
            self._obj_det = ObjectDetector()
        return self._obj_det

    @property
    def scene_und(self):
        if not self._scene_und:
            self._scene_und = SceneUnderstander()
        return self._scene_und

    @property
    def act_rec(self):
        if not self._act_rec:
            self._act_rec = ActionRecognizer()
        return self._act_rec

    @property
    def aud_det(self):
        if not self._aud_det:
            self._aud_det = AudioEventDetector()
        return self._aud_det

    @property
    def intelligence_engine(self):
        if not self._intelligence_engine:
            self._intelligence_engine = VideoIntelligenceEngine()
        return self._intelligence_engine

    @property
    def embedding_model(self):
        if not self._embedding_model:
            print("[CI-Pipeline] Loading SentenceTransformer 'all-MiniLM-L6-v2'...")
            self._embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        return self._embedding_model

    def analyze_video(self, video_path: str, video_id: str, force_reanalyze: bool = False) -> dict:
        """Runs the raw video file through all analysis stages with full metrics tracking and Phase 5 compliance."""
        
        # Setup debug log output directory
        debug_dir = get_path(f"datasets/processed/debug_pipeline/{video_id}")
        os.makedirs(debug_dir, exist_ok=True)
        
        def save_debug_stage(filename, data):
            filepath = os.path.join(debug_dir, filename)
            with open(filepath, "w") as f:
                json.dump(data, f, indent=2)

        # Return cached analysis from database if present
        if not force_reanalyze:
            existing = self.db.get_record(video_id)
            if existing:
                print(f"[CI-Pipeline] Found cached report for {video_id}. Returning saved state.")
                return existing

        print(f"[CI-Pipeline] Delegating analysis to new Video Intelligence Engine for: {video_path}")
        
        # Call the new Video Intelligence Engine
        report = self.intelligence_engine.analyze_video(video_path, video_id)
        
        metadata = report["metadata"]
        hierarchy = report["hierarchy"]
        
        # Build list metrics and details for compatibility
        # Safely extract string values from evidence nodes (which may be dicts)
        def _node_str(node):
            if isinstance(node, dict):
                return node.get("value", str(node))
            return str(node)

        speech_nodes = hierarchy.get("evidence", {}).get("speech", [])
        speech_text = _node_str(speech_nodes[0]) if speech_nodes else ""
        
        ocr_nodes = hierarchy.get("evidence", {}).get("ocr", [])
        ocr_text = " | ".join([_node_str(o) for o in ocr_nodes]) if ocr_nodes else ""
        
        vision_nodes = hierarchy.get("evidence", {}).get("vision", [])
        objects_list = [_node_str(v) for v in vision_nodes if (isinstance(v, dict) and v.get("source") == "YOLO") or (isinstance(v, str))]
        scenes_list = [_node_str(v) for v in vision_nodes if (isinstance(v, dict) and v.get("source") == "CLIP")]
        
        action_nodes = hierarchy.get("evidence", {}).get("actions", [])
        actions_list = [_node_str(a) for a in action_nodes]
        
        audio_nodes = hierarchy.get("evidence", {}).get("audio", [])
        audio_events_list = [_node_str(au) for au in audio_nodes]
        
        # Mean confidence calculation
        conf_values = [c.confidence if hasattr(c, "confidence") else c.get("confidence", 0.0) for c in metadata.get("confidence", {}).values()]
        mean_confidence = round(sum(conf_values) / len(conf_values), 4) if conf_values else 0.80

        # Output log statements
        stages_log = [
            f"[Pipeline] VIE processed video in {report['metrics']['total_execution_time_sec']}s",
            f"[Pipeline] Vector embedding calculated in {report['metrics']['vector_embedding_time_sec']}s"
        ]

        # Convert confidence schemas to dictionaries for saving
        confidence_breakdown = {}
        for k, v in metadata.get("confidence", {}).items():
            confidence_breakdown[k] = v.confidence if hasattr(v, "confidence") else v.get("confidence", 0.0)

        # Build final record
        final_record = {
            "video_id": video_id,
            "title": metadata.get("title", f"Clip {video_id}"),
            "summary": metadata.get("summary", ""),
            "tags": metadata.get("keywords", []),
            "category": metadata.get("category", "Entertainment"),
            "subcategory": metadata.get("subcategory", "General Video"),
            "keywords": metadata.get("keywords", []),
            "entities": metadata.get("entities", []),
            "language": metadata.get("language", "English"),
            "content_type": metadata.get("content_type", "Video Clip"),
            "mood": metadata.get("mood", "Normal"),
            "transcript": speech_text,
            "ocr": ocr_text,
            "objects": objects_list,
            "scenes": scenes_list,
            "actions": actions_list,
            "audio_events": audio_events_list,
            "confidence": confidence_breakdown,
            "overall_confidence": mean_confidence,
            "embedding_text": report["embedding_text"],
            "embedding": report["embedding"],
            "provenance": report["metadata"]["confidence"],
            "provenance_report": {
                k: {
                    "hallucination_classification": (
                        v.hallucination_classification if hasattr(v, "hallucination_classification")
                        else v.get("hallucination_classification", "Supported")
                    ),
                    "reason": (
                        v.reason if hasattr(v, "reason")
                        else v.get("reason", "Derived from raw multimodal evidence.")
                    ),
                    "derived_from": (
                        v.derived_from if hasattr(v, "derived_from")
                        else v.get("derived_from", ["speech", "vision", "ocr"])
                    )
                }
                for k, v in metadata.get("confidence", {}).items()
            },
            "pipeline_logs": stages_log,
            
            # New semantic attributes
            "primary_topic": metadata.get("primary_topic", ""),
            "secondary_topics": metadata.get("secondary_topics", []),
            "important_objects": metadata.get("objects", []),
            "activities": metadata.get("activities", []),
            "recommendation_keywords": metadata.get("recommendation_keywords", []),
            "target_audience": metadata.get("target_audience", []),
            "reasoning": metadata.get("reasoning", ""),
            # evidence_graph: flatten all node dicts to plain strings for safe React rendering
            "evidence_graph": {
                "speech": [_node_str(n) for n in hierarchy.get("evidence", {}).get("speech", [])],
                "ocr": [_node_str(n) for n in hierarchy.get("evidence", {}).get("ocr", [])],
                "vision": [_node_str(n) for n in hierarchy.get("evidence", {}).get("vision", [])],
                "actions": [_node_str(n) for n in hierarchy.get("evidence", {}).get("actions", [])],
                "audio": [_node_str(n) for n in hierarchy.get("evidence", {}).get("audio", [])],
            }
        }

        # Save to database file
        self.db.save_record(video_id, final_record)
        print(f"[CI-Pipeline] Intelligence report registered. Total Time: {report['metrics']['total_execution_time_sec']}s")
        
        return final_record
