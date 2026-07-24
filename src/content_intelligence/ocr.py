import numpy as np
from PIL import Image
from typing import List, Tuple, Dict, Any

class OCRDetector:
    """Local Screen OCR text extractor using PyTorch-native EasyOCR."""
    
    def __init__(self):
        print("[OCRDetector] Loading EasyOCR (English)...")
        import easyocr
        # Disable GPU for EasyOCR as it frequently hangs on Apple Silicon MPS
        self.reader = easyocr.Reader(['en'], gpu=False)

    def extract_text(self, frames: List[Tuple[float, Image.Image]]) -> List[Dict[str, Any]]:
        """Processes a list of video frames, performing text extraction on each."""
        results = []
        for timestamp, pil_img in frames:
            try:
                # Convert PIL image to a numpy array for EasyOCR
                frame_np = np.array(pil_img)
                detections = self.reader.readtext(frame_np)
                
                texts = []
                confidences = []
                
                for bbox, text, prob in detections:
                    text_str = text.strip()
                    if len(text_str) > 0 and prob > 0.35:
                        texts.append(text_str)
                        confidences.append(float(prob))
                
                if texts:
                    avg_confidence = sum(confidences) / len(confidences)
                    results.append({
                        "timestamp": timestamp,
                        "text": " | ".join(texts),
                        "confidence": round(avg_confidence, 4)
                    })
            except Exception as e:
                print(f"[OCRDetector] Error running OCR on frame at {timestamp}s: {e}")
                
        return results
