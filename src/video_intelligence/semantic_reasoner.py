import re
from typing import Dict, Any, List
from src.video_intelligence.schemas import EvidenceGraphSchema

class SemanticReasoner:
    """Fuses VLM predictions with modular pipeline evidence, correcting contradictions and enriching attributes."""

    def reason(self, vlm_data: Dict[str, Any], evidence: EvidenceGraphSchema) -> Dict[str, Any]:
        """
        Applies reasoning rules to refine VLM metadata using the evidence graph.
        
        Returns:
            Dict containing refined metadata fields.
        """
        refined = vlm_data.copy()

        # Extract text & visual aggregations for cross-checking
        speech_text = " ".join([n.value.lower() for n in evidence.speech])
        ocr_text = " ".join([n.value.lower() for n in evidence.ocr])
        yolo_labels = [n.value.lower() for n in evidence.vision]

        # Rule 1: Language override
        # If Whisper transcribed speech, use the language it detected as the source of truth
        if evidence.speech:
            # Whisper transcripts are highly reliable for spoken language
            # Check for common language indications in the text or default to Whisper's speech engine language
            has_hindi = any(w in speech_text for w in ["hai", "ki", "ka", "ko", "aur", "yoga", "swami", "ram", "shanti"])
            if has_hindi:
                refined["language"] = "Hindi"
            else:
                refined["language"] = "English"

        # Rule 2: Strict Multimodal Category Rules (User Mandated)
        title_str = vlm_data.get("title", "").lower()
        caption_str = vlm_data.get("caption", "").lower()
        summary_str = vlm_data.get("summary", "").lower()
        text_bag = f"{title_str} {caption_str} {summary_str} {speech_text} {ocr_text} {' '.join(yolo_labels)}"

        # Rule 2A: AARTI — Flame/Fire involved for deity (flame, diya, torch, camphor, oil lamp, night ceremony)
        flame_keywords = ["flame", "fire", "diya", "torch", "lamp", "aarti", "oil lamp", "burning oil", "camphor", "fire ritual"]
        has_flame_evidence = any(k in text_bag for k in flame_keywords)
        
        # Rule 2B: BHAJAN — Devotional gathering with clapping/hands raised/singing/kirtan or 'THIS BHAJAN'
        bhajan_keywords = ["clapping", "hand clapping", "applause", "hands raised", "bhajan", "kirtan", "satsang", "singing", "devotional gathering"]
        has_bhajan_evidence = any(k in text_bag for k in bhajan_keywords)

        # Rule 2C: ABHISHEKAM — Liquid pouring (milk, water, panchamrutha, curd, honey)
        abhishekam_keywords = ["abhishekam", "pouring water", "pouring milk", "doodh", "panchamrutha", "white liquid", "pouring stream"]
        has_abhishekam_evidence = any(k in text_bag for k in abhishekam_keywords)

        # Rule 2D: POOJA — Flowers & quiet ritual/lamps combination without liquid stream or active torch waving
        pooja_keywords = ["flower", "garland", "petal", "incense", "tilak", "archana", "puja", "pooja"]
        has_pooja_evidence = any(k in text_bag for k in pooja_keywords)

        if has_flame_evidence:
            refined["category"] = "Aarti"
            refined["subcategory"] = "Flame Worship & Lamp Ritual"
            print("[Reasoner] Set category to 'Aarti' based on active flame/fire evidence.")
        elif has_abhishekam_evidence:
            refined["category"] = "Abhishekam"
            refined["subcategory"] = "Milk / Panchamrutha / Water Abhishekam"
            print("[Reasoner] Set category to 'Abhishekam' based on liquid pouring evidence.")
        elif has_bhajan_evidence:
            refined["category"] = "Bhajan"
            refined["subcategory"] = "Devotional Hymns & Songs"
            print("[Reasoner] Set category to 'Bhajan' based on devotional singing/clapping evidence.")
        elif has_pooja_evidence:
            refined["category"] = "Pooja"
            refined["subcategory"] = "Devotional Ritual & Worship"
            print("[Reasoner] Set category to 'Pooja' based on flower & ritual offering evidence.")

        # Rule 3: Grounded Entity & Activity enrichment
        # Enrich entities from OCR text if they look like proper nouns (e.g. brand names, creator tags)
        ocr_proper_nouns = re.findall(r"\b[A-Z][a-z]+\b", ocr_text)
        for word in ocr_proper_nouns:
            if word not in refined["entities"] and len(word) > 3:
                refined["entities"].append(word)

        # Rule 4: Clean list fields (de-duplicate & format)
        refined["keywords"] = self._clean_list(refined.get("keywords", []))
        refined["recommendation_keywords"] = self._clean_list(refined.get("recommendation_keywords", []))
        refined["entities"] = self._clean_list(refined.get("entities", []))
        refined["activities"] = self._clean_list(refined.get("activities", []))
        refined["objects"] = self._clean_list(refined.get("objects", []))

        return refined

    def _clean_list(self, items: List[str]) -> List[str]:
        """Cleans whitespace, removes empty values, and filters duplicates."""
        seen = set()
        cleaned = []
        for item in items:
            val = str(item).strip()
            if val and val.lower() not in seen:
                cleaned.append(val)
                seen.add(val.lower())
        return cleaned
