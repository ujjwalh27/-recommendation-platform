from pathlib import Path
import cv2
from tqdm import tqdm

VIDEO_DIR = Path("datasets/raw/videos")
OUTPUT_DIR = Path("datasets/keyframes")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

video_files = sorted(VIDEO_DIR.glob("*.mp4"))

positions = [0.25, 0.50, 0.75]

generated = 0
failed = 0

print(f"Found {len(video_files)} videos")

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

    video_folder = OUTPUT_DIR / video_path.stem
    video_folder.mkdir(exist_ok=True)

    for i, pos in enumerate(positions, start=1):

        frame_no = int(frame_count * pos)

        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)

        success, frame = cap.read()

        if success:
            cv2.imwrite(
                str(video_folder / f"frame_{i}.jpg"),
                frame
            )
            generated += 1

    cap.release()

print()
print("Keyframe extraction complete.")
print(f"Frames generated : {generated}")
print(f"Videos failed    : {failed}")