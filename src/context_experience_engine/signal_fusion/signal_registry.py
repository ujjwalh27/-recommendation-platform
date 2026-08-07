from typing import Dict, Any, List


class SignalRegistry:
    """
    Registry for all perception model signals, default contribution weights,
    and fallback mechanisms used in Multimodal Signal Fusion.
    """

    SUPPORTED_MODELS = ["MiniCPM", "YOLO", "VideoMAE", "Whisper", "AST", "OCR", "CLIP"]

    DEFAULT_WEIGHTS = {
        "MiniCPM": 0.30,
        "YOLO": 0.20,
        "VideoMAE": 0.15,
        "Whisper": 0.15,
        "AST": 0.10,
        "OCR": 0.05,
        "CLIP": 0.05
    }

    SIGNAL_MAP = {
        "MiniCPM": ["summary", "narrative", "ritual_description", "inferred_objects"],
        "YOLO": ["objects", "object_counts", "person_count", "lamp_count", "flower_count", "vessel_count", "idol_detected"],
        "VideoMAE": ["actions", "motion_level", "kinetic_intensity"],
        "Whisper": ["transcript", "speech_speed", "chants", "silence_duration"],
        "AST": ["audio_events", "bells", "drums", "chanting", "music", "crowd_noise"],
        "OCR": ["ocr_text", "temple_names", "banners"],
        "CLIP": ["scene_environment", "visual_tags"]
    }

    def __init__(self, custom_weights: Dict[str, float] = None):
        self.weights = self.DEFAULT_WEIGHTS.copy()
        if custom_weights:
            self.weights.update(custom_weights)
        self.normalize_weights()

    def normalize_weights(self):
        """Ensures all model weights sum to 1.0."""
        total = sum(self.weights.values())
        if total > 0:
            for k in self.weights:
                self.weights[k] = round(self.weights[k] / total, 4)

    def get_weight(self, model_name: str) -> float:
        return self.weights.get(model_name, 0.05)

    def list_models(self) -> List[str]:
        return self.SUPPORTED_MODELS.copy()
