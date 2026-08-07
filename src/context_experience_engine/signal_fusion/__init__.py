"""
Multimodal Signal Fusion Subsystem
Collects, weights, and fuses evidence signals across MiniCPM, YOLO, VideoMAE, Whisper, AST, OCR, and CLIP.
"""

from .signal_registry import SignalRegistry
from .evidence_collector import EvidenceCollector
from .confidence_fusion import ConfidenceFusionEngine
from .fusion_engine import MultimodalSignalFusionEngine

__all__ = [
    "SignalRegistry",
    "EvidenceCollector",
    "ConfidenceFusionEngine",
    "MultimodalSignalFusionEngine",
]
