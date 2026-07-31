"""
Task 2 – Knowledge Base Loader Module
Loads and queries the versioned CMREE domain knowledge base YAML.
"""

import os
from typing import Dict, Any, Optional

try:
    import yaml
    YAML_AVAIL = True
except ImportError:
    YAML_AVAIL = False


class KnowledgeBaseLoader:
    """Loads and indexes knowledge_base.yaml for fast entity and ritual lookup."""

    def __init__(self, kb_path: str = None):
        if kb_path is None:
            kb_path = os.path.join(os.path.dirname(__file__), "knowledge_base.yaml")
        
        self.kb_path = kb_path
        self.kb_data = {}
        self.load_kb()

    def load_kb(self):
        """Loads knowledge_base.yaml from disk."""
        if not os.path.exists(self.kb_path):
            print(f"[CMREE-KB] Warning: KB file not found at {self.kb_path}")
            return

        try:
            if YAML_AVAIL:
                with open(self.kb_path, "r", encoding="utf-8") as f:
                    self.kb_data = yaml.safe_load(f) or {}
            else:
                # Basic fallback parsing if PyYAML is missing
                self.kb_data = {}
            print(f"[CMREE-KB] Loaded KB version: {self.get_metadata().get('version', 'unknown')}")
        except Exception as e:
            print(f"[CMREE-KB] Error loading KB: {e}")

    def get_metadata(self) -> Dict[str, Any]:
        return self.kb_data.get("metadata", {})

    def get_deities(self) -> Dict[str, Any]:
        return self.kb_data.get("deities", {})

    def get_rituals(self) -> Dict[str, Any]:
        return self.kb_data.get("rituals", {})

    def get_temples(self) -> Dict[str, Any]:
        return self.kb_data.get("temples", {})

    def lookup_deity_by_temple(self, temple_name: str) -> Optional[str]:
        """Infers deity name associated with a temple."""
        temples = self.get_temples()
        t_lower = temple_name.lower().strip()
        for t_key, t_info in temples.items():
            if t_lower in t_key.lower() or t_lower in t_info.get("canonical_name", "").lower():
                return t_info.get("deity")
        return None

    def lookup_family_by_ritual(self, ritual_name: str) -> Optional[str]:
        """Infers ritual family from a specific ritual name."""
        if not ritual_name:
            return "Pooja"
        r_lower = ritual_name.lower().strip()
        if any(k in r_lower for k in ["aarti", "arti", "flame", "lamp"]):
            return "Aarti"
        if any(k in r_lower for k in ["abhishekam", "abhishek", "pouring", "bathing", "lingam"]):
            return "Abhishekam"
        if any(k in r_lower for k in ["bhajan", "song", "hymn", "music"]):
            return "Bhajan"
        if any(k in r_lower for k in ["meditation", "dhyana", "japa", "mantra"]):
            return "Meditation"
        if any(k in r_lower for k in ["homa", "havan", "yajna", "yagya"]):
            return "Homa / Yajna"
        if any(k in r_lower for k in ["annadanam", "bhandara", "prasad"]):
            return "Annadanam"
        if any(k in r_lower for k in ["kirtan", "sankeerthana"]):
            return "Kirtan"
        if any(k in r_lower for k in ["archana", "ashtottara"]):
            return "Archana"
        if any(k in r_lower for k in ["pravachan", "katha", "satsang", "discourse"]):
            return "Pravachan"
        if any(k in r_lower for k in ["procession", "yatra", "ratha"]):
            return "Procession"
        if any(k in r_lower for k in ["darshan", "sanctum", "shrine view"]):
            return "Darshan"
        if any(k in r_lower for k in ["pooja", "puja", "worship"]):
            return "Pooja"

        rituals = self.get_rituals()
        for r_key, r_info in rituals.items():
            if r_lower in r_key.lower() or r_lower in r_info.get("canonical_name", "").lower():
                return r_info.get("family")
        return "Pooja"
