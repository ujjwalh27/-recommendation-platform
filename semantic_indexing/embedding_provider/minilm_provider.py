"""
Task 1 – MiniLM Embedding Provider
SentenceTransformer 'all-MiniLM-L6-v2' implementation (384 dimensions).
"""

from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
from semantic_indexing.embedding_provider.base_provider import BaseEmbeddingProvider


class MiniLMEmbeddingProvider(BaseEmbeddingProvider):
    """SentenceTransformer all-MiniLM-L6-v2 provider."""

    def __init__(self, model_id: str = "all-MiniLM-L6-v2"):
        self._model_id = model_id
        self._model = None

    def initialize(self) -> None:
        if self._model is None:
            print(f"[CSIEI-Provider] Initializing MiniLM provider: {self._model_id}")
            self._model = SentenceTransformer(self._model_id)

    def encode(self, text: str) -> np.ndarray:
        self.initialize()
        vec = self._model.encode(text, convert_to_numpy=True).astype("float32")
        norm = np.linalg.norm(vec)
        return vec / norm if norm > 0 else vec

    def encode_batch(self, texts: List[str]) -> np.ndarray:
        self.initialize()
        vecs = self._model.encode(texts, convert_to_numpy=True, batch_size=32, show_progress_bar=False).astype("float32")
        norms = np.linalg.norm(vecs, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        return vecs / norms

    def model_name(self) -> str:
        return self._model_id

    def embedding_dimension(self) -> int:
        return 384
