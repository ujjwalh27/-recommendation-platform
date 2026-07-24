from typing import List, Dict, Any
from src.semantic_knowledge.schemas import GraphNode, GraphEdge, SceneSegment

class RelationshipBuilder:
    """Handles Step 3: Relationship Extraction & Step 4: Temporal Knowledge Sequencing."""

    def build_relationships(
        self,
        nodes: List[GraphNode],
        scenes: List[SceneSegment],
        vlm_data: Dict[str, Any]
    ) -> List[GraphEdge]:
        """
        Constructs explicit directional relationship edges between entity nodes and scene nodes,
        preserving temporal event chronology.
        """
        edges: List[GraphEdge] = []
        node_map = {n.id: n for n in nodes}

        # Helper to safely add edges
        seen_edges = set()
        def add_edge(subj_id: str, predicate: str, obj_id: str, conf: float = 0.85, timestamp: float = None, prov: str = "Inferred"):
            if subj_id in node_map and obj_id in node_map and subj_id != obj_id:
                edge_key = (subj_id, predicate, obj_id)
                if edge_key not in seen_edges:
                    seen_edges.add(edge_key)
                    edges.append(GraphEdge(
                        subject_id=subj_id,
                        predicate=predicate,
                        object_id=obj_id,
                        confidence=conf,
                        timestamp=timestamp,
                        provenance=prov
                    ))

        # 1. Step 4: Temporal Scene Chronology Edges
        for i in range(len(scenes) - 1):
            s_curr = scenes[i].scene_id
            s_next = scenes[i+1].scene_id
            add_edge(s_curr, "TRANSITIONS_TO", s_next, conf=1.0, timestamp=scenes[i].timestamp_start, prov="Chronology")

        # 2. Map Entities to Scenes (CONTAINS / LOCATED_AT / PERFORMS)
        people_nodes = [n for n in nodes if n.type == "Person"]
        location_nodes = [n for n in nodes if n.type in ["Location", "Building"]]
        object_nodes = [n for n in nodes if n.type in ["Object", "Vehicle", "ReligiousSymbol", "Food"]]
        music_nodes = [n for n in nodes if n.type == "Music"]

        category = vlm_data.get("category", "").lower()
        activities = vlm_data.get("activities", [])

        # Link Entities to Scenes
        for sc in scenes:
            s_id = sc.scene_id
            
            # Scene CONTAINS Objects
            for obj in object_nodes:
                if any(obj.name.lower() in o.lower() for o in sc.objects):
                    add_edge(s_id, "CONTAINS", obj.id, conf=0.90, timestamp=sc.timestamp_start, prov="YOLO/CLIP")

            # Scene LOCATED_AT Buildings
            for loc in location_nodes:
                add_edge(s_id, "LOCATED_AT", loc.id, conf=0.85, timestamp=sc.timestamp_start, prov="CLIP/VLM")

        # 3. Step 3: Domain-Specific Entity-to-Entity Relationships
        for p in people_nodes:
            # Person PERFORMS Action / Prayer
            for act in activities:
                act_node_id = f"ent_concept_{act.lower().replace(' ', '_')}"
                if act_node_id in node_map:
                    add_edge(p.id, "PERFORMS", act_node_id, conf=0.88, prov="Multimodal Reasoning")

            # Person PREPARES Food
            if "food" in category or "cooking" in category:
                food_nodes = [n for n in nodes if n.type == "Food"]
                for f in food_nodes:
                    add_edge(p.id, "PREPARES", f.id, conf=0.90, prov="Food Domain Reasoning")

            # Person LISTEN_TO / PERFORMS Music
            for m in music_nodes:
                predicate = "PERFORMS" if "singer" in p.name.lower() or "artist" in p.name.lower() else "LISTEN_TO"
                add_edge(p.id, predicate, m.id, conf=0.85, prov="Music Domain Reasoning")

            # Person LOCATED_AT Location
            for loc in location_nodes:
                add_edge(p.id, "LOCATED_AT", loc.id, conf=0.80, prov="Spatial Inference")

        # 4. Object USES & CONTAINS relationships
        for loc in location_nodes:
            for obj in object_nodes:
                add_edge(loc.id, "CONTAINS", obj.id, conf=0.75, prov="Spatial Inclusion")

        return edges
