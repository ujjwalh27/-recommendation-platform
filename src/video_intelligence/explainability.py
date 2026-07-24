from typing import Dict, Any
from src.video_intelligence.schemas import ProvenanceDetailSchema

class ExplainabilityEngine:
    """Manages natural-language explanations of algorithmic decisions and provenance mappings."""

    def format_provenance_summary(self, provenance: Dict[str, ProvenanceDetailSchema]) -> str:
        """
        Creates a clean structured summary of the confidence scoring and modality sources.
        """
        summary_lines = ["=== Algorithmic Telemetry Provenance Summary ==="]
        for field, detail in provenance.items():
            sources_str = ", ".join(detail.evidence)
            summary_lines.append(
                f"- [{field.upper()}] Confidence: {detail.confidence:.2f} | Sources: [{sources_str}] | Reason: {detail.reason}"
            )
        return "\n".join(summary_lines)

    def generate_field_explanation(self, field_name: str, detail: ProvenanceDetailSchema) -> str:
        """
        Generates a user-facing explanation card explaining why a field got its classification.
        """
        sources_str = ", ".join(detail.evidence)
        return (
            f"Determined using {sources_str} analysis (Confidence: {detail.confidence * 100:.1f}%). "
            f"Reasoning: {detail.reason}"
        )
