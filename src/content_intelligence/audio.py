import torch
import librosa
import numpy as np
from transformers import ASTFeatureExtractor, ASTForAudioClassification
from typing import List, Dict, Any

class AudioEventDetector:
    """Local Audio Event Detection using Hugging Face's Audio Spectrogram Transformer (AST)."""
    
    def __init__(self, model_name="MIT/ast-finetuned-audioset-10-10-0.4593"):
        self.model_name = model_name
        # Use CPU for AST audio events due to compatibility issues with MPS compilation on macOS
        self.device = "cpu"
        if torch.cuda.is_available():
            self.device = "cuda"
            
        print(f"[AudioEventDetector] Loading AST model '{self.model_name}' on {self.device}...")
        self.feature_extractor = ASTFeatureExtractor.from_pretrained(model_name)
        self.model = ASTForAudioClassification.from_pretrained(model_name).to(self.device)

    def detect_events(self, audio_path: str) -> List[Dict[str, Any]]:
        """Analyzes the audio file and extracts top classified sounds from AudioSet classes."""
        try:
            # AST requires exactly 16000Hz sampling rate
            y, sr = librosa.load(audio_path, sr=16000, duration=30.0) # limit to first 30 seconds
            
            if len(y) == 0:
                return []
                
            # Preprocess the raw audio amplitude arrays
            inputs = self.feature_extractor(y, sampling_rate=sr, return_tensors="pt")
            
            # Transfer input tensor vectors to device
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = self.model(**inputs)
                
            logits = outputs.logits
            probabilities = logits.softmax(dim=-1).cpu().numpy()[0]
            
            # Sort index array descending
            top_k_indices = np.argsort(probabilities)[::-1][:5]
            
            events = []
            for idx in top_k_indices:
                prob = float(probabilities[idx])
                if prob > 0.05: # threshold
                    label = self.model.config.id2label[idx]
                    clean_label = label.replace("_", " ").replace("-", " ").capitalize()
                    events.append({
                        "event": clean_label,
                        "confidence": round(prob, 4)
                    })
                    
            return events
        except Exception as e:
            print(f"[AudioEventDetector] AST event classification error: {e}")
            return []
