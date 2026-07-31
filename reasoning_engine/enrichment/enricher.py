"""
Task 5 – Metadata Enrichment Module
Derives secondary contextual metadata (ritual family, deity, tradition, location, festival season, keywords)
using the knowledge base and rule inferences.
"""

from typing import Dict, Any, List
from reasoning_engine.knowledge_base.loader import KnowledgeBaseLoader


class MetadataEnricher:
    """Enriches reasoned metadata with relational domain knowledge."""

    def __init__(self, kb_loader: KnowledgeBaseLoader = None):
        self.kb = kb_loader or KnowledgeBaseLoader()

    def enrich(self, resolved_obs: Dict[str, Any], rule_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Performs multi-step enrichment on the observation and rule inference results.
        Returns enriched dict containing normalized metadata fields.
        """
        enriched = {}

        # 1. Primary Ritual & Ritual Family
        primary_ritual = rule_output.get("inferred_primary_ritual") or "Devotional Worship"
        ritual_family = self.kb.lookup_family_by_ritual(primary_ritual) or "Pooja"
        
        enriched["primary_ritual"] = primary_ritual
        enriched["ritual_family"] = ritual_family

        # 2. Deity Resolution
        deities_found = resolved_obs.get("canonical_deities", [])
        primary_deity = rule_output.get("inferred_primary_deity")
        
        if not primary_deity and deities_found:
            primary_deity = deities_found[0]

        # 3. Temple Identification
        temple_found = None
        combined_text = (
            resolved_obs.get("scene", "") + " " +
            " ".join(resolved_obs.get("ocr_text", [])) + " " +
            resolved_obs.get("speech_text", "")
        )

        for t_key, t_info in self.kb.get_temples().items():
            c_name = t_info.get("canonical_name", t_key)
            if t_key.lower() in combined_text.lower() or c_name.lower() in combined_text.lower():
                temple_found = c_name
                if not primary_deity and t_info.get("deity"):
                    primary_deity = t_info.get("deity")
                break

        enriched["primary_deity"] = primary_deity or (deities_found[0] if deities_found else None)
        enriched["temple"] = temple_found

        # 4. Tradition & Tradition Category
        deities_kb = self.kb.get_deities()
        tradition = "Universal Devotional"
        if enriched["primary_deity"] and enriched["primary_deity"] in deities_kb:
            tradition = deities_kb[enriched["primary_deity"]].get("tradition", "Universal Devotional")
        enriched["tradition"] = tradition

        # 5. Offerings
        rule_offerings = set(rule_output.get("inferred_offerings", []))
        canonical_objs = set(resolved_obs.get("canonical_objects", []))
        
        for obj in canonical_objs:
            if obj in ["Water Vessel", "Water Pot"]: rule_offerings.add("Water")
            elif obj in ["Milk Vessel", "Milk Kalash"]: rule_offerings.add("Milk")
            elif obj in ["Marigold Flowers", "Garland"]: rule_offerings.add("Flowers")
            elif obj in ["Oil Lamp", "Aarti Diya"]: rule_offerings.add("Oil Lamp")
            elif obj == "Fire Altar": rule_offerings.add("Ghee")

        enriched["offerings"] = sorted(list(rule_offerings)) if rule_offerings else ["Flowers"]

        # 6. Keywords Generation (Deduplicated, Normalized)
        fallback_cat = "Any other devotional or temple-related activities"
        raw_keywords = [
            enriched["primary_category"] if "primary_category" in rule_output else fallback_cat,
            primary_ritual,
            ritual_family,
            enriched["primary_deity"],
            tradition,
            resolved_obs.get("language", "Hindi")
        ]
        if temple_found: raw_keywords.append(temple_found)
        raw_keywords.extend(enriched["offerings"])

        keywords_clean = []
        seen = set()
        for kw in raw_keywords:
            if kw and kw.lower() not in seen:
                seen.add(kw.lower())
                keywords_clean.append(kw)

        enriched["keywords"] = keywords_clean
        enriched["primary_category"] = rule_output.get("inferred_primary_category", fallback_cat)

        return enriched
