import os
import numpy as np
from PIL import Image
from tqdm import tqdm

from src.embeddings.clip_model import ClipModel


KEYFRAME_DIR = "datasets/keyframes"
OUTPUT_DIR = "datasets/embeddings"

os.makedirs(OUTPUT_DIR, exist_ok=True)


clip = ClipModel()

video_ids = []
embeddings = []


video_folders = sorted(os.listdir(KEYFRAME_DIR))

print(f"Found {len(video_folders)} videos")


for video_id in tqdm(video_folders):

    folder = os.path.join(KEYFRAME_DIR, video_id)

    frame_vectors = []

    for frame_name in sorted(os.listdir(folder)):

        image_path = os.path.join(folder, frame_name)

        image = Image.open(image_path).convert("RGB")

        vector = clip.encode_image(image)

        frame_vectors.append(vector)

    frame_vectors = np.stack(frame_vectors)

    video_embedding = frame_vectors.mean(axis=0)

    video_ids.append(video_id)

    embeddings.append(video_embedding)


video_ids = np.array(video_ids)
embeddings = np.array(embeddings)

np.save(
    os.path.join(OUTPUT_DIR, "video_ids.npy"),
    video_ids
)

np.save(
    os.path.join(OUTPUT_DIR, "video_embeddings.npy"),
    embeddings
)

print()

print("Embedding generation completed.")

print("Videos:", len(video_ids))

print("Embedding shape:", embeddings.shape)