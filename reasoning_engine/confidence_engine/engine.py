"""
Task 6 – CMREE Confidence Engine
Computes evidence-grounded confidence scores for every inferred field and attaches
evidence provenance & rule execution trails.
"""

from typing import Dict, Any, List


class CMREEConfidenceEngine:
    """Calculates grounded confidence scores based on cross-modal evidence & rule base scores."""

    def compute_field_confidences(
        self,
        resolved_obs: Dict[str, Any],
        rule_output: Dict[str, Any],
        enriched_metadata: Dict[str, Any]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Computes structured field-level confidence dictionaries containing value, confidence, evidence, rules.
        """
        matched_rules = rule_output.get("matched_rules", [])
        top_rule = matched_rules[0] if matched_rules else None

        field_confidences = {}

        # 1. Primary Ritual Confidence
        rit_val = enriched_metadata.get("primary_ritual", "Devotional Worship")
        base_rit_conf = top_rule.get("base_confidence", 0.85) if top_rule else 0.70
        
        # Modal agreement bonus
        ev_list = []
        if top_rule:
            ev_list.extend(top_rule.get("evidences", []))
        
        ocr_text = " ".join(resolved_obs.get("ocr_text", [])).lower()
        speech_text = resolved_obs.get("speech_text", "").lower()

        agreement_bonus = 0.0
        if rit_val.lower() in ocr_text:
            agreement_bonus += 0.08
            ev_list.append(f"OCR text matches ritual '{rit_val}'")
        if rit_val.lower() in speech_text or "om" in speech_text or "namah" in speech_text:
            agreement_bonus += 0.07
            ev_list.append("Audio speech transcript confirms devotional chanting")

        final_rit_conf = min(0.99, round(base_rit_conf + agreement_bonus, 3))
        rule_ids = [r["rule_id"] for r in matched_rules] if matched_rules else ["DEFAULT_FALLBACK"]

        field_confidences["primary_ritual"] = {
            "value": rit_val,
            "confidence": final_rit_conf,
            "evidence": ev_list or ["Visual keyframe observation"],
            "rules": rule_ids
        }

        # 2. Primary Deity Confidence
        deity_val = enriched_metadata.get("primary_deity")
        if deity_val:
            deity_ev = [f"Entity resolved deity '{deity_val}'"]
            deity_conf = 0.90 if deity_val in resolved_obs.get("canonical_deities", []) else 0.82
            if enriched_metadata.get("temple"):
                deity_conf = min(0.98, deity_conf + 0.08)
                deity_ev.append(f"Associated temple '{enriched_metadata['temple']}' confirms deity")
        else:
            deity_conf = 0.0
            deity_ev = ["No explicit deity evidence detected"]

        field_confidences["primary_deity"] = {
            "value": deity_val,
            "confidence": round(deity_conf, 3),
            "evidence": deity_ev,
            "rules": rule_ids
        }

        # 3. Ritual Family Confidence
        field_confidences["ritual_family"] = {
            "value": enriched_metadata.get("ritual_family", "Abhishekam"),
            "confidence": round(final_rit_conf * 0.98, 3),
            "evidence": [f"Hierarchically derived from primary ritual '{rit_val}'"],
            "rules": rule_ids
        }

        # 4. Overall Document Confidence
        overall_conf = round((final_rit_conf * 0.50) + (deity_conf * 0.50), 3)
        field_confidences["overall"] = {
            "confidence": overall_conf,
            "status": "high_confidence" if overall_conf >= 0.85 else ("moderate_confidence" if overall_conf >= 0.60 else "low_confidence")
        }

        return field_confidences
