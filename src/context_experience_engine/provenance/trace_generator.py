from typing import Dict, Any, List


class ReasoningTraceGenerator:
    """
    Generates detailed human-readable reasoning traces for every enriched metadata field.
    Includes exact evidence items, source models, confidence contributions, and applied rule IDs.
    """

    def generate_traces(
        self,
        perceptual_metadata: Dict[str, Any],
        emotional_metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Creates a dictionary of formatted reasoning traces.
        """
        traces = {}

        for layer_name, meta_dict in [("Perceptual", perceptual_metadata), ("Emotional", emotional_metadata)]:
            for field, item in meta_dict.items():
                val = item.get("value", "Unspecified")
                conf = item.get("confidence", 0.80)
                rules = item.get("rules", ["RULE_DEFAULT"])
                evidence_list = item.get("evidence", [])

                ev_lines = []
                for ev in evidence_list:
                    if isinstance(ev, dict):
                        ev_lines.append(f"✓ [{ev.get('source', 'Model')}] {ev.get('value', '')}")
                    else:
                        ev_lines.append(f"✓ {ev}")

                ev_str = " | ".join(ev_lines) if ev_lines else "✓ Multimodal observation layer"
                rule_str = ", ".join(rules)

                trace_text = (
                    f"Field: {field.replace('_', ' ').title()} -> Value: {val} | "
                    f"Confidence: {conf} | Applied Rules: [{rule_str}] | Evidence: {ev_str}"
                )

                traces[f"{layer_name.lower()}_{field}"] = {
                    "field": field,
                    "layer": layer_name,
                    "inferred_value": val,
                    "confidence": conf,
                    "applied_rules": rules,
                    "evidence_items": evidence_list,
                    "human_readable_trace": trace_text,
                    "reasoning": item.get("reason", "")
                }

        return traces
