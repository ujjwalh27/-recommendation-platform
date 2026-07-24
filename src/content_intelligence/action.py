import numpy as np
import torch
from PIL import Image
from transformers import VideoMAEImageProcessor, VideoMAEForVideoClassification
from typing import List, Tuple, Dict, Any

class ActionRecognizer:
    """Action Recognition using VideoMAE to analyze motion across frame sequences."""
    
    def __init__(self, model_name="MCG-NJU/videomae-base-short-finetuned-kinetics"):
        self.model_name = model_name
        # Use CPU for VideoMAE due to stability issues with MPS compilation on macOS
        self.device = "cpu"
        if torch.cuda.is_available():
            self.device = "cuda"
            
        print(f"[ActionRecognizer] Loading VideoMAE '{self.model_name}' on {self.device}...")
        self.processor = VideoMAEImageProcessor.from_pretrained(model_name)
        self.model = VideoMAEForVideoClassification.from_pretrained(model_name).to(self.device)

    def recognize_actions(self, frames: List[Tuple[float, Image.Image]]) -> List[Dict[str, Any]]:
        """Processes video frame sequences as a clip and predicts the top motion activities."""
        if not frames:
            return []
            
        try:
            # extract PIL images
            pil_images = [img for _, img in frames]
            
            # VideoMAE usually expects exactly 16 frames. 
            # We will pad by repeating the last frame if sequence is short.
            if len(pil_images) == 0:
                return []
                
            while len(pil_images) < 16:
                pil_images.append(pil_images[-1])
            pil_images = pil_images[:16]
            
            # Preprocess the video clip
            inputs = self.processor(pil_images, return_tensors="pt")
            
            # Transfer input tensors to device
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = self.model(**inputs)
                
            logits = outputs.logits
            probabilities = logits.softmax(dim=-1).cpu().numpy()[0]
            
            # Retrieve the top-5 predicted kinetics action indices
            top_k_indices = np.argsort(probabilities)[::-1][:5]
            
            actions = []
            for idx in top_k_indices:
                prob = float(probabilities[idx])
                if prob > 0.20: # threshold to eliminate spurious background motion noise
                    label = self.model.config.id2label[idx]
                    clean_label = label.replace("_", " ").replace("-", " ").capitalize()
                    actions.append({
                        "action": clean_label,
                        "confidence": round(prob, 4)
                    })
                    
            return actions
        except Exception as e:
            print(f"[ActionRecognizer] VideoMAE inference error: {e}")
            return []
