"""
Task 4 – Rule-Based Reasoning Engine
Evaluates explainable inference rules against normalized & resolved observations.
Produces deterministic ritual classifications, deity inferences, and rule execution logs.
"""

import os
import re
from typing import Dict, Any, List, Tuple, Optional

try:
    import yaml
    YAML_AVAIL = True
except ImportError:
    YAML_AVAIL = False


class RuleEngine:
    """Executes rule-based inference against resolved observations."""

    def __init__(self, rules_path: str = None):
        if rules_path is None:
            rules_path = os.path.join(os.path.dirname(__file__), "reasoning_rules.yaml")
        
        self.rules_path = rules_path
        self.rules = []
        self.load_rules()

    def load_rules(self):
        """Loads reasoning rules from YAML."""
        if not os.path.exists(self.rules_path):
            print(f"[CMREE-RuleEngine] Warning: Rules file not found at {self.rules_path}")
            return

        try:
            if YAML_AVAIL:
                with open(self.rules_path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
                    self.rules = data.get("rules", [])
            print(f"[CMREE-RuleEngine] Loaded {len(self.rules)} active reasoning rules.")
        except Exception as e:
            print(f"[CMREE-RuleEngine] Error loading rules: {e}")

    def evaluate(self, resolved_obs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluates all rules against the resolved observation.
        Returns:
            {
                "matched_rules": [...],
                "inferred_primary_ritual": str or None,
                "inferred_primary_category": str or None,
                "inferred_primary_deity": str or None,
                "inferred_offerings": [...],
                "rule_trace": [...]
            }
        """
        matched_rules = []
        rule_trace = []
        combined_text = (
            resolved_obs.get("scene", "") + " " +
            " ".join(resolved_obs.get("ocr_text", [])) + " " +
            resolved_obs.get("speech_text", "")
        )

        canonical_objs = set(resolved_obs.get("canonical_objects", []))
        canonical_acts = set(resolved_obs.get("canonical_actions", []))
        canonical_deities = set(resolved_obs.get("canonical_deities", []))

        for rule in self.rules:
            rule_id = rule.get("id")
            rule_name = rule.get("name")
            conds = rule.get("conditions", {})
            outputs = rule.get("output", {})
            explanation = rule.get("explanation", "")

            matched_evidences = []

            # Check objects_any
            obj_cond = conds.get("objects_any", [])
            if obj_cond:
                obj_matches = [o for o in obj_cond if o in canonical_objs]
                if obj_matches:
                    matched_evidences.append(f"Detected object(s): {', '.join(obj_matches)}")
                else:
                    continue

            # Check actions_any
            act_cond = conds.get("actions_any", [])
            if act_cond:
                act_matches = [a for a in act_cond if a in canonical_acts]
                if act_matches:
                    matched_evidences.append(f"Detected action(s): {', '.join(act_matches)}")
                else:
                    continue

            # Check deities_any
            deity_cond = conds.get("deities_any", [])
            if deity_cond:
                deity_matches = [d for d in deity_cond if d in canonical_deities]
                if deity_matches:
                    matched_evidences.append(f"Detected deity: {', '.join(deity_matches)}")
                else:
                    continue

            # Check text_contains
            text_cond = conds.get("text_contains", [])
            if text_cond:
                text_matches = [t for t in text_cond if re.search(r'\b' + re.escape(t) + r'\b', combined_text, re.IGNORECASE)]
                if text_matches:
                    matched_evidences.append(f"Text/Transcript matched: '{', '.join(text_matches)}'")
                else:
                    continue

            # Rule triggered!
            matched_rules.append({
                "rule_id": rule_id,
                "rule_name": rule_name,
                "output": outputs,
                "base_confidence": rule.get("base_confidence", 0.90),
                "evidences": matched_evidences,
                "explanation": explanation
            })
            rule_trace.append(f"[{rule_id}] Triggered: {explanation} (Evidences: {'; '.join(matched_evidences)})")

        # Pick top matched rule by base_confidence
        inferred_ritual = None
        inferred_category = None
        inferred_deity = None
        offerings = set()

        if matched_rules:
            matched_rules.sort(key=lambda r: r["base_confidence"], reverse=True)
            top_rule = matched_rules[0]
            inferred_ritual = top_rule["output"].get("primary_ritual")
            fallback_cat = "Any other devotional or temple-related activities"
            inferred_category = top_rule["output"].get("primary_category", fallback_cat)
            inferred_deity = top_rule["output"].get("primary_deity")

            for mr in matched_rules:
                off = mr["output"].get("offering")
                if off:
                    offerings.add(off)

        fallback_cat = "Any other devotional or temple-related activities"
        return {
            "matched_rules": matched_rules,
            "inferred_primary_ritual": inferred_ritual,
            "inferred_primary_category": inferred_category or fallback_cat,
            "inferred_primary_deity": inferred_deity,
            "inferred_offerings": sorted(list(offerings)),
            "rule_trace": rule_trace
        }
