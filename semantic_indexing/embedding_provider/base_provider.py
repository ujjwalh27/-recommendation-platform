"""
Task 1 – Base Embedding Provider Interface
Defines the standard abstract contract for all embedding models.
"""

from abc import ABC, abstractmethod
from typing import List
import numpy as np


class BaseEmbeddingProvider(ABC):
    """Abstract base class for modular embedding providers."""

    @abstractmethod
    def initialize(self) -> None:
        """Initializes the underlying embedding model weights."""
        pass

    @abstractmethod
    def encode(self, text: str) -> np.ndarray:
        """Encodes a single text string into a 1D L2-normalized numpy array float32 vector."""
        pass

    @abstractmethod
    def encode_batch(self, texts: List[str]) -> np.ndarray:
        """Encodes a list of text strings into a 2D float32 numpy array (N, dim)."""
        pass

    @abstractmethod
    def model_name(self) -> str:
        """Returns the unique name identifier of the model."""
        pass

    @abstractmethod
    def embedding_dimension(self) -> int:
        """Returns the vector output dimension (e.g. 384, 768, 1024)."""
        pass
