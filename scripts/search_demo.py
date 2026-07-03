import numpy as np

from backend.recommendation.vector_search import VectorSearch

video_ids = np.load(
    "datasets/embeddings/video_ids.npy",
    allow_pickle=True
)

embeddings = np.load(
    "datasets/embeddings/video_embeddings.npy"
)

search = VectorSearch()

query_embedding = embeddings[0]

results = search.search(
    query_embedding,
    k=10
)

print()

print("Query Video")

print(video_ids[0])

print()

print("Most Similar")

for r in results:

    print(r)