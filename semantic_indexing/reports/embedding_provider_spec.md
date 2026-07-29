# CSIEI Task 1: Embedding Provider Abstraction Specification

## Overview

The **Embedding Provider Abstraction Layer** introduces a modular, plugin-based architecture for vector embedding generation. The system is completely decoupled from any single model dependency, allowing dynamic selection and evaluation of different SentenceTransformers, BGE, and Multilingual-E5 models.

---

## Architecture Contract (`BaseEmbeddingProvider`)

```python
class BaseEmbeddingProvider(ABC):
    @abstractmethod
    def initialize(self) -> None: ...
    @abstractmethod
    def encode(self, text: str) -> np.ndarray: ...
    @abstractmethod
    def encode_batch(self, texts: List[str]) -> np.ndarray: ...
    @abstractmethod
    def model_name(self) -> str: ...
    @abstractmethod
    def embedding_dimension(self) -> int: ...
```

---

## Provider Registry Matrix

| Provider Key | Provider Class | Model Identifier | Output Dimension | Primary Use Case |
|:---|:---|:---|:---:|:---|
| `minilm` | `MiniLMEmbeddingProvider` | `all-MiniLM-L6-v2` | **384** | Primary production model (High speed, CPU efficient, low latency ~15ms) |
| `bge-small` | `BGEEmbeddingProvider` | `BAAI/bge-small-en-v1.5` | **384** | High-precision retrieval for domain-specific English search queries |
| `e5-small` | `MultilingualE5Provider` | `intfloat/multilingual-e5-small` | **384** | Multilingual devotional search (Hindi, Sanskrit, Tamil, Telugu, Marathi) |

---

## Configuration & Provider Factory

To select an active provider dynamically:

```python
from semantic_indexing.embedding_provider.provider_factory import EmbeddingProviderFactory

# Instantiate active provider
provider = EmbeddingProviderFactory.get_provider("minilm")
provider.initialize()

vector = provider.encode("Category: Temple Ritual | Ritual: Jalabhishekam | Deity: Lord Shiva")
```
