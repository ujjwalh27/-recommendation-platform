from typing import Dict, List, Any

# Dynamic persona configuration definitions
PERSONAS: Dict[str, Dict[str, Any]] = {
    "Automobile Enthusiast": {
        "preferred_categories": ["Automobile"],
        "description": "Fascinated by cars, motorbikes, engines, racing, and driving."
    },
    "Tech Enthusiast": {
        "preferred_categories": ["Tech"],
        "description": "Interested in gadgets, computers, programming, tutorials, and tech specs."
    },
    "Food Lover": {
        "preferred_categories": ["Food"],
        "description": "Loves recipes, cooking, restaurants, eating, and culinary content."
    },
    "Animal Lover": {
        "preferred_categories": ["Animal"],
        "description": "Enjoys pets, cute animal clips, wildlife, and veterinary content."
    },
    "Traveler": {
        "preferred_categories": ["Travel"],
        "description": "Passionate about vacations, nature, beaches, exploring destinations, and world travel."
    },
    "Gamer": {
        "preferred_categories": ["Gamer"],
        "description": "Watches gameplay, game tutorials, streaming highlights, and gaming hacks."
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
