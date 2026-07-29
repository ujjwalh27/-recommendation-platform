from typing import Dict, List, Any

# Dynamic spiritual and domain persona configuration definitions
PERSONAS: Dict[str, Dict[str, Any]] = {
    "Devotional Practitioner": {
        "preferred_categories": ["Pooja & Aarti", "Abhishekam"],
        "description": "Engaged in daily shrine worship, lamp lighting, and temple rituals."
    },
    "Temple Pilgrim": {
        "preferred_categories": ["Abhishekam", "Archana & Mantras", "Pooja & Aarti"],
        "description": "Fascinated by sacred fluid pourings, lingam abhishekam, and temple visits."
    },
    "Bhajan & Chant Seeker": {
        "preferred_categories": ["Bhajan & Kirtan", "Pooja & Aarti", "Archana & Mantras"],
        "description": "Loves devotional music, morning/evening aarti singing, and sacred chants."
    },
    "Spiritual Discourse Scholar": {
        "preferred_categories": ["Pravachan & Discourses", "Archana & Mantras"],
        "description": "Interested in scriptural commentary, Bhagavad Gita lectures, and wisdom talks."
    },
    "Cultural & Festival Enthusiast": {
        "preferred_categories": ["Lifestyle & Culture", "Performative Arts"],
        "description": "Enjoys traditional festival preparations, cultural attire, and classical dance."
    },
    "Legal & Rights Advocate": {
        "preferred_categories": ["Legal & Society"],
        "description": "Follows legal awareness, citizen rights, and social commentary."
    }
}


def get_all_personas() -> Dict[str, Dict[str, Any]]:
    """Returns the list of all defined personas and their preferences."""
    return PERSONAS


def get_persona_preferred_categories(persona_name: str) -> List[str]:
    """Gets the list of preferred categories for a specific persona."""
    persona = PERSONAS.get(persona_name)
    if not persona:
        return []
    return persona["preferred_categories"]
