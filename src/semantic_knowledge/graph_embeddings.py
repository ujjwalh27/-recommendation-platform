import networkx as nx
from typing import List, Tuple, Dict, Any
from sentence_transformers import SentenceTransformer

class GraphEmbeddingBuilder:
    """Handles Step 11: Graph Embeddings for MiniLM Vector Indexing."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._embedding_model = None

    @property
    def embedding_model(self) -> SentenceTransformer:
        if not self._embedding_model:
            print(f"[GraphEmbeddings] Loading SentenceTransformer '{self.model_name}'...")
            self._embedding_model = SentenceTransformer(self.model_name)
        return self._embedding_model

    def build_embedding_text(self, G: nx.DiGraph) -> str:
        """
        Extracts canonical graph node labels, ontology classes, and relationship triples
        to form the canonical graph embedding text block.
        """
        parts = []

        # 1. Canonical Node Names & Entity Types
        for n, attrs in G.nodes(data=True):
            n_type = attrs.get("type", "")
            n_name = attrs.get("name", "")
            if n_type != "Scene" and n_name:
                parts.append(f"{n_type}: {n_name}")

        # 2. Relationship Triples (Subject Predicate Object)
        for u, v, attrs in G.edges(data=True):
            subj_name = G.nodes[u].get("name", u)
            pred = attrs.get("relationship", "RELATED_TO")
            obj_name = G.nodes[v].get("name", v)
            if G.nodes[u].get("type") != "Scene" and G.nodes[v].get("type") != "Scene":
                parts.append(f"{subj_name} {pred} {obj_name}")

        embedding_text = " . ".join(parts)
        if not embedding_text.strip():
            embedding_text = f"Semantic Knowledge Graph with {G.number_of_nodes()} nodes"

        return embedding_text

    def generate_vector(self, G: nx.DiGraph) -> Tuple[str, List[float]]:
        """
        Generates canonical embedding text and encodes it into a 384-dimensional vector.
        """
        emb_text = self.build_embedding_text(G)
        vector = self.embedding_model.encode(emb_text, normalize_embeddings=True)
        return emb_text, vector.tolist()
