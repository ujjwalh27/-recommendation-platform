from typing import List, Tuple, Dict, Any
from src.semantic_knowledge.schemas import GraphNode, GraphEdge

class DomainOntology:
    """Handles Step 6: Lightweight Domain Taxonomy and Concept Normalization (IS_A hierarchy)."""

    # Static Taxonomy Knowledge Base
    TAXONOMY_RULES = {
        # Devotion Objects & Shrine Taxonomy
        "oil lamp": ("Oil Lamp / Deepa", "Object"),
        "deepa": ("Oil Lamp / Deepa", "Object"),
        "diya": ("Oil Lamp / Deepa", "Object"),
        "idol": ("Sacred Idol", "Object"),
        "temple": ("Religious Temple", "Location"),
        "shrine": ("Home Prayer Shrine", "Location"),
        "prayer room": ("Home Prayer Room", "Location"),
        "flowers": ("Devotional Offering", "Object"),
        "incense": ("Incense Stick / Dhoop", "Object"),
        "bell": ("Temple Bell", "Object"),
        "aarti plate": ("Aarti Offering Plate", "Object"),
        "prasadam": ("Sacred Food Offering", "Food"),

        # Devotion Activities Taxonomy
        "lighting deepa": ("Lighting Deepa / Lamp", "Event"),
        "performing puja": ("Devotional Worship", "Event"),
        "puja": ("Devotional Worship", "Event"),
        "aarti": ("Offering Aarti", "Event"),
        "offering aarti": ("Offering Aarti", "Event"),
        "chanting": ("Chanting Mantras", "Event"),
        "meditation": ("Spiritual Meditation", "Event"),
        "offering flowers": ("Offering Flowers", "Event"),
        "prayer": ("Devotional Prayer", "Event"),

        # Devotion Concepts & Personalities
        "sai baba": ("Sri Sai Baba", "Person"),
        "sai": ("Sri Sai Baba", "Person"),
        "samartha": ("Sri Sai Samartha Mantra", "ReligiousSymbol"),
        "mantra": ("Sacred Chant", "ReligiousSymbol"),
        "bhajan": ("Devotional Music", "Music"),
        "priest": ("Religious Leader", "Person"),
        "swami": ("Spiritual Master", "Person"),
        "satsang": ("Spiritual Gathering", "Event"),
        "hindu ritual": ("Hindu Devotional Ritual", "Concept"),
        "devotional worship": ("Devotional Worship", "Concept"),
        "spiritual practice": ("Spiritual Practice", "Concept"),

        # Food Taxonomy
        "cake": ("Baked Food", "Food"),
        "recipe": ("Culinary Instruction", "Concept"),
        "cooking": ("Food Preparation", "Event"),
        "kitchen": ("Culinary Space", "Location"),

        # Music & Entertainment
        "singing": ("Vocal Performance", "Event"),
        "dance": ("Physical Performance", "Event"),
        "song": ("Musical Composition", "Music"),

        # Automobiles
        "car": ("Motor Vehicle", "Vehicle"),
        "motorcycle": ("Two-Wheeled Vehicle", "Vehicle"),
        "driving": ("Vehicle Operation", "Event")
    }

    def apply_ontology(self, nodes: List[GraphNode]) -> Tuple[List[GraphNode], List[GraphEdge]]:
        """
        Normalizes nodes against the taxonomy, returning new parent concept nodes and IS_A edges.
        """
        parent_nodes: List[GraphNode] = []
        is_a_edges: List[GraphEdge] = []
        seen_parents = set()

        for node in nodes:
            name_lower = node.name.lower()
            for key, (parent_name, parent_type) in self.TAXONOMY_RULES.items():
                if key in name_lower:
                    parent_id = f"ent_{parent_type.lower()}_{parent_name.lower().replace(' ', '_').replace('/', '_')}"
                    
                    if parent_id not in seen_parents:
                        seen_parents.add(parent_id)
                        parent_nodes.append(GraphNode(
                            id=parent_id,
                            name=parent_name,
                            type=parent_type,
                            properties={"is_canonical": True},
                            confidence=0.95,
                            source="DomainOntology"
                        ))

                    # Create IS_A edge: Node IS_A Parent
                    is_a_edges.append(GraphEdge(
                        subject_id=node.id,
                        predicate="IS_A",
                        object_id=parent_id,
                        confidence=0.95,
                        provenance="Ontology Taxonomy"
                    ))

        return parent_nodes, is_a_edges
