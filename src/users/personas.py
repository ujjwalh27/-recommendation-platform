from typing import Dict, List, Any

# Dynamic spiritual and domain persona configuration definitions (Canonical Taxonomy)
PERSONAS: Dict[str, Dict[str, Any]] = {
    "Devotional Practitioner": {
        "preferred_categories": ["Aarti", "Pooja", "Abhishekam"],
        "baseline_scores": {"Aarti": 40.0, "Pooja": 35.0, "Abhishekam": 25.0},
        "preferred_deities": ["Lord Shiva", "Lord Krishna & Radha", "Lord Ganesha"],
        "preferred_ritual_families": ["Aarti", "Pooja", "Abhishekam"],
        "description": "Engaged in daily shrine worship, lamp lighting, and temple rituals."
    },
    "Temple Pilgrim": {
        "preferred_categories": ["Temple Darshan", "Abhishekam", "Pooja"],
        "baseline_scores": {"Temple Darshan": 45.0, "Abhishekam": 30.0, "Pooja": 25.0},
        "preferred_deities": ["Lord Shiva", "Lord Venkateshwara", "Lord Rama"],
        "preferred_ritual_families": ["Temple Darshan", "Abhishekam"],
        "description": "Fascinated by sacred fluid pourings, lingam abhishekam, and temple visits."
    },
    "Bhajan & Chant Seeker": {
        "preferred_categories": ["Bhajan", "Aarti", "Temple Darshan"],
        "baseline_scores": {"Bhajan": 50.0, "Aarti": 30.0, "Temple Darshan": 20.0},
        "preferred_deities": ["Lord Krishna & Radha", "Lord Rama", "Lord Shiva"],
        "preferred_ritual_families": ["Bhajan", "Aarti"],
        "description": "Loves devotional music, morning/evening aarti singing, and sacred chants."
    },
    "Spiritual Discourse Scholar": {
        "preferred_categories": ["Pooja", "Bhajan", "Temple Darshan"],
        "baseline_scores": {"Pooja": 40.0, "Bhajan": 35.0, "Temple Darshan": 25.0},
        "preferred_deities": ["Lord Krishna", "Lord Rama", "Lord Shiva"],
        "preferred_ritual_families": ["Pooja", "Bhajan"],
        "description": "Interested in scriptural commentary, Bhagavad Gita lectures, and wisdom talks."
    },
    "Cultural & Festival Enthusiast": {
        "preferred_categories": ["Festival Processions", "Pooja", "Aarti"],
        "baseline_scores": {"Festival Processions": 50.0, "Pooja": 30.0, "Aarti": 20.0},
        "preferred_deities": ["Lord Ganesha", "Lord Krishna & Radha", "Lord Shiva"],
        "preferred_ritual_families": ["Procession", "Festival Processions"],
        "description": "Enjoys traditional festival preparations, chariot processions, and sacred food service."
    }
}

DEFAULT_BASELINE_SCORES = {
    "Aarti": 30.0,
    "Pooja": 30.0,
    "Abhishekam": 20.0,
    "Bhajan": 20.0
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


def get_persona_baseline_scores(persona_name: str) -> Dict[str, float]:
    """Gets cold-start baseline category scores for a specific persona."""
    persona = PERSONAS.get(persona_name)
    if not persona or "baseline_scores" not in persona:
        return dict(DEFAULT_BASELINE_SCORES)
    return dict(persona["baseline_scores"])

