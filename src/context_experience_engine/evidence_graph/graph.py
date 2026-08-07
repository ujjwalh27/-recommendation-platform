from typing import Dict, Any, List


class EvidenceGraphBuilder:
    """
    Constructs a Directed Acyclic Graph (DAG) connecting raw perception nodes ->
    model nodes -> evidence nodes -> rule inference nodes -> enriched metadata fields.
    Available for debugging, visualization, and explainability.
    """

    def build_graph(
        self,
        evidence_doc: Dict[str, Any],
        perceptual_metadata: Dict[str, Any],
        emotional_metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Builds graph dictionary containing nodes and directed edges.
        """
        nodes = []
        edges = []

        # Root Video Node
        nodes.append({"id": "node_video_root", "type": "ROOT", "label": "Perception Observation Stream"})

        # Model Subsystem Nodes
        models = [
            ("node_model_minicpm", "MiniCPM-V", "vlm"),
            ("node_model_yolo", "YOLOv11", "visual"),
            ("node_model_videomae", "VideoMAE", "videomae"),
            ("node_model_whisper", "Whisper", "whisper"),
            ("node_model_ast", "AST", "audio"),
            ("node_model_ocr", "EasyOCR", "text"),
            ("node_model_clip", "CLIP", "clip"),
        ]

        for m_id, m_name, doc_key in models:
            nodes.append({"id": m_id, "type": "MODEL", "label": m_name, "data": evidence_doc.get(doc_key, {})})
            edges.append({"source": "node_video_root", "target": m_id, "relation": "EXTRACTED_BY"})

        # Perceptual Field Nodes & Edges
        for field, data in perceptual_metadata.items():
            field_node_id = f"node_field_perc_{field}"
            nodes.append({
                "id": field_node_id,
                "type": "PERCEPTUAL_FIELD",
                "label": f"{field}: {data.get('value')}",
                "confidence": data.get("confidence"),
                "rules": data.get("rules", [])
            })

            # Link evidence items to model nodes
            for ev in data.get("evidence", []):
                src = ev.get("source", "MiniCPM") if isinstance(ev, dict) else "MiniCPM"
                m_target_id = f"node_model_{src.lower()}"
                edges.append({
                    "source": m_target_id,
                    "target": field_node_id,
                    "relation": "SUPPORTS_INFERENCE",
                    "evidence_value": ev.get("value") if isinstance(ev, dict) else str(ev)
                })

        # Emotional Field Nodes & Edges
        for field, data in emotional_metadata.items():
            field_node_id = f"node_field_emo_{field}"
            nodes.append({
                "id": field_node_id,
                "type": "EMOTIONAL_FIELD",
                "label": f"{field}: {data.get('value')}",
                "confidence": data.get("confidence"),
                "rules": data.get("rules", [])
            })

            for ev in data.get("evidence", []):
                src = ev.get("source", "MiniCPM") if isinstance(ev, dict) else "MiniCPM"
                m_target_id = f"node_model_{src.lower()}"
                edges.append({
                    "source": m_target_id,
                    "target": field_node_id,
                    "relation": "SUPPORTS_INFERENCE",
                    "evidence_value": ev.get("value") if isinstance(ev, dict) else str(ev)
                })

        return {
            "graph_metadata": {
                "total_nodes": len(nodes),
                "total_edges": len(edges),
                "structure": "DIRECTED_ACYCLIC_GRAPH"
            },
            "nodes": nodes,
            "edges": edges
        }
