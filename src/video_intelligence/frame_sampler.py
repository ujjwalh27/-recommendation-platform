import os
import cv2
import numpy as np
import subprocess
from PIL import Image
from typing import List, Tuple, Dict, Any
from src.video_intelligence.config import TEMP_DIR, SCENE_THRESHOLD, MAX_SAMPLED_FRAMES, MIN_SCENE_DURATION_S
from src.content_intelligence.utils import extract_audio

class VideoPreprocessor:
    """Handles audio demuxing and dynamic scene-based keyframe sampling from video files."""

    def __init__(self, temp_dir: str = None):
        self.temp_dir = temp_dir or TEMP_DIR
        os.makedirs(self.temp_dir, exist_ok=True)

    def process(self, video_path: str, video_id: str) -> Dict[str, Any]:
        """
        Extracts WAV audio and dynamically samples keyframes using color histogram differences.
        
        Returns:
            Dict containing audio_path and list of sampled frame details.
        """
        video_temp_dir = os.path.join(self.temp_dir, video_id)
        os.makedirs(video_temp_dir, exist_ok=True)

        # 1. Demux audio track
        audio_path = os.path.join(video_temp_dir, "audio.wav")
        audio_extracted = False
        try:
            extract_audio(video_path, audio_path)
            audio_extracted = os.path.exists(audio_path) and os.path.getsize(audio_path) > 0
        except Exception as e:
            print(f"[Preprocessor] Audio extraction warning: {e}. Video may not contain audio.")

        # 2. Dynamic Scene/Keyframe Sampling
        sampled_frames = self._detect_scenes_and_sample(video_path, video_temp_dir)

        return {
            "video_id": video_id,
            "video_path": video_path,
            "audio_path": audio_path if audio_extracted else None,
            "temp_dir": video_temp_dir,
            "frames": sampled_frames
        }

    def _detect_scenes_and_sample(self, video_path: str, output_dir: str) -> List[Dict[str, Any]]:
        """
        Uses OpenCV color histogram differences to identify scene boundaries and extracts representative frames.
        """
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Could not open video file: {video_path}")

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps <= 0:
            fps = 30.0
        
        duration = total_frames / fps
        
        # Step through the video at 1-second intervals for fast analysis
        step = max(1, int(fps))
        prev_hist = None
        scene_changes = [] # list of (timestamp_seconds, frame_index)

        for frame_idx in range(0, total_frames, step):
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, frame = cap.read()
            if not ret:
                break
            
            # Convert to HSV for robust color comparison
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # Compute 2D histogram on Hue & Saturation
            hist = cv2.calcHist([hsv], [0, 1], None, [16, 16], [0, 180, 0, 256])
            cv2.normalize(hist, hist)
            
            timestamp = round(frame_idx / fps, 2)
            
            if prev_hist is not None:
                # Compare histograms using correlation (1.0 = perfect match, 0.0 = completely different)
                correlation = cv2.compareHist(prev_hist, hist, cv2.HISTCMP_CORREL)
                difference = 1.0 - correlation
                
                # Check scene change criteria
                if difference >= SCENE_THRESHOLD:
                    if not scene_changes or (timestamp - scene_changes[-1][0] >= MIN_SCENE_DURATION_S):
                        scene_changes.append((timestamp, frame_idx, difference))
            else:
                # Always include the first frame
                scene_changes.append((timestamp, frame_idx, 1.0))
                
            prev_hist = hist

        # Fallback: if no scene changes were detected (e.g. extremely static or dark video),
        # perform uniform sampling to guarantee we have representative visual data.
        if len(scene_changes) <= 1:
            scene_changes = []
            num_fallback_frames = 5
            indices = [int(i * total_frames / (num_fallback_frames + 1)) for i in range(1, num_fallback_frames + 1)]
            # Include start and end boundaries
            indices = [0] + indices + [total_frames - 1]
            for idx in indices:
                ts = round(idx / fps, 2)
                scene_changes.append((ts, idx, 0.5))

        # Sort scene changes by structural difference descending and limit to MAX_SAMPLED_FRAMES
        # but keep temporal chronological ordering for final frame outputs.
        if len(scene_changes) > MAX_SAMPLED_FRAMES:
            # Sort by difference score to keep high-contrast frame changes
            scene_changes.sort(key=lambda x: x[2], reverse=True)
            scene_changes = scene_changes[:MAX_SAMPLED_FRAMES]
            
        # Re-sort chronologically by timestamp
        scene_changes.sort(key=lambda x: x[0])

        # Extract and save frames
        frames_list = []
        for idx, (ts, f_idx, diff) in enumerate(scene_changes):
            cap.set(cv2.CAP_PROP_POS_FRAMES, f_idx)
            ret, frame = cap.read()
            if ret:
                frame_name = f"frame_{idx:03d}_{int(ts)}s.jpg"
                frame_path = os.path.join(output_dir, frame_name)
                # Save frame
                cv2.imwrite(frame_path, frame)
                
                # Check resolution
                height, width, _ = frame.shape
                
                frames_list.append({
                    "index": idx,
                    "frame_index": f_idx,
                    "timestamp": ts,
                    "difference_score": float(diff),
                    "image_path": frame_path,
                    "width": width,
                    "height": height
                })
                
        cap.release()
        print(f"[Preprocessor] Processed video: {len(frames_list)} keyframes sampled based on visual changes.")
        return frames_list
