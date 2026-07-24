import os
import json
from typing import List, Dict, Any
from src.explainable_reasoning.schemas import SemanticMemoryConcept
from src.explainable_reasoning.config import MEMORY_STORE_PATH

class SemanticMemory:
    """Handles Part 6: Reusable Semantic Memory & Concept Association Accumulation."""

    def __init__(self, memory_file: str = None):
        self.memory_file = memory_file or MEMORY_STORE_PATH
        os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
        self.memory_data = self._load_memory()

    def _load_memory(self) -> Dict[str, Dict[str, Any]]:
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[SemanticMemory] Error loading memory file: {e}")
        
        # Default Seed Associations
        return {
            "Devotion": {
                "concept_name": "Devotion",
                "domain": "Spiritual",
                "co_occurrence_count": 12,
                "associated_entities": ["Temple", "Priest", "Bell", "Prayer", "Flowers", "Bhajan", "Aarti", "Mantras"]
            },
            "Food": {
                "concept_name": "Food",
                "domain": "Culinary",
                "co_occurrence_count": 8,
                "associated_entities": ["Kitchen", "Pan", "Vegetables", "Recipe", "Ingredients", "Bowl", "Cooking"]
            },
            "Automobile": {
                "concept_name": "Automobile",
                "domain": "Automotive",
                "co_occurrence_count": 5,
                "associated_entities": ["Car", "Road", "Driving", "Motorcycle", "Engine", "Vehicle"]
            }
        }

    def update_memory(self, category: str, keywords: List[str]):
        """Accumulates recurring concept co-occurrences into persistent semantic memory."""
        if category not in self.memory_data:
            self.memory_data[category] = {
                "concept_name": category,
                "domain": category,
                "co_occurrence_count": 1,
                "associated_entities": keywords
            }
        else:
            item = self.memory_data[category]
            item["co_occurrence_count"] += 1
            existing = set(item["associated_entities"])
            for kw in keywords:
                if kw not in existing:
                    item["associated_entities"].append(kw)
                    existing.add(kw)

        # Save to disk
        try:
            with open(self.memory_file, "w", encoding="utf-8") as f:
                json.dump(self.memory_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[SemanticMemory] Error saving memory file: {e}")

    def query_concept_memory(self, concept: str) -> List[SemanticMemoryConcept]:
        """Queries accumulated semantic memory for associated concepts."""
        results = []
        for cat, data in self.memory_data.items():
            if concept.lower() in cat.lower() or any(concept.lower() in ent.lower() for ent in data["associated_entities"]):
                results.append(SemanticMemoryConcept(
                    concept_name=data["concept_name"],
                    associated_entities=data["associated_entities"],
                    co_occurrence_count=data["co_occurrence_count"],
                    domain=data["domain"]
                ))
        return results
