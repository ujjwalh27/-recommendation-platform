import torch
from ultralytics import YOLO
from PIL import Image
from typing import List, Tuple, Dict, Any

class ObjectDetector:
    """Local Object Detection module using Ultralytics YOLOv11 (nano model for speed)."""
    
    def __init__(self, model_name="yolo11n.pt"):
        self.model_name = model_name
        # Use CPU for YOLO due to Apple Silicon MPS memory overhead concerns on macOS
        self.device = "cpu"
        if torch.cuda.is_available():
            self.device = "cuda"
            
        print(f"[ObjectDetector] Loading YOLO '{self.model_name}' on {self.device}...")
        self.model = YOLO(self.model_name)

    def detect_objects(self, frames: List[Tuple[float, Image.Image]]) -> List[Dict[str, Any]]:
        """Detects objects across all sampled frames and aggregates unique labels and confidence scores."""
        label_aggregates = {}
        
        for timestamp, pil_img in frames:
            try:
                # Run YOLO prediction (quiet mode)
                results = self.model.predict(source=pil_img, device=self.device, verbose=False)
                
                for r in results:
                    for box in r.boxes:
                        class_id = int(box.cls[0])
                        label = self.model.names[class_id]
                        confidence = float(box.conf[0])
                        
                        if confidence < 0.35: # Filter out low-confidence objects
                            continue
                            
                        if label not in label_aggregates:
                            label_aggregates[label] = []
                        label_aggregates[label].append(confidence)
            except Exception as e:
                print(f"[ObjectDetector] Error during YOLO inference on frame at {timestamp}s: {e}")
                
        # Format and return list of objects sorted by mean confidence
        detected = []
        for label, confs in label_aggregates.items():
            avg_conf = sum(confs) / len(confs)
            detected.append({
                "label": label,
                "count": len(confs),
                "confidence": round(avg_conf, 4)
            })
            
        detected.sort(key=lambda x: x["confidence"], reverse=True)
        return detected
