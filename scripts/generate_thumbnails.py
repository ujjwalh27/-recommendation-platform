from pathlib import Path
import cv2
from tqdm import tqdm

VIDEO_DIR = Path("datasets/raw/videos")
THUMBNAIL_DIR = Path("datasets/thumbnails")

THUMBNAIL_DIR.mkdir(parents=True, exist_ok=True)

video_files = sorted(VIDEO_DIR.glob("*.mp4"))

print(f"Found {len(video_files)} videos")

generated = 0
failed = 0

for video_path in tqdm(video_files):

    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        failed += 1
        continue

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if frame_count == 0:
        failed += 1
        cap.release()
        continue

    middle_frame = frame_count // 2

    cap.set(cv2.CAP_PROP_POS_FRAMES, middle_frame)

    success, frame = cap.read()

    if success:
        thumbnail_path = THUMBNAIL_DIR / f"{video_path.stem}.jpg"
        cv2.imwrite(str(thumbnail_path), frame)
        generated += 1
    else:
        failed += 1

    cap.release()

print()
print("Thumbnail generation complete.")
print(f"Generated : {generated}")
print(f"Failed    : {failed}")