import os
import json
import re

class DaivEntityResolver:
    """
    Hierarchical Entity Resolver for Daiv Platform.
    Resolves generic concepts (e.g., 'Temple', 'Prayer', 'Abhishekam') 
    to fine-grained, domain-specific entities (e.g., 'Shirdi Sai Temple', 'Sai Kakad Aarti', 'Milk Abhishekam').
    """

    def __init__(self, kb_path=None):
        if kb_path is None:
            kb_path = os.path.join(os.path.dirname(__file__), "daiv_knowledge_base.json")
        
        self.kb_path = kb_path
        self.kb = self._load_kb()

    def _load_kb(self):
        if os.path.exists(self.kb_path):
            with open(self.kb_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def resolve_deity(self, raw_text_tokens, visual_cues=None):
        """
        Resolves generic deity references to canonical deity names (e.g. Shirdi Sai Baba, Lord Hanuman).
        """
        text_concat = " ".join([str(x) for x in raw_text_tokens]).lower() if isinstance(raw_text_tokens, list) else str(raw_text_tokens).lower()
        vis_concat = " ".join([str(x) for x in visual_cues]).lower() if visual_cues else ""
        combined = text_concat + " " + vis_concat


        # Search Deities in KB
        for deity_name, d_info in self.kb.get("deities", {}).items():
            for alias in d_info.get("aliases", []):
                if alias.lower() in combined:
                    return {
                        "canonical_name": d_info["canonical_name"],
                        "tradition": d_info["tradition"],
                        "resolution_path": f"Deity -> {d_info['tradition']} -> {d_info['canonical_name']}",
                        "confidence": 0.96
                    }
        
        # Specific deity keyword matching
        if "sai" in combined:
            return {"canonical_name": "Shirdi Sai Baba", "tradition": "Sai", "resolution_path": "Deity -> Sai -> Shirdi Sai Baba", "confidence": 0.92}
        elif "hanuman" in combined or "bajrangbali" in combined:
            return {"canonical_name": "Lord Hanuman", "tradition": "Vaishnava", "resolution_path": "Deity -> Vaishnava -> Lord Hanuman", "confidence": 0.94}
        elif "shiva" in combined or "lingam" in combined or "mahadev" in combined or "bholenath" in combined:
            return {"canonical_name": "Lord Shiva", "tradition": "Shaiva", "resolution_path": "Deity -> Shaiva -> Lord Shiva", "confidence": 0.94}
        elif "ganesha" in combined or "ganpati" in combined or "vinayaka" in combined or "elephant" in combined:
            return {"canonical_name": "Lord Ganesha", "tradition": "Smarta", "resolution_path": "Deity -> Smarta -> Lord Ganesha", "confidence": 0.92}
        elif "durga" in combined or "devi" in combined or "shakti" in combined or "mata" in combined:
            return {"canonical_name": "Goddess Durga", "tradition": "Shakta", "resolution_path": "Deity -> Shakta -> Goddess Durga", "confidence": 0.92}
        elif "krishna" in combined or "kanha" in combined:
            return {"canonical_name": "Lord Krishna", "tradition": "Vaishnava", "resolution_path": "Deity -> Vaishnava -> Lord Krishna", "confidence": 0.92}

        # Return None when no spiritual deity is identified
        return {"canonical_name": None, "tradition": None, "resolution_path": None, "confidence": 0.0}

    def resolve_ritual(self, raw_ritual, detected_offerings=None, speech_text="", visual_cues=None, vlm_summary=""):
        """
        Resolves generic ritual tokens ('Abhishekam', 'Aarti', 'Prayer') to hierarchical sub-types.
        """
        r_str = str(raw_ritual).lower()
        off_concat = " ".join(detected_offerings).lower() if detected_offerings else ""
        speech_str = str(speech_text).lower()
        vis_str = " ".join([str(x) for x in visual_cues]).lower() if visual_cues else ""
        vlm_str = str(vlm_summary).lower()
        
        combined = f"{r_str} {off_concat} {speech_str} {vis_str} {vlm_str}"

        has_aarti = any(w in combined for w in ["aarti", "arti", "deepa", "lamp", "flame", "diya", "camphor", "kapoor"])
        
        # High-precision Abhishekam signals (active liquid pouring, bathing, Lingam ritual, or explicit abhishekam)
        abhishekam_keywords = [
            "abhishekam", "abhishek", "jalabhishekam", "doodh abhishek", "doodhabhishek",
            "pouring", "bathing", "anointed", "white liquid", "liquid stream", "water over", 
            "milk over", "panchamrut", "panchamrutha", "lingam", "linga", "shiva lingam", "shivaling", "kalash"
        ]
        has_active_pouring = any(w in combined for w in abhishekam_keywords)

        # Abhishekam takes absolute priority over Aarti flame when liquid/bathing/Lingam ritual is present
        if has_active_pouring:
            if "milk" in combined or "doodh" in combined:
                return {
                    "primary_ritual": "Abhishekam",
                    "sub_ritual": "Milk Abhishekam",
                    "hierarchical_path": "Ritual -> Abhishekam -> Milk Abhishekam",
                    "confidence": 0.98
                }
            elif "panchamrut" in combined or "panchamrutha" in combined or ("curd" in combined and "honey" in combined):
                return {
                    "primary_ritual": "Abhishekam",
                    "sub_ritual": "Panchamrutha Abhishekam",
                    "hierarchical_path": "Ritual -> Abhishekam -> Panchamrutha Abhishekam",
                    "confidence": 0.96
                }
            return {
                "primary_ritual": "Abhishekam",
                "sub_ritual": "Water Abhishekam",
                "hierarchical_path": "Ritual -> Abhishekam -> Water Abhishekam",
                "confidence": 0.95
            }

        # Aarti flame ritual takes precedence if flame is present and no liquid pouring is occurring
        if has_aarti and not has_active_pouring:
            if "morning" in combined or "kakad" in combined:
                return {
                    "primary_ritual": "Aarti",
                    "sub_ritual": "Kakad Aarti",
                    "hierarchical_path": "Ritual -> Aarti -> Kakad Aarti",
                    "confidence": 0.96
                }
            return {
                "primary_ritual": "Aarti",
                "sub_ritual": "Devotional Aarti",
                "hierarchical_path": "Ritual -> Aarti -> Devotional Aarti",
                "confidence": 0.95
            }

        elif "pravachan" in combined or "katha" in combined or "gita" in combined or "teaching" in combined:
            return {
                "primary_ritual": "Pravachan",
                "sub_ritual": "Bhagavad Gita Pravachan",
                "hierarchical_path": "Ritual -> Pravachan -> Bhagavad Gita Pravachan",
                "confidence": 0.95
            }

        return {
            "primary_ritual": None,
            "sub_ritual": None,
            "hierarchical_path": None,
            "confidence": 0.0
        }
