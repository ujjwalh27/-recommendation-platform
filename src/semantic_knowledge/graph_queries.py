import networkx as nx
from typing import List, Dict, Any
from src.semantic_knowledge.schemas import GraphNode, GraphEdge, GraphQueryResult

class GraphQueryEngine:
    """Handles Step 9: Graph Querying & Traversals."""

    def find_nodes_by_type(self, G: nx.DiGraph, target_type: str) -> GraphQueryResult:
        """Finds all graph nodes matching a specific entity type (e.g. Person, Location, Food)."""
        nodes = []
        for n, attrs in G.nodes(data=True):
            if attrs.get("type", "").lower() == target_type.lower():
                nodes.append(GraphNode(
                    id=n,
                    name=attrs.get("name", n),
                    type=attrs.get("type"),
                    properties=attrs.get("properties", {}),
                    confidence=attrs.get("confidence", 1.0),
                    source=attrs.get("source", "Engine"),
                    timestamp=attrs.get("timestamp")
                ))
        return GraphQueryResult(query_type=f"find_nodes_by_type_{target_type}", count=len(nodes), nodes=nodes)

    def find_objects_after_timestamp(self, G: nx.DiGraph, timestamp_s: float) -> GraphQueryResult:
        """Finds all physical objects appearing after a given timestamp threshold."""
        nodes = []
        for n, attrs in G.nodes(data=True):
            if attrs.get("type") in ["Object", "Vehicle", "ReligiousSymbol", "Food"]:
                ts = attrs.get("timestamp")
                if ts is not None and ts >= timestamp_s:
                    nodes.append(GraphNode(
                        id=n,
                        name=attrs.get("name", n),
                        type=attrs.get("type"),
                        properties=attrs.get("properties", {}),
                        confidence=attrs.get("confidence", 1.0),
                        source=attrs.get("source"),
                        timestamp=ts
                    ))
        return GraphQueryResult(query_type="find_objects_after_timestamp", count=len(nodes), nodes=nodes)

    def find_people_to_place_relationships(self, G: nx.DiGraph) -> GraphQueryResult:
        """Finds all relationship edges connecting People to Locations or Buildings."""
        matching_edges = []
        for u, v, attrs in G.edges(data=True):
            u_type = G.nodes[u].get("type", "")
            v_type = G.nodes[v].get("type", "")
            if u_type == "Person" and v_type in ["Location", "Building"]:
                matching_edges.append(GraphEdge(
                    subject_id=u,
                    predicate=attrs.get("relationship", "LOCATED_AT"),
                    object_id=v,
                    confidence=attrs.get("confidence", 1.0),
                    timestamp=attrs.get("timestamp"),
                    provenance=attrs.get("provenance", "")
                ))
        return GraphQueryResult(query_type="people_to_place_relationships", count=len(matching_edges), edges=matching_edges)

    def find_temporal_sequence(self, G: nx.DiGraph) -> GraphQueryResult:
        """Traverses the TRANSITIONS_TO edge sequence to reconstruct chronological scene ordering."""
        scene_nodes = [n for n, attrs in G.nodes(data=True) if attrs.get("type") == "Scene"]
        scene_nodes.sort(key=lambda n: G.nodes[n].get("timestamp", 0.0))
        
        sequence_names = [G.nodes[n].get("name", n) for n in scene_nodes]
        return GraphQueryResult(query_type="temporal_sequence", count=len(sequence_names), sequence=sequence_names)
