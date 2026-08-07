from typing import Dict, List, Any

# Dynamic spiritual and domain persona configuration definitions (Canonical Taxonomy)
PERSONAS: Dict[str, Dict[str, Any]] = {
    "Devotional Practitioner": {
        "preferred_categories": ["Aarti", "Pooja", "Abhishekam"],
        "description": "Engaged in daily shrine worship, lamp lighting, and temple rituals."
    },
    "Temple Pilgrim": {
        "preferred_categories": ["Abhishekam", "Temple Darshan", "Pooja"],
        "description": "Fascinated by sacred fluid pourings, lingam abhishekam, and temple visits."
    },
    "Bhajan & Chant Seeker": {
        "preferred_categories": ["Bhajan", "Kirtan / Nama Sankeerthana", "Meditation / Chanting"],
        "description": "Loves devotional music, morning/evening aarti singing, and sacred chants."
    },
    "Spiritual Discourse Scholar": {
        "preferred_categories": ["Pravachan / Spiritual Discourses", "Meditation / Chanting"],
        "description": "Interested in scriptural commentary, Bhagavad Gita lectures, and wisdom talks."
    },
    "Cultural & Festival Enthusiast": {
        "preferred_categories": ["Festival Processions", "Annadanam", "Homa / Yajna"],
        "description": "Enjoys traditional festival preparations, chariot processions, and sacred food service."
    }
}


def get_all_personas() -> Dict[str, Dict[str, Any]]:
    """Returns the list of all defined personas and their preferences."""
    return PERSONAS


def get_persona_preferred_categories(persona_name: str) -> List[str]:
    """Gets the list of preferred categories for a specific persona."""
    persona = PERSONAS.get(persona_name)
    if not persona:
        return ["Aarti", "Pooja", "Abhishekam"]
    return persona["preferred_categories"]
