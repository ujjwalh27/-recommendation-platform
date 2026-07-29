"""
CMREE – Canonical Metadata Reasoning & Enrichment Engine Pipeline
Master pipeline orchestrating Observation Validation -> Entity Resolution -> Rule Reasoning ->
Metadata Enrichment -> Confidence Scoring -> Explainability -> Canonical Document Generation -> Audit Validation.
"""

from typing import Dict, Any, Tuple, List
from reasoning_engine.observation_schema.validator import ObservationValidator
from reasoning_engine.entity_resolution.resolver import EntityResolver
from reasoning_engine.rule_engine.engine import RuleEngine
from reasoning_engine.enrichment.enricher import MetadataEnricher
from reasoning_engine.confidence_engine.engine import CMREEConfidenceEngine
from reasoning_engine.explainability.engine import ExplainabilityEngine
from reasoning_engine.canonical_metadata.generator import CanonicalMetadataGenerator
from reasoning_engine.validation.validator import MetadataValidator


class CMREEPipeline:
    """Master CMREE reasoning & enrichment pipeline."""

    def __init__(self):
        self.obs_validator = ObservationValidator()
        self.resolver = EntityResolver()
        self.rule_engine = RuleEngine()
        self.enricher = MetadataEnricher()
        self.conf_engine = CMREEConfidenceEngine()
        self.expl_engine = ExplainabilityEngine()
        self.generator = CanonicalMetadataGenerator()
        self.doc_validator = MetadataValidator()

    def process_observation(self, raw_obs: Dict[str, Any]) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Processes a raw VLM observation dictionary through the complete CMREE pipeline.
        Returns:
            (canonical_document, validation_issues)
        """
        # Step 1: Observation Validation
        _, norm_obs, obs_errors = self.obs_validator.validate_and_normalize(raw_obs)

        # Step 2: Entity Resolution
        resolved_obs = self.resolver.resolve_observation(norm_obs)

        # Step 3: Rule-Based Reasoning
        rule_output = self.rule_engine.evaluate(resolved_obs)

        # Step 4: Metadata Enrichment
        enriched_metadata = self.enricher.enrich(resolved_obs, rule_output)

        # Step 5: Confidence Engine
        field_confidences = self.conf_engine.compute_field_confidences(resolved_obs, rule_output, enriched_metadata)

        # Step 6: Explainability Engine
        reasoning_trace = self.expl_engine.generate_trace(
            raw_obs, resolved_obs, rule_output, enriched_metadata, field_confidences
        )

        # Step 7: Canonical Metadata Document Generation
        canonical_doc = self.generator.generate_canonical_document(
            video_id=norm_obs["video_id"],
            resolved_obs=resolved_obs,
            enriched_metadata=enriched_metadata,
            field_confidences=field_confidences,
            reasoning_trace=reasoning_trace
        )

        # Step 8: Document Validation
        _, validation_issues = self.doc_validator.validate_canonical_document(canonical_doc)

        return canonical_doc, validation_issues
