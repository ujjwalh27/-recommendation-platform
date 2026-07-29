import os
import json

from src.semantic_knowledge.observation_extractor import ObservationExtractor
from src.semantic_knowledge.temporal_reasoning_engine import TemporalReasoningEngine
from src.semantic_knowledge.ritual_decision_engine import RitualDecisionEngine

class HierarchicalClassifier:
    """
    Task 3, 4, 7, 8 – Hierarchical Classifier for SRCDE.
    Coordinates observation extraction, temporal timeline analysis, and rule-based decision engine
    to produce the exact target JSON schema with explainability and ranked candidate predictions.
    """

    def __init__(self):
        self.observation_extractor = ObservationExtractor()
        self.temporal_engine = TemporalReasoningEngine()
        self.decision_engine = RitualDecisionEngine()

    def classify(self, vision_data, speech_data=None, ocr_data=None, keyframe_events=None):
        # Step 1: Observation Extraction (Task 1)
        obs = self.observation_extractor.extract(vision_data, speech_data, ocr_data)

        # Step 2: Temporal Reasoning (Task 6)
        temporal_analysis = self.temporal_engine.analyze_timeline(keyframe_events, obs)

        # Step 3: Decision Engine Evaluation (Task 2, 3, 4, 5)
        decision = self.decision_engine.evaluate_decision(obs, temporal_analysis)

        # Build Explanation Summary
        primary_cls = decision["primary_class"]
        sub_cls = decision["sub_class"]
        conf = decision["confidence"]
        
        explanation_text = f"Strong evidence for {primary_cls} ({sub_cls}). Confirmed with {conf*100:.0f}% confidence based on multimodal vision, speech, and OCR observation rules."

        # Step 4: Construct Target Output Schema (Task 7 & 8)
        output_schema = {
            "classification": {
                "content_type": decision["content_type"],
                "primary_class": decision["primary_class"],
                "sub_class": decision["sub_class"]
            },
            "confidence": decision["confidence"],
            "observations": {
                "people": obs["people"],
                "objects": obs["objects"],
                "actions": obs["actions"],
                "speech": obs["speech"],
                "ocr": obs["ocr"]
            },
            "reasoning": decision["reasoning"],
            "alternative_predictions": decision["alternative_predictions"],
            "explanation": explanation_text
        }

        return output_schema
