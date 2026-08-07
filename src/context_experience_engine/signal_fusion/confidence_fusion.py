import os
from typing import Dict, Any, List, Optional

try:
    import yaml
    YAML_AVAIL = True
except ImportError:
    YAML_AVAIL = False

from .signal_registry import SignalRegistry


class ConfidenceFusionEngine:
    """
    Computes dynamic weighted confidence scores across contributing perception models
    (MiniCPM, YOLO, VideoMAE, Whisper, AST, OCR, CLIP) based on configurable signal weights.
    """

    def __init__(self, config_path: Optional[str] = None):
        if config_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            config_path = os.path.join(base_dir, "config", "signal_weights.yaml")

        self.registry = SignalRegistry()
        self.config_path = config_path
        self.load_config()

    def load_config(self):
        """Loads model weights from external YAML config if available."""
        if os.path.exists(self.config_path) and YAML_AVAIL:
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
                weights = data.get("weights", {})
                if weights:
                    self.registry = SignalRegistry(custom_weights=weights)
            print(f"[ConfidenceFusion] Loaded model weights from {self.config_path}")

    def compute_field_confidence(
        self,
        contributing_evidence: List[Dict[str, Any]],
        base_rule_confidence: float = 0.80,
        confidence_modifier: float = 0.0
    ) -> float:
        """
        Calculates dynamic weighted confidence score:
        Sum(weight(model_i) * base_confidence(model_i)) / Sum(weight(model_i)) + modifier
        """
        if not contributing_evidence:
            return round(max(0.50, min(0.99, base_rule_confidence + confidence_modifier)), 2)

        weighted_sum = 0.0
        total_weight = 0.0

        for item in contributing_evidence:
            model = item.get("source", "MiniCPM")
            model_weight = self.registry.get_weight(model)
            model_conf = float(item.get("confidence", base_rule_confidence))

            weighted_sum += model_weight * model_conf
            total_weight += model_weight

        if total_weight > 0:
            fused_conf = weighted_sum / total_weight
        else:
            fused_conf = base_rule_confidence

        final_score = fused_conf + confidence_modifier
        return round(max(0.50, min(0.98, final_score)), 2)
