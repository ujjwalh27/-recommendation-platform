import subprocess
import os
import cv2
from PIL import Image
from typing import List, Tuple

def extract_audio(video_path: str, output_audio_path: str) -> str:
    """Extracts a mono 16kHz WAV audio track from the video file using ffmpeg."""
    if os.path.exists(output_audio_path):
        try:
            os.remove(output_audio_path)
        except Exception:
            pass
    
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        output_audio_path
    ]
    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    except Exception as e:
        raise RuntimeError(f"FFmpeg audio extraction failed: {e}. Make sure ffmpeg is installed.")
        
    return output_audio_path

def extract_frames(video_path: str, num_frames: int = 5) -> List[Tuple[float, Image.Image]]:
    """Uniformly extracts frames from the video file and returns (timestamp_seconds, PIL Image) tuples."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Could not open video file: {video_path}")
        
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 30.0
    
    # Select frames uniformly
    indices = [int(i * total_frames / (num_frames + 1)) for i in range(1, num_frames + 1)]
    frames = []
    
    for idx in indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if ret:
            # Convert OpenCV BGR to PIL RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(rgb_frame)
            timestamp = round(idx / fps, 2)
            frames.append((timestamp, pil_img))
            
    cap.release()
    return frames
