import numpy as np

from src.search.faiss_index import FaissIndex


embeddings = np.load(
    "datasets/embeddings/video_embeddings.npy"
).astype("float32")

video_ids = np.load(
    "datasets/embeddings/video_ids.npy"
)

print("Embeddings:", embeddings.shape)

index = FaissIndex()

index.build(
    embeddings,
    video_ids
)

index.save("models")

print()
print("FAISS Index Created Successfully")