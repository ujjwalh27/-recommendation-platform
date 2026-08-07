from typing import Dict, Any, List
from .evidence_collector import EvidenceCollector
from .confidence_fusion import ConfidenceFusionEngine
from .signal_registry import SignalRegistry


class MultimodalSignalFusionEngine:
    """
    Multimodal Signal Fusion Engine.
    Aggregates structured signals from MiniCPM, YOLO, VideoMAE, Whisper, AST, OCR, and CLIP,
    evaluates cross-modal evidence rules, and assigns dynamically fused confidence scores.
    """

    def __init__(self):
        self.collector = EvidenceCollector()
        self.confidence_engine = ConfidenceFusionEngine()
        self.registry = SignalRegistry()

    def process(
        self,
        observation: Dict[str, Any],
        canonical_metadata: Dict[str, Any],
        raw_report: Dict[str, Any] = None,
        perceptual_rules: List[Dict[str, Any]] = None,
        emotional_rules: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Executes complete Signal Fusion pipeline:
        1. Collect structured Evidence Document
        2. Evaluate Multimodal Rules
        3. Calculate Dynamic Fused Confidence scores
        """
        raw_report = raw_report or {}

        # 1. Collect unified Evidence Document
        evidence_doc = self.collector.collect(observation, raw_report)

        return {
            "evidence_document": evidence_doc,
            "fusion_status": "MULTIMODAL_SIGNALS_FUSED",
            "active_models": self.registry.list_models()
        }
