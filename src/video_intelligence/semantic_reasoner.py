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

        # Extract text aggregations for cross-checking
        speech_text = " ".join([n.value.lower() for n in evidence.speech])
        ocr_text = " ".join([n.value.lower() for n in evidence.ocr])

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

        # Rule 2: Category Override Heuristics
        # If VLM suggests a general category but secondary sensors have overwhelming evidence of a specific one:
        vlm_category = refined.get("category", "").lower().strip()
        yolo_labels = [n.value.lower() for n in evidence.vision]
        audio_events = [n.value.lower() for n in evidence.audio]

        # Case 2A: VLM guessed Food/Travel, but YOLO detected "car", "motorcycle", or "truck" multiple times
        car_count = sum(1 for val in yolo_labels if val in ["car", "motorcycle", "truck", "bus"])
        if vlm_category != "automobile" and car_count >= 2:
            refined["category"] = "Automobile"
            refined["subcategory"] = "Vehicle Review/Vlog"
            print("[Reasoner] Overrode category to 'Automobile' based on YOLO vehicle count.")

        # Case 2B: VLM guessed Entertainment/Lifestyle, but Speech transcript contains strong devotional keywords
        devotional_words = ["temple", "mantra", "puja", "satsang", "bhagavad", "krishna", "swami", "mukundananda", "bhakti"]
        devotional_speech_hits = sum(1 for w in devotional_words if w in speech_text)
        if vlm_category != "devotion" and devotional_speech_hits >= 3:
            refined["category"] = "Devotion"
            refined["subcategory"] = "Temple Discourse"
            print("[Reasoner] Overrode category to 'Devotion' based on Whisper transcript keywords.")

        # Case 2C: VLM guessed Lifestyle/Entertainment, but AST detected "singing" or "music" with high confidence
        singing_hits = any("sing" in ev or "music" in ev for ev in audio_events)
        if vlm_category != "music" and singing_hits and "singing" in speech_text:
            refined["category"] = "Music"
            refined["subcategory"] = "Vocal Performance"
            print("[Reasoner] Overrode category to 'Music' based on AST audio events.")

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
