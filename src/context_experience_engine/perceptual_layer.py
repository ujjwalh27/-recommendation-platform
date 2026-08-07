from typing import Dict, Any
from .rule_engine import CEEERuleEngine


class PerceptualMetadataEnricher:
    """
    Computes Layer 2 — Perceptual Metadata (scene-level objective metadata)
    using the Multimodal Evidence Document and MSFACR Rule Engine.
    """

    def __init__(self, rule_engine: CEEERuleEngine):
        self.rule_engine = rule_engine

    def enrich(
        self,
        evidence_doc: Dict[str, Any],
        canonical_metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Infers all Layer 2 perceptual metadata fields using multimodal evidence signals.
        """
        category = str(canonical_metadata.get("primary_category", ""))
        rules = self.rule_engine.perceptual_rules

        perceptual_fields = [
            "environment", "lighting", "camera_motion", "camera_distance",
            "camera_angle", "crowd_size", "visual_complexity", "motion_level",
            "decoration_level", "scene_density"
        ]

        perceptual_metadata = {}
        for field in perceptual_fields:
            field_rules = rules.get(field, [])
            perceptual_metadata[field] = self.rule_engine.evaluate_field(
                field_rules=field_rules,
                evidence_doc=evidence_doc,
                category=category
            )

        return perceptual_metadata
