import os
import time
import cv2
from typing import Dict, Any, List

# Schema imports
from src.video_intelligence.schemas import (
    EvidenceGraphSchema,
    EvidenceNodeSchema,
    SemanticGraphHierarchySchema
)

# Component imports
from src.video_intelligence.frame_sampler import VideoPreprocessor
from src.video_intelligence.multimodal_model import MultimodalVLMClient
from src.video_intelligence.semantic_reasoner import SemanticReasoner
from src.video_intelligence.confidence_engine import ConfidenceEngine
from src.video_intelligence.explainability import ExplainabilityEngine
from src.video_intelligence.knowledge_builder import KnowledgeBuilder
from src.video_intelligence.metadata_generator import MetadataGenerator
from src.video_intelligence.evaluator import HumanEvaluator

# Secondary sensor models

from src.content_intelligence.speech import SpeechRecognizer
from src.content_intelligence.ocr import OCRDetector
from src.content_intelligence.vision import ObjectDetector
from src.content_intelligence.scene import SceneUnderstander
from src.content_intelligence.action import ActionRecognizer
from src.content_intelligence.audio import AudioEventDetector

class VideoIntelligenceOrchestrator:
    """Coordinates the entire VIE pipeline execution from raw video file to structured semantic outputs."""

    def __init__(self):
        # 1. Preprocessor & VLM Client
        self.preprocessor = VideoPreprocessor()
        self.vlm_client = MultimodalVLMClient()

        # 2. Reasoning, Graph Building, and Formatting components
        self.reasoner = SemanticReasoner()
        self.confidence_engine = ConfidenceEngine()
        self.explainability = ExplainabilityEngine()
        self.knowledge_builder = KnowledgeBuilder()
        self.metadata_generator = MetadataGenerator()
        self.evaluator = HumanEvaluator()

        # 2b. Daiv Domain HRCE Components (Lazy imported to prevent circular dependency)
        from src.semantic_knowledge.hrce_classifier import HRCEClassifier
        from src.semantic_knowledge.daiv_hierarchical_metadata import DaivHierarchicalMetadataGenerator
        self.hrce_classifier = HRCEClassifier()
        self.daiv_metadata_gen = DaivHierarchicalMetadataGenerator()



        # 3. Secondary Modality Sensors (lazy-loaded to conserve memory)
        self._speech_rec = None
        self._ocr_det = None
        self._obj_det = None
        self._scene_und = None
        self._act_rec = None
        self._aud_det = None

    # Lazy-loading properties for secondary models
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

    def process_video(self, video_path: str, video_id: str) -> Dict[str, Any]:
        """
        Executes the end-to-end Video Intelligence Engine processing cascade.
        """
        print(f"[Orchestrator] Starting VIE execution for video: {video_id}")
        t_start = time.time()

        # Step 1: Video Preprocessing
        prep_data = self.preprocessor.process(video_path, video_id)
        audio_path = prep_data["audio_path"]
        keyframes = prep_data["frames"]

        # Determine video duration
        duration = 0.0
        cap = cv2.VideoCapture(video_path)
        if cap.isOpened():
            total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
            fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
            duration = round(total_frames / fps, 2)
            cap.release()

        # Convert keyframes list to PIL Image tuples for secondary models compat
        pil_frames = []
        for kf in keyframes:
            try:
                from PIL import Image
                img = Image.open(kf["image_path"])
                pil_frames.append((kf["timestamp"], img))
            except Exception as e:
                print(f"[Orchestrator] Error loading frame image: {e}")

        # Step 2: Run Secondary Modality Extractors concurrently (sequential execution)
        evidence = EvidenceGraphSchema()

        # Speech (Whisper)
        speech_transcript = ""
        speech_conf = 0.0
        if audio_path and os.path.exists(audio_path):
            try:
                speech_res = self.speech_rec.transcribe(audio_path)
                speech_transcript = speech_res.get("transcript", "")
                speech_conf = float(speech_res.get("confidence", 0.0))
                if speech_transcript:
                    evidence.speech.append(EvidenceNodeSchema(
                        source="Speech", value=speech_transcript, confidence=speech_conf
                    ))
            except Exception as e:
                print(f"[Orchestrator] Speech recognition error: {e}")

        # OCR Text Scanner
        if pil_frames:
            try:
                ocr_res = self.ocr_det.extract_text(pil_frames)
                for o in ocr_res:
                    evidence.ocr.append(EvidenceNodeSchema(
                        source="OCR", value=o["text"], confidence=o["confidence"], timestamp=o.get("timestamp")
                    ))
            except Exception as e:
                print(f"[Orchestrator] OCR extraction error: {e}")

        # Object Detection (YOLO / CLIP)
        if pil_frames:
            try:
                obj_res = self.obj_det.detect_objects(pil_frames)
                for obj in obj_res:
                    evidence.vision.append(EvidenceNodeSchema(
                        source="YOLO", value=obj["label"], confidence=obj["confidence"]
                    ))
                    
                scene_res = self.scene_und.classify_scenes(pil_frames)
                for sc in scene_res:
                    evidence.vision.append(EvidenceNodeSchema(
                        source="CLIP", value=sc["concept"], confidence=sc["confidence"]
                    ))
            except Exception as e:
                print(f"[Orchestrator] Vision extraction error: {e}")

        # Action Recognition (VideoMAE)
        if pil_frames:
            try:
                act_res = self.act_rec.recognize_actions(pil_frames)
                for act in act_res:
                    evidence.actions.append(EvidenceNodeSchema(
                        source="VideoMAE", value=act["action"], confidence=act["confidence"]
                    ))
            except Exception as e:
                print(f"[Orchestrator] Action recognition error: {e}")

        # Audio Spectrogram events (AST)
        if audio_path and os.path.exists(audio_path):
            try:
                audio_res = self.aud_det.detect_events(audio_path)
                for ev in audio_res:
                    evidence.audio.append(EvidenceNodeSchema(
                        source="AST", value=ev["event"], confidence=ev["confidence"]
                    ))
            except Exception as e:
                print(f"[Orchestrator] Audio event detection error: {e}")

        # Compile a text summary of secondary evidence for fallback text reasoning
        evidence_summary_parts = []
        if evidence.ocr:
            ocr_text = ", ".join(list(set([n.value for n in evidence.ocr])))
            evidence_summary_parts.append(f"- Text visible on screen (OCR): {ocr_text}")
        if evidence.vision:
            objects_text = ", ".join(list(set([n.value for n in evidence.vision if n.source == "YOLO"])))
            scenes_text = ", ".join(list(set([n.value for n in evidence.vision if n.source == "CLIP"])))
            if objects_text:
                evidence_summary_parts.append(f"- Objects detected in keyframes: {objects_text}")
            if scenes_text:
                evidence_summary_parts.append(f"- Environment/Scene categories: {scenes_text}")
        if evidence.actions:
            actions_text = ", ".join(list(set([n.value for n in evidence.actions])))
            evidence_summary_parts.append(f"- Human actions/activities recognized: {actions_text}")
        if evidence.audio:
            audio_text = ", ".join(list(set([n.value for n in evidence.audio])))
            evidence_summary_parts.append(f"- Audio sounds/events: {audio_text}")

        evidence_summary = "\n".join(evidence_summary_parts) if evidence_summary_parts else "No primary objects or on-screen text detected."

        # Step 3: Call holistic Multimodal VLM Qwen2.5-VL (with Text fallback)
        frame_paths = [kf["image_path"] for kf in keyframes]
        print(f"[Orchestrator] Querying MiniCPM-V with {len(frame_paths)} keyframes...")
        vlm_data = self.vlm_client.analyze_keyframes(frame_paths, speech_transcript, evidence_summary)

        # Step 4: Semantic Reasoning & Override Heuristics
        refined_data = self.reasoner.reason(vlm_data, evidence)

        # Step 5: Compute Grounded Provenance & Confidence Metrics
        confidence_map = self.confidence_engine.calculate_confidence(refined_data, evidence)

        # Step 6: Generate Recommendation-Ready Metadata Report
        final_metadata = self.metadata_generator.generate_report(refined_data, confidence_map)

        # Step 6b: Enrich with HRCE & Daiv Fine-Grained Domain Metadata
        try:
            ocr_lines = [n.value for n in evidence.ocr]
            vis_objs = [n.value for n in evidence.vision]
            act_objs = [n.value for n in evidence.actions]

            hrce_res = self.hrce_classifier.classify_video_content(
                vision_data={"detected_objects": vis_objs, "actions": act_objs},
                speech_data={"transcript": speech_transcript, "keywords": [speech_transcript]},
                ocr_data=ocr_lines
            )

            daiv_pkg = self.daiv_metadata_gen.generate_daiv_metadata_package(
                video_id,
                vision_data={"detected_objects": vis_objs, "actions": act_objs},
                speech_data={"transcript": speech_transcript, "keywords": [speech_transcript]},
                ocr_data=ocr_lines
            )

            final_metadata["hrce_classification"] = hrce_res
            final_metadata["daiv_semantic_profile"] = daiv_pkg["daiv_semantic_profile"]
            final_metadata["recommendation_filter_keys"] = daiv_pkg["recommendation_filter_keys"]
            print(f"[Orchestrator] HRCE Classification: {hrce_res['content_type']} -> {hrce_res['primary_class']} -> {hrce_res['sub_class']}")

            # Step 6c: Enrich with SRCDE Target Structured JSON Schema Output
            from src.semantic_knowledge.hierarchical_classifier import HierarchicalClassifier
            srcde_cls = HierarchicalClassifier()
            srcde_res = srcde_cls.classify(
                vision_data={"detected_objects": vis_objs, "actions": act_objs},
                speech_data={"transcript": speech_transcript, "keywords": [speech_transcript]},
                ocr_data=ocr_lines
            )
            final_metadata["srcde_structured_classification"] = srcde_res
            print(f"[Orchestrator] SRCDE Classification: {srcde_res['classification']['content_type']} -> {srcde_res['classification']['primary_class']} -> {srcde_res['classification']['sub_class']} (Conf: {srcde_res['confidence']})")
        except Exception as e:
            print(f"[Orchestrator] HRCE/SRCDE enrichment warning: {e}")



        # Step 7: Build Hierarchical Semantic Graph representation
        hierarchy = self.knowledge_builder.build_hierarchy(
            video_id=video_id,
            duration=duration,
            vlm_data=refined_data,
            evidence=evidence,
            confidence=final_metadata["confidence"],
            keyframes=keyframes
        )

        # Step 8: Generate Human Auditor Validation Report Markdown File
        report_path = self.evaluator.generate_report(video_id, final_metadata, hierarchy)

        execution_time = round(time.time() - t_start, 2)
        print(f"[Orchestrator] Completed VIE execution in {execution_time}s. Metadata & provenance maps generated successfully.")

        return {
            "metadata": final_metadata,
            "evidence": evidence,
            "hierarchy": hierarchy.dict(),
            "validation_report_path": report_path,
            "execution_time_sec": execution_time
        }
