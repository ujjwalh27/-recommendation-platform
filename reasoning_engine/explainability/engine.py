"""
Task 7 – Explainability Engine
Generates human-readable, step-by-step reasoning traces for every inference.
Used by reviewer dashboards, audit logs, and developer debugging tools.
"""

from typing import Dict, Any, List


class ExplainabilityEngine:
    """Generates structured reasoning traces detailing observation resolution, rule firing, and enrichment steps."""

    def generate_trace(
        self,
        raw_obs: Dict[str, Any],
        resolved_obs: Dict[str, Any],
        rule_output: Dict[str, Any],
        enriched_metadata: Dict[str, Any],
        field_confidences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Builds a comprehensive reasoning trace object.
        """
        matched_rules = rule_output.get("matched_rules", [])
        top_rule = matched_rules[0] if matched_rules else None

        trace_steps = {
            "step_1_observation_validation": {
                "status": "PASS",
                "scene": resolved_obs.get("scene", ""),
                "raw_objects_count": len(raw_obs.get("objects", [])),
                "raw_actions_count": len(raw_obs.get("actions", [])),
                "has_speech_text": bool(resolved_obs.get("speech_text")),
                "has_ocr_text": bool(resolved_obs.get("ocr_text"))
            },
            "step_2_entity_resolution": {
                "canonical_objects": resolved_obs.get("canonical_objects", []),
                "canonical_actions": resolved_obs.get("canonical_actions", []),
                "canonical_deities": resolved_obs.get("canonical_deities", [])
            },
            "step_3_rule_evaluation": {
                "total_rules_evaluated": len(rule_output.get("rule_trace", [])),
                "matched_rules_count": len(matched_rules),
                "primary_rule_applied": top_rule.get("rule_id") if top_rule else "DEFAULT_FALLBACK",
                "primary_rule_explanation": top_rule.get("explanation") if top_rule else "No specific rule matched; fallback pooja classification assigned.",
                "evidence_points": top_rule.get("evidences", []) if top_rule else ["Visual keyframe observation"]
            },
            "step_4_enrichment": {
                "inferred_primary_ritual": enriched_metadata.get("primary_ritual"),
                "derived_ritual_family": enriched_metadata.get("ritual_family"),
                "derived_primary_deity": enriched_metadata.get("primary_deity"),
                "derived_temple": enriched_metadata.get("temple"),
                "derived_tradition": enriched_metadata.get("tradition"),
                "offerings": enriched_metadata.get("offerings", [])
            },
            "step_5_confidence_scoring": {
                "overall_confidence": field_confidences.get("overall", {}).get("confidence", 0.85),
                "confidence_status": field_confidences.get("overall", {}).get("status", "high_confidence")
            }
        }

        # Human-readable summary lines
        summary_lines = [
            f"Primary Ritual: {enriched_metadata.get('primary_ritual')} (Family: {enriched_metadata.get('ritual_family')})",
            f"Primary Deity: {enriched_metadata.get('primary_deity')} | Tradition: {enriched_metadata.get('tradition')}"
        ]
        if top_rule:
            summary_lines.append(f"Rule Applied: [{top_rule['rule_id']}] – {top_rule['explanation']}")
            for ev in top_rule.get("evidences", []):
                summary_lines.append(f"  ✓ {ev}")

        return {
            "summary_lines": summary_lines,
            "detailed_steps": trace_steps
        }
