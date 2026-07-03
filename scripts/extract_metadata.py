from pathlib import Path
import cv2
import pandas as pd
from tqdm import tqdm

VIDEO_DIR = Path("datasets/raw/videos")
OUTPUT_FILE = Path("datasets/processed/video_metadata.csv")

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

rows = []

video_files = sorted(VIDEO_DIR.glob("*.mp4"))

print(f"Found {len(video_files)} videos")

for video_path in tqdm(video_files):

    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        print(f"Could not open {video_path.name}")
        continue

    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    duration = frame_count / fps if fps > 0 else 0

    file_size_mb = video_path.stat().st_size / (1024 * 1024)

    rows.append({
        "video_id": video_path.stem,
        "filename": video_path.name,
        "duration_seconds": round(duration, 2),
        "fps": round(fps, 2),
        "frame_count": int(frame_count),
        "width": width,
        "height": height,
        "resolution": f"{width}x{height}",
        "file_size_mb": round(file_size_mb, 2)
    })

    cap.release()

df = pd.DataFrame(rows)

df.to_csv(OUTPUT_FILE, index=False)

print()
print("Metadata extraction complete.")
print(f"Videos processed : {len(df)}")
print(f"Saved to : {OUTPUT_FILE}")