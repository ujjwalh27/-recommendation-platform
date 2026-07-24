import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from typing import List, Tuple, Dict, Any

class SceneUnderstander:
    """Zero-shot Scene Understanding using CLIP to classify frames against environment concepts."""
    
    def __init__(self, model_name="openai/clip-vit-base-patch32"):
        self.model_name = model_name
        # Use CPU for CLIP due to Apple Silicon MPS compilation compatibility issues
        self.device = "cpu"
        if torch.cuda.is_available():
            self.device = "cuda"
            
        print(f"[SceneUnderstander] Loading CLIP '{self.model_name}' on {self.device}...")
        self.model = CLIPModel.from_pretrained(model_name).to(self.device)
        self.processor = CLIPProcessor.from_pretrained(model_name)
        
        # Predefined scene candidates for zero-shot text classification
        self.scene_labels = [
            "a temple, shrine, or devotional place",
            "a person talking to camera in a reel or video",
            "an indoor home room or studio",
            "an audition or performance setup",
            "an indoor living room",
            "an outdoor natural landscape",
            "a busy city street",
            "an office desk environment",
            "a computer screen or software UI",
            "a gaming set with glowing LEDs",
            "a kitchen cooking set",
            "a stage with music performance",
            "a gym or athletic field",
            "a podcast or news recording studio",
            "the inside of a car or vehicle"
        ]

    def classify_scenes(self, frames: List[Tuple[float, Image.Image]]) -> List[Dict[str, Any]]:
        """Classifies each video frame and returns aggregated scene environments with confidences."""
        scene_scores = {lbl: [] for lbl in self.scene_labels}
        
        for timestamp, pil_img in frames:
            try:
                inputs = self.processor(
                    text=self.scene_labels,
                    images=pil_img,
                    return_tensors="pt",
                    padding=True
                )
                
                # Transfer inputs to local acceleration device
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
                
                with torch.no_grad():
                    outputs = self.model(**inputs)
                
                # Extract similarity probabilities
                logits_per_image = outputs.logits_per_image
                probs = logits_per_image.softmax(dim=-1).cpu().numpy()[0]
                
                for idx, score in enumerate(probs):
                    label = self.scene_labels[idx]
                    scene_scores[label].append(float(score))
            except Exception as e:
                print(f"[SceneUnderstander] CLIP error on frame at {timestamp}s: {e}")
                
        # Formulate scene summaries
        results = []
        for label, scores in scene_scores.items():
            if scores:
                avg_score = sum(scores) / len(scores)
                if avg_score > 0.08: # Only return meaningful scene matches
                    # Make name user-friendly
                    clean_label = label.replace("an ", "").replace("a ", "").replace("the ", "").capitalize()
                    results.append({
                        "concept": clean_label,
                        "confidence": round(avg_score, 4)
                    })
                    
        results.sort(key=lambda x: x["confidence"], reverse=True)
        return results
