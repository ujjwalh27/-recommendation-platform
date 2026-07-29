"""
Task 3 – Entity Resolution Module
Normalizes raw observation tokens into canonical semantic entities.
Resolves synonyms, spelling variations, multilingual aliases, and abbreviations.
"""

import os
import json
import re
from typing import Dict, Any, List, Optional


class EntityResolver:
    """Normalizes raw observations into canonical entity structures using dictionary lookup & fuzzy alias matching."""

    def __init__(self, dict_path: str = None):
        if dict_path is None:
            dict_path = os.path.join(os.path.dirname(__file__), "entity_alias_dictionary.json")
        
        self.dict_path = dict_path
        self.aliases = {}
        self._load_dictionary()

    def _load_dictionary(self):
        if os.path.exists(self.dict_path):
            with open(self.dict_path, "r", encoding="utf-8") as f:
                self.aliases = json.load(f)

    def resolve_entity(self, raw_term: str, category: str = "objects") -> Optional[str]:
        """
        Resolves a single raw term to its canonical entity string.
        category: 'deities' | 'objects' | 'actions' | 'rituals'
        """
        if not raw_term:
            return None

        clean_term = raw_term.strip().lower()
        cat_dict = self.aliases.get(category, {})

        # Direct canonical name match
        for canonical, alias_list in cat_dict.items():
            if clean_term == canonical.lower():
                return canonical
            for alias in alias_list:
                if clean_term == alias.lower() or alias.lower() in clean_term or clean_term in alias.lower():
                    return canonical

        return None

    def resolve_observation(self, observation: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes a full normalized observation payload and adds canonical entity annotations.
        """
        resolved = dict(observation)

        # 1. Resolve objects
        raw_objects = observation.get("objects", [])
        resolved_objects = []
        canonical_objects_set = set()

        for obj in raw_objects:
            obj_name = obj.get("name", "") if isinstance(obj, dict) else str(obj)
            canonical = self.resolve_entity(obj_name, "objects") or obj_name
            canonical_objects_set.add(canonical)
            resolved_objects.append({
                "raw_name": obj_name,
                "canonical_name": canonical,
                "confidence": obj.get("confidence", 0.85) if isinstance(obj, dict) else 0.85
            })

        # Also search scene & ocr_text for objects (e.g., Shiva Linga in text or scene description)
        combined_text = (
            observation.get("scene", "") + " " +
            " ".join(observation.get("ocr_text", [])) + " " +
            observation.get("speech_text", "")
        )

        for canonical_name, alias_list in self.aliases.get("objects", {}).items():
            for alias in [canonical_name] + alias_list:
                if re.search(r'\b' + re.escape(alias) + r'\b', combined_text, re.IGNORECASE):
                    if canonical_name not in canonical_objects_set:
                        canonical_objects_set.add(canonical_name)
                        resolved_objects.append({
                            "raw_name": alias,
                            "canonical_name": canonical_name,
                            "confidence": 0.90
                        })
                    break

        resolved["resolved_objects"] = resolved_objects
        resolved["canonical_objects"] = sorted(list(canonical_objects_set))

        # 2. Resolve actions
        raw_actions = observation.get("actions", [])
        resolved_actions = []
        canonical_actions_set = set()

        for act in raw_actions:
            canonical = self.resolve_entity(act, "actions") or act
            canonical_actions_set.add(canonical)
            resolved_actions.append({"raw_action": act, "canonical_action": canonical})

        for canonical_act, alias_list in self.aliases.get("actions", {}).items():
            for alias in [canonical_act] + alias_list:
                if re.search(r'\b' + re.escape(alias) + r'\b', combined_text, re.IGNORECASE):
                    if canonical_act not in canonical_actions_set:
                        canonical_actions_set.add(canonical_act)
                        resolved_actions.append({"raw_action": alias, "canonical_action": canonical_act})
                    break

        resolved["resolved_actions"] = resolved_actions
        resolved["canonical_actions"] = sorted(list(canonical_actions_set))

        # 3. Resolve deities
        canonical_deities_set = set()
        for canonical_deity, alias_list in self.aliases.get("deities", {}).items():
            for alias in [canonical_deity] + alias_list:
                if re.search(r'\b' + re.escape(alias) + r'\b', combined_text, re.IGNORECASE):
                    canonical_deities_set.add(canonical_deity)
                    break

        resolved["canonical_deities"] = sorted(list(canonical_deities_set))

        return resolved
