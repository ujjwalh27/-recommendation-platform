import re
from typing import List, Dict, Any
from src.semantic_knowledge.schemas import GraphNode, SceneSegment
from src.semantic_knowledge.config import ENTITY_TYPES

class MultimodalEntityExtractor:
    """Handles Step 2: Multimodal Entity Extraction across 14 categories."""

    def extract_entities(self, scenes: List[SceneSegment], vlm_data: Dict[str, Any], evidence: Any) -> List[GraphNode]:
        """
        Extracts entities across 14 distinct categories and wraps them as GraphNode objects.
        """
        entity_nodes: List[GraphNode] = []
        seen_ids = set()

        def add_entity(name: str, ent_type: str, source: str, conf: float = 0.85, properties: Dict[str, Any] = None):
            if not name or not name.strip():
                return
            clean_name = name.strip()
            node_id = f"ent_{ent_type.lower()}_{clean_name.lower().replace(' ', '_')}"
            
            if node_id not in seen_ids and ent_type in ENTITY_TYPES:
                seen_ids.add(node_id)
                entity_nodes.append(GraphNode(
                    id=node_id,
                    name=clean_name,
                    type=ent_type,
                    properties=properties or {},
                    confidence=conf,
                    source=source
                ))

        # 1. Extract People & Organizations from VLM & transcripts
        for p in vlm_data.get("people", []):
            add_entity(p, "Person", "VLM")
        for ent in vlm_data.get("entities", []):
            if any(w in ent.lower() for w in ["swami", "priest", "chef", "devotee", "singer", "artist", "actor", "person"]):
                add_entity(ent, "Person", "VLM")
            elif any(w in ent.lower() for w in ["inc", "org", "foundation", "trust", "temple board", "channel"]):
                add_entity(ent, "Organization", "VLM")
            else:
                add_entity(ent, "Concept", "VLM")

        # 2. Extract Locations & Buildings
        for loc in vlm_data.get("locations", []):
            if any(w in loc.lower() for w in ["temple", "church", "mosque", "house", "building", "kitchen", "stadium"]):
                add_entity(loc, "Building", "VLM/CLIP")
            else:
                add_entity(loc, "Location", "VLM/CLIP")

        # 3. Extract Objects & Vehicles from YOLO
        yolo_labels = [n.value for n in getattr(evidence, "vision", []) if getattr(n, "source", "") == "YOLO"]
        for label in yolo_labels:
            if label.lower() in ["car", "motorcycle", "bus", "truck", "train", "bicycle", "vehicle"]:
                add_entity(label, "Vehicle", "YOLO", conf=0.90)
            elif label.lower() in ["cat", "dog", "bird", "horse", "cow", "elephant", "animal"]:
                add_entity(label, "Animal", "YOLO", conf=0.90)
            else:
                add_entity(label, "Object", "YOLO", conf=0.85)

        for obj in vlm_data.get("objects", []):
            if obj.lower() not in [y.lower() for y in yolo_labels]:
                add_entity(obj, "Object", "VLM", conf=0.75)

        # 4. Extract Food & Music
        category = vlm_data.get("category", "").lower()
        subcategory = vlm_data.get("subcategory", "").lower()

        if "food" in category or "recipe" in subcategory:
            for item in vlm_data.get("keywords", []):
                if any(w in item.lower() for w in ["dish", "recipe", "food", "cake", "onion", "paneer", "rice", "sweet"]):
                    add_entity(item, "Food", "VLM/Speech", conf=0.85)

        if "music" in category or "singing" in subcategory or "bhajan" in subcategory:
            for item in vlm_data.get("keywords", []):
                if any(w in item.lower() for w in ["song", "music", "bhajan", "chant", "singing", "melody", "mantra"]):
                    add_entity(item, "Music", "AST/Speech", conf=0.90)

        # 5. Extract Religious Symbols
        for item in vlm_data.get("keywords", []) + vlm_data.get("secondary_topics", []):
            if any(w in item.lower() for w in ["aarti", "puja", "om", "mantra", "tilak", "diya", "idol", "deity"]):
                add_entity(item, "ReligiousSymbol", "VLM/OCR", conf=0.92)

        # 6. Extract Events
        for ev in vlm_data.get("events", []):
            add_entity(ev, "Event", "VLM", conf=0.85)
        if subcategory:
            add_entity(subcategory, "Event", "VLM", conf=0.80)

        # 7. Extract Concepts & Topics
        primary_topic = vlm_data.get("primary_topic", "")
        if primary_topic:
            add_entity(primary_topic, "Concept", "VLM", conf=0.90)
            
        for topic in vlm_data.get("secondary_topics", []):
            add_entity(topic, "Concept", "VLM", conf=0.80)

        return entity_nodes
