"""
Task 3 – Canonical Embedding Generator
Consumes CMREE canonical semantic documents and generates dense L2-normalized vector embeddings.
"""

from typing import Dict, Any, List
import numpy as np
from semantic_indexing.embedding_provider.base_provider import BaseEmbeddingProvider
from semantic_indexing.embedding_provider.provider_factory import EmbeddingProviderFactory
from semantic_indexing.semantic_document.builder import CanonicalSemanticDocumentBuilder


class CanonicalEmbeddingGenerator:
    """Generates canonical semantic vector embeddings using configurable embedding providers."""

    def __init__(self, provider: BaseEmbeddingProvider = None):
        self.provider = provider or EmbeddingProviderFactory.get_provider("minilm")
        self.doc_builder = CanonicalSemanticDocumentBuilder()

    def generate_single_embedding(self, canonical_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Generates embedding for a single canonical metadata dict."""
        text = self.doc_builder.build_dense_embedding_text(canonical_metadata)
        vector = self.provider.encode(text)

        return {
            "embedding": vector,
            "embedding_text": text,
            "model_name": self.provider.model_name(),
            "dimension": self.provider.embedding_dimension()
        }

    def generate_batch_embeddings(self, canonical_metadata_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generates embeddings for a batch of canonical metadata dicts."""
        texts = [self.doc_builder.build_dense_embedding_text(m) for m in canonical_metadata_list]
        vectors = self.provider.encode_batch(texts)

        return {
            "embeddings": vectors,
            "embedding_texts": texts,
            "model_name": self.provider.model_name(),
            "dimension": self.provider.embedding_dimension()
        }
