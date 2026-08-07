import os
from typing import Dict, Any, List, Optional

try:
    import yaml
    YAML_AVAIL = True
except ImportError:
    YAML_AVAIL = False

from .signal_fusion.confidence_fusion import ConfidenceFusionEngine


class CEEERuleEngine:
    """
    Multimodal Rule Engine for MSFACR.
    Evaluates multimodal evidence rules against structured Evidence Documents,
    calculates dynamic weighted confidence, and builds complete evidence provenance objects.
    """

    def __init__(self, rules_dir: Optional[str] = None):
        if rules_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            top_rules_dir = os.path.join(base_dir, "rules")
            pkg_rules_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rules")
            rules_dir = top_rules_dir if os.path.exists(top_rules_dir) else pkg_rules_dir

        self.rules_dir = rules_dir
        self.perceptual_rules = {}
        self.emotional_rules = {}
        self.confidence_fusion = ConfidenceFusionEngine()
        self.load_rules()

    def load_rules(self):
        """Loads external YAML rules dynamically."""
        perc_path = os.path.join(self.rules_dir, "perceptual_rules.yaml")
        emo_path = os.path.join(self.rules_dir, "emotional_rules.yaml")

        if os.path.exists(perc_path) and YAML_AVAIL:
            with open(perc_path, "r", encoding="utf-8") as f:
                self.perceptual_rules = (yaml.safe_load(f) or {}).get("rules", {})
            print(f"[CEEE-RuleEngine] Loaded multimodal perceptual rules from {perc_path}")

        if os.path.exists(emo_path) and YAML_AVAIL:
            with open(emo_path, "r", encoding="utf-8") as f:
                self.emotional_rules = (yaml.safe_load(f) or {}).get("rules", {})
            print(f"[CEEE-RuleEngine] Loaded multimodal emotional rules from {emo_path}")

    def evaluate_field(
        self,
        field_rules: List[Dict[str, Any]],
        evidence_doc: Dict[str, Any],
        category: str = ""
    ) -> Dict[str, Any]:
        """
        Evaluates multimodal field rules against Evidence Document.
        Returns a rich explainable object containing:
        value, confidence, evidence (list of {"source": ..., "value": ...}), rules, reason.
        """
        visual = evidence_doc.get("visual", {})
        videomae = evidence_doc.get("videomae", {})
        audio = evidence_doc.get("audio", {})
        whisper = evidence_doc.get("whisper", {})
        ocr = evidence_doc.get("text", {})
        clip = evidence_doc.get("clip", {})
        vlm = evidence_doc.get("vlm", {})

        vlm_summary = vlm.get("summary", "").lower()
        clip_labels = " ".join(clip.get("clip_labels", [])).lower()
        objects_str = " ".join(visual.get("objects", [])).lower()
        actions_str = " ".join(videomae.get("actions", [])).lower()
        transcript = whisper.get("transcript", "").lower()

        matched_rule = None
        contributing_evidence = []

        # Sort rules by priority descending
        sorted_rules = sorted(field_rules, key=lambda r: r.get("priority", 1), reverse=True)

        for rule in sorted_rules:
            conds = rule.get("conditions", {})
            if not conds:  # Default rule
                matched_rule = rule
                break

            match = True
            rule_evs = []

            # Check CLIP conditions
            clip_cond = conds.get("clip_contains", [])
            if clip_cond:
                if any(c in clip_labels or c in clip.get("environment", "") for c in clip_cond):
                    rule_evs.append({"source": "CLIP", "value": f"classified scene as {clip.get('environment', 'sacred')}"})
                else:
                    match = False
                    continue

            # Check YOLO conditions
            yolo_cond = conds.get("yolo_contains", [])
            if yolo_cond:
                found_objs = [o for o in yolo_cond if o in objects_str]
                if found_objs:
                    rule_evs.append({"source": "YOLO", "value": f"detected objects [{', '.join(found_objs[:3])}]"})
                else:
                    match = False
                    continue

            # Check YOLO person count
            min_p = conds.get("yolo_min_persons")
            if min_p is not None and visual.get("person_count", 0) < min_p:
                match = False
                continue

            max_p = conds.get("yolo_max_persons")
            if max_p is not None and visual.get("person_count", 0) > max_p:
                match = False
                continue

            # Check MiniCPM conditions
            vlm_cond = conds.get("minicpm_contains", [])
            if vlm_cond:
                found_vlm = [v for v in vlm_cond if v in vlm_summary]
                if found_vlm:
                    rule_evs.append({"source": "MiniCPM", "value": f"summary described '{found_vlm[0]}'"})
                else:
                    match = False
                    continue

            # Check VideoMAE conditions
            vmae_cond = conds.get("videomae_contains", [])
            if vmae_cond:
                found_act = [a for a in vmae_cond if a in actions_str or a in videomae.get("motion_level", "").lower()]
                if found_act:
                    rule_evs.append({"source": "VideoMAE", "value": f"action '{found_act[0]}'"})
                else:
                    match = False
                    continue

            # Check Whisper conditions
            wsp_cond = conds.get("whisper_contains", [])
            if wsp_cond:
                found_wsp = [w for w in wsp_cond if w in transcript or (w == "slow" and whisper.get("speech_speed") == "slow")]
                if found_wsp:
                    rule_evs.append({"source": "Whisper", "value": f"transcript chant '{found_wsp[0]}'"})
                else:
                    match = False
                    continue

            # Check AST audio events
            ast_cond = conds.get("ast_contains", [])
            if ast_cond:
                found_ast = [a for a in ast_cond if audio.get(a, False)]
                if found_ast:
                    rule_evs.append({"source": "AST", "value": f"audio event '{found_ast[0]}'"})
                else:
                    match = False
                    continue

            if match:
                matched_rule = rule
                contributing_evidence = rule_evs
                break

        if not matched_rule:
            matched_rule = {
                "id": "RULE_DEFAULT_FALLBACK",
                "output": {"value": "Normal", "reason": "Standard inference based on observation layer."},
                "confidence_modifier": 0.0
            }

        # Fallback evidence if rule contributing evidence is empty
        if not contributing_evidence:
            if vlm_summary:
                contributing_evidence.append({"source": "MiniCPM", "value": vlm_summary[:40]})
            if visual.get("objects"):
                contributing_evidence.append({"source": "YOLO", "value": f"objects {visual.get('objects')[:2]}"})
            if clip.get("environment"):
                contributing_evidence.append({"source": "CLIP", "value": clip.get("environment")})

        out = matched_rule.get("output", {})
        val = out.get("value", "Normal")
        reason = out.get("reason", "Inferred from multimodal signal fusion.")
        rule_id = matched_rule.get("id", "RULE_DEFAULT")
        mod = matched_rule.get("confidence_modifier", 0.0)

        # Dynamic confidence calculation
        fused_confidence = self.confidence_fusion.compute_field_confidence(
            contributing_evidence=contributing_evidence,
            base_rule_confidence=0.82,
            confidence_modifier=mod
        )

        return {
            "value": val,
            "confidence": fused_confidence,
            "evidence": contributing_evidence,
            "rules": [rule_id],
            "reason": reason
        }
