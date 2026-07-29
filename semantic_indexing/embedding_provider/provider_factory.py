"""
Task 1 – Embedding Provider Factory
Configurable factory for selecting and instantiating embedding provider instances.
"""

from typing import Dict, Any, Type, List
from semantic_indexing.embedding_provider.base_provider import BaseEmbeddingProvider
from semantic_indexing.embedding_provider.minilm_provider import MiniLMEmbeddingProvider
from semantic_indexing.embedding_provider.bge_provider import BGEEmbeddingProvider
from semantic_indexing.embedding_provider.e5_provider import MultilingualE5Provider


class EmbeddingProviderFactory:
    """Factory registry for creating modular embedding providers."""

    _PROVIDERS: Dict[str, Type[BaseEmbeddingProvider]] = {
        "minilm": MiniLMEmbeddingProvider,
        "all-minilm-l6-v2": MiniLMEmbeddingProvider,
        "bge-small": BGEEmbeddingProvider,
        "bge": BGEEmbeddingProvider,
        "e5-small": MultilingualE5Provider,
        "e5": MultilingualE5Provider
    }

    @classmethod
    def get_provider(cls, provider_key: str = "minilm") -> BaseEmbeddingProvider:
        """Returns an uninitialized instance of the requested embedding provider."""
        key = provider_key.lower().strip()
        if key not in cls._PROVIDERS:
            print(f"[CSIEI-Factory] Provider '{provider_key}' not found. Defaulting to 'minilm'.")
            key = "minilm"

        provider_cls = cls._PROVIDERS[key]
        return provider_cls()

    @classmethod
    def list_available_providers(cls) -> List[str]:
        return sorted(list(set(cls._PROVIDERS.keys())))
