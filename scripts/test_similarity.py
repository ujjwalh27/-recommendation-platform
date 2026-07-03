from src.search.similarity_search import SimilaritySearch

engine = SimilaritySearch()

scores, ids = engine.search(
    video_index=0,
    top_k=10
)

print()

print("Most Similar Videos")

print("-------------------")

for rank, (score, video_id) in enumerate(zip(scores, ids), start=1):

    print(
        f"{rank}. {video_id}   Score: {score:.4f}"
    )