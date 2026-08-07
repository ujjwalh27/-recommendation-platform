from typing import Dict, Any
from .rule_engine import CEEERuleEngine


class EmotionalMetadataEnricher:
    """
    Computes Layer 3 — Emotional Metadata (experiential & recommendation-oriented metadata)
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
        Infers all Layer 3 emotional metadata fields using multimodal evidence signals.
        """
        category = str(canonical_metadata.get("primary_category", ""))
        rules = self.rule_engine.emotional_rules

        emotional_fields = [
            "energy_level", "emotional_tone", "devotional_intensity",
            "ambience", "pace", "immersiveness"
        ]

        emotional_metadata = {}
        for field in emotional_fields:
            field_rules = rules.get(field, [])
            emotional_metadata[field] = self.rule_engine.evaluate_field(
                field_rules=field_rules,
                evidence_doc=evidence_doc,
                category=category
            )

        return emotional_metadata
