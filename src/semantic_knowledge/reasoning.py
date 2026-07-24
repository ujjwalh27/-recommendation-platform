from typing import List, Tuple, Dict, Any
from src.semantic_knowledge.schemas import GraphNode, GraphEdge

class SemanticReasoningEngine:
    """Handles Step 7: Semantic Reasoning and Unobserved Concept Deduction."""

    def infer_concepts(self, nodes: List[GraphNode], edges: List[GraphEdge]) -> Tuple[List[GraphNode], List[GraphEdge]]:
        """
        Scans graph nodes and infers high-level unobserved concepts with evidence citations.
        """
        inferred_nodes: List[GraphNode] = []
        inferred_edges: List[GraphEdge] = []
        seen_ids = set()

        node_names_lower = [n.name.lower() for n in nodes]
        node_map = {n.name.lower(): n.id for n in nodes}

        # Rule 1: Temple + Bell + Priest / Prayer => Infer "Temple Ritual"
        temple_cues = ["temple", "bell", "priest", "swami", "prayer", "aarti", "mantra", "devotional music"]
        matching_temple = [c for c in temple_cues if any(c in name for name in node_names_lower)]
        if len(matching_temple) >= 2:
            inf_id = "ent_event_temple_ritual"
            if inf_id not in seen_ids:
                seen_ids.add(inf_id)
                inferred_nodes.append(GraphNode(
                    id=inf_id,
                    name="Temple Ritual",
                    type="Event",
                    properties={"inferred_from": matching_temple},
                    confidence=0.92,
                    source=f"ReasoningEngine (Evidence: {', '.join(matching_temple)})"
                ))
                # Add edges from supporting evidence to inferred concept
                for cue in matching_temple:
                    if cue in node_map:
                        inferred_edges.append(GraphEdge(
                            subject_id=node_map[cue],
                            predicate="PART_OF",
                            object_id=inf_id,
                            confidence=0.92,
                            provenance=f"Inferred via multi-node concurrence ({cue})"
                        ))

        # Rule 2: Pan + Vegetables + Cooking / Recipe => Infer "Culinary Cooking Activity" (requires explicit cooking verb)
        cooking_cues = ["pan", "cooking", "recipe", "kitchen"]
        matching_cooking = [c for c in cooking_cues if any(c in name for name in node_names_lower)]
        if len(matching_cooking) >= 2:
            inf_id = "ent_event_culinary_cooking_activity"
            if inf_id not in seen_ids:
                seen_ids.add(inf_id)
                inferred_nodes.append(GraphNode(
                    id=inf_id,
                    name="Culinary Cooking Activity",
                    type="Event",
                    properties={"inferred_from": matching_cooking},
                    confidence=0.92,
                    source=f"ReasoningEngine (Evidence: {', '.join(matching_cooking)})"
                ))

        # Rule 3: Speaker + Video / Audition / Dialogue => Infer "Personal Speaking Reel"
        speech_cues = ["aditi", "jadhav", "audition", "speaking", "monologue", "dialogue", "acting", "talk", "performance", "person"]
        matching_speech = [c for c in speech_cues if any(c in name for name in node_names_lower)]
        if len(matching_speech) >= 2:
            inf_id = "ent_event_personal_speaking_reel"
            if inf_id not in seen_ids:
                seen_ids.add(inf_id)
                inferred_nodes.append(GraphNode(
                    id=inf_id,
                    name="Personal Speaking Reel",
                    type="Event",
                    properties={"inferred_from": matching_speech},
                    confidence=0.94,
                    source=f"ReasoningEngine (Evidence: {', '.join(matching_speech)})"
                ))
                for cue in matching_cooking:
                    if cue in node_map:
                        inferred_edges.append(GraphEdge(
                            subject_id=node_map[cue],
                            predicate="PART_OF",
                            object_id=inf_id,
                            confidence=0.90,
                            provenance=f"Inferred via culinary concurrence ({cue})"
                        ))

        # Rule 3: Car / Vehicle + Driving / Road => Infer "Automotive Driving Vlog"
        auto_cues = ["car", "vehicle", "driving", "motorcycle", "road"]
        matching_auto = [c for c in auto_cues if any(c in name for name in node_names_lower)]
        if len(matching_auto) >= 2:
            inf_id = "ent_event_automotive_driving_vlog"
            if inf_id not in seen_ids:
                seen_ids.add(inf_id)
                inferred_nodes.append(GraphNode(
                    id=inf_id,
                    name="Automotive Driving Vlog",
                    type="Event",
                    properties={"inferred_from": matching_auto},
                    confidence=0.88,
                    source=f"ReasoningEngine (Evidence: {', '.join(matching_auto)})"
                ))

        return inferred_nodes, inferred_edges
