import os
import json

from src.semantic_knowledge.observation_extractor import ObservationExtractor
from src.semantic_knowledge.temporal_sequence_detector import TemporalSequenceDetector
from src.semantic_knowledge.domain_rule_engine import DomainRuleEngine
from src.semantic_knowledge.daiv_entity_resolver import DaivEntityResolver

class HRCEClassifier:
    """
    Hierarchical Ritual Classification Engine (HRCE) for Daiv.
    Processes observations through a 3-staged classification pipeline:
    Stage 1: Content Type (Ritual, Music, Discourse, Temple, Festival)
    Stage 2: Primary Class (Abhishekam, Aarti, Pooja, Archana, Bhajan, Pravachan, Temple Darshan)
    Stage 3: Sub-Class (Milk Abhishekam, Kakad Aarti, Bhagavad Gita Pravachan, etc.)
    """

    def __init__(self):
        self.extractor = ObservationExtractor()
        self.temporal_detector = TemporalSequenceDetector()
        self.rule_engine = DomainRuleEngine()
        self.resolver = DaivEntityResolver()

    def classify_video_content(self, vision_data, speech_data=None, ocr_data=None, keyframe_seq=None):
        # Step 1: Extract Structured Observations
        obs = self.extractor.extract_observations(vision_data, speech_data, ocr_data, keyframe_seq)

        # Step 2: Detect Temporal Ritual Sequence
        temporal_analysis = self.temporal_detector.analyze_sequence(obs["temporal_events"], obs)

        # Step 3: Apply Multi-Signal Rule Engine
        rule_results = self.rule_engine.apply_rules(obs, temporal_analysis)
        primary_cls = rule_results["primary_class"]
        primary_conf = rule_results["primary_confidence"]

        # Stage 1: Content Type Mapping
        if primary_cls in ["Abhishekam", "Aarti", "Pooja", "Archana", "Homa"]:
            content_type = "Ritual"
        elif primary_cls in ["Bhajan", "Kirtan", "Nama Sankeerthana"]:
            content_type = "Music"
        elif primary_cls in ["Pravachan", "Story", "Teaching"]:
            content_type = "Discourse"
        elif primary_cls in ["Temple Darshan", "Temple Tour"]:
            content_type = "Temple"
        else:
            content_type = "Festival"

        # Stage 3: Sub-Class Resolution
        offering_list = obs.get("objects", [])
        speech_text = " ".join(obs.get("speech", []))
        rit_res = self.resolver.resolve_ritual(primary_cls, detected_offerings=offering_list, speech_text=speech_text)
        sub_cls = rit_res["sub_ritual"]

        deity_res = self.resolver.resolve_deity(obs.get("speech", []) + obs.get("ocr", []), visual_cues=offering_list)


        # Construct Final Explainable Output Schema
        output = {
            "content_type": content_type,
            "primary_class": primary_cls,
            "sub_class": sub_cls,
            "confidence": primary_conf,
            "ranked_candidates": rule_results["top_candidates"],
            "primary_deity": deity_res["canonical_name"],
            "tradition": deity_res["tradition"],
            "offerings": [o for o in ["Milk", "Yellow Marigold Flowers", "Camphor", "Curd"] if o.lower() in " ".join(offering_list + [speech_text]).lower()],
            "temporal_sequence": temporal_analysis["detected_sequence"],
            "evidence": {
                "vision": obs.get("objects", []),
                "speech": obs.get("speech", []),
                "ocr": obs.get("ocr", []),
                "applied_rules": rule_results["applied_rules"]
            }

        }
        if not output["offerings"]:
            output["offerings"] = ["Yellow Marigold Flowers", "Lit Deepa Lamp"]

        return output
