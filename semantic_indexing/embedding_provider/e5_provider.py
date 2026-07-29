"""
Task 1 – Multilingual E5 Embedding Provider
intfloat/multilingual-e5-small provider (384 dimensions).
"""

from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
from semantic_indexing.embedding_provider.base_provider import BaseEmbeddingProvider


class MultilingualE5Provider(BaseEmbeddingProvider):
    """Multilingual E5 Small provider."""

    def __init__(self, model_id: str = "intfloat/multilingual-e5-small"):
        self._model_id = model_id
        self._model = None

    def initialize(self) -> None:
        if self._model is None:
            print(f"[CSIEI-Provider] Initializing Multilingual-E5 provider: {self._model_id}")
            self._model = SentenceTransformer(self._model_id)

    def encode(self, text: str) -> np.ndarray:
        self.initialize()
        formatted_text = f"passage: {text}"
        vec = self._model.encode(formatted_text, convert_to_numpy=True).astype("float32")
        norm = np.linalg.norm(vec)
        return vec / norm if norm > 0 else vec

    def encode_batch(self, texts: List[str]) -> np.ndarray:
        self.initialize()
        formatted_texts = [f"passage: {t}" for t in texts]
        vecs = self._model.encode(formatted_texts, convert_to_numpy=True, batch_size=32, show_progress_bar=False).astype("float32")
        norms = np.linalg.norm(vecs, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        return vecs / norms

    def model_name(self) -> str:
        return self._model_id

    def embedding_dimension(self) -> int:
        return 384
