import os
import json
from src.semantic_knowledge.daiv_domain_reasoner import DaivDomainReasoner

class DaivHierarchicalMetadataGenerator:
    """
    Hierarchical Metadata Generator for Daiv Recommendation Engine.
    Converts domain-reasoned metadata into structured, hierarchical JSON packages
    optimized for precision recommendation filtering.
    """

    def __init__(self):
        self.reasoner = DaivDomainReasoner()

    def generate_daiv_metadata_package(self, video_id, vision_data, speech_data=None, ocr_data=None, keyframe_seq=None):
        reasoned = self.reasoner.reason_video_intelligence(vision_data, speech_data, ocr_data, keyframe_seq)

        package = {
            "video_id": video_id,
            "daiv_semantic_profile": {
                "taxonomy_hierarchy": {
                    "religion": reasoned["religion"],
                    "tradition": reasoned["tradition"],
                    "primary_deity": reasoned["primary_deity"],
                    "secondary_deities": reasoned["secondary_deities"],
                    "ritual_hierarchy": {
                        "category": reasoned["primary_ritual"],
                        "sub_ritual": reasoned["sub_ritual"],
                        "current_stage": reasoned["ritual_stage"]
                    }
                },
                "spiritual_attributes": {
                    "festival": reasoned["festival"],
                    "occasion": reasoned["occasion"],
                    "offerings": reasoned["offerings"],
                    "sacred_objects": reasoned["sacred_objects"],
                    "mantras": reasoned["mantras"]
                },
                "engagement_context": {
                    "content_type": reasoned["content_type"],
                    "intent": reasoned["intent"],
                    "target_audience": reasoned["audience"],
                    "mood": reasoned["mood"],
                    "language": reasoned["language"]
                },
                "temporal_ritual_flow": reasoned["sequence_of_events"]
            },
            "recommendation_filter_keys": {
                "deity_key": f"{reasoned['religion'].lower()}:{reasoned['tradition'].lower()}:{reasoned['primary_deity'].lower().replace(' ', '_')}",
                "ritual_key": f"{reasoned['primary_ritual'].lower().replace(' ', '_')}:{reasoned['sub_ritual'].lower().replace(' ', '_')}",
                "festival_key": reasoned["festival"].lower().replace(" ", "_"),
                "intent_key": reasoned["intent"].lower().replace(" ", "_")
            },
            "explainability": reasoned["explainability_provenance"],
            "overall_confidence": reasoned["overall_confidence"]
        }
        return package
