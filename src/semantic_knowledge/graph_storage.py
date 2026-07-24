import os
import json
import networkx as nx
from typing import List, Dict, Any, Tuple
from src.semantic_knowledge.schemas import GraphNode, GraphEdge, SceneSegment, KnowledgeGraphData
from src.semantic_knowledge.config import GRAPH_STORAGE_DIR

class NetworkXGraphStorage:
    """Handles Step 8: NetworkX Semantic Knowledge Graph Storage & Serializers."""

    def __init__(self, storage_dir: str = None):
        self.storage_dir = storage_dir or GRAPH_STORAGE_DIR
        os.makedirs(self.storage_dir, exist_ok=True)

    def create_graph(
        self,
        video_id: str,
        duration: float,
        nodes: List[GraphNode],
        edges: List[GraphEdge],
        scenes: List[SceneSegment]
    ) -> Tuple[nx.DiGraph, str]:
        """
        Populates a NetworkX DiGraph instance with nodes and edges and saves it to disk.
        
        Returns:
            Tuple of (nx.DiGraph instance, output_file_path)
        """
        G = nx.DiGraph(video_id=video_id, duration=duration)

        # 1. Add Scene & Entity Nodes with full property attributes
        for n in nodes:
            G.add_node(
                n.id,
                name=n.name,
                type=n.type,
                properties=n.properties,
                confidence=n.confidence,
                source=n.source,
                timestamp=n.timestamp
            )

        # 2. Add Directional Edges with full metadata
        for e in edges:
            G.add_edge(
                e.subject_id,
                e.object_id,
                relationship=e.predicate,
                confidence=e.confidence,
                timestamp=e.timestamp,
                provenance=e.provenance
            )

        # 3. Serialize Graph to JSON
        output_file = os.path.join(self.storage_dir, f"{video_id}_graph.json")
        graph_json_data = self.to_json(G, video_id, duration, scenes)
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(graph_json_data, f, indent=2, ensure_ascii=False)

        print(f"[GraphStorage] Built NetworkX Knowledge Graph ({G.number_of_nodes()} nodes, {G.number_of_edges()} edges) saved to: {output_file}")
        return G, output_file

    def to_json(self, G: nx.DiGraph, video_id: str, duration: float, scenes: List[SceneSegment]) -> Dict[str, Any]:
        """Converts NetworkX graph to standardized JSON dictionary representation."""
        nodes_list = []
        for n, attrs in G.nodes(data=True):
            nodes_list.append({
                "id": n,
                "name": attrs.get("name", n),
                "type": attrs.get("type", "Concept"),
                "properties": attrs.get("properties", {}),
                "confidence": attrs.get("confidence", 1.0),
                "source": attrs.get("source", "Engine"),
                "timestamp": attrs.get("timestamp")
            })

        edges_list = []
        for u, v, attrs in G.edges(data=True):
            edges_list.append({
                "subject_id": u,
                "predicate": attrs.get("relationship", "RELATED_TO"),
                "object_id": v,
                "confidence": attrs.get("confidence", 1.0),
                "timestamp": attrs.get("timestamp"),
                "provenance": attrs.get("provenance", "Inferred")
            })

        return {
            "video_id": video_id,
            "duration": duration,
            "summary_stats": {
                "node_count": G.number_of_nodes(),
                "edge_count": G.number_of_edges(),
                "scene_count": len(scenes)
            },
            "nodes": nodes_list,
            "edges": edges_list,
            "scenes": [s.dict() for s in scenes]
        }

    def to_rdf_triples(self, G: nx.DiGraph) -> List[Tuple[str, str, str]]:
        """Exports graph to W3C-style RDF Triples (Subject, Predicate, Object)."""
        triples = []
        for u, v, attrs in G.edges(data=True):
            subj_name = G.nodes[u].get("name", u)
            pred = attrs.get("relationship", "RELATED_TO")
            obj_name = G.nodes[v].get("name", v)
            triples.append((subj_name, pred, obj_name))
        return triples
