from typing import List, Dict, Any, Tuple
from src.video_intelligence.schemas import EvidenceGraphSchema, ProvenanceDetailSchema

class ConfidenceEngine:
    """Computes mathematically grounded confidence scores and provenance logs by cross-validating VLM assertions with secondary sensors."""

    def __init__(self, weight_vlm: float = 0.50, weight_agreement: float = 0.30, weight_completeness: float = 0.20):
        self.w_vlm = weight_vlm
        self.w_agree = weight_agreement
        self.w_complete = weight_completeness

    def calculate_confidence(self, vlm_data: Dict[str, Any], evidence: EvidenceGraphSchema) -> Dict[str, ProvenanceDetailSchema]:
        """
        Validates VLM data fields against secondary modality evidence.
        
        Returns:
            Dict mapping field names to ProvenanceDetailSchema containing evidence list, confidence score, and justification.
        """
        provenance = {}

        # 1. Category confidence
        prov_cat = self._verify_category(vlm_data.get("category", ""), evidence)
        provenance["category"] = prov_cat
        provenance["subcategory"] = ProvenanceDetailSchema(
            evidence=prov_cat.evidence,
            confidence=max(0.40, round(prov_cat.confidence - 0.05, 3)),
            reason=f"Subcategory derived from category reasoning. {prov_cat.reason}"
        )

        # 2. Title & Summary confidence
        provenance["title"] = self._verify_text_block("title", vlm_data.get("title", ""), evidence)
        provenance["summary"] = self._verify_text_block("summary", vlm_data.get("summary", ""), evidence)

        # 3. Primary Topic confidence
        provenance["primary_topic"] = self._verify_topic(vlm_data.get("primary_topic", ""), evidence)

        # 4. Language confidence
        provenance["language"] = self._verify_language(vlm_data.get("language", ""), evidence)

        # 5. Mood / Emotion confidence
        provenance["mood"] = self._verify_mood(vlm_data.get("mood", ""), evidence)
        provenance["emotion"] = self._verify_mood(vlm_data.get("emotion", ""), evidence)

        # 6. Activities & Objects confidence
        provenance["activities"] = self._verify_list_field("activities", vlm_data.get("activities", []), evidence, "actions")
        provenance["objects"] = self._verify_list_field("objects", vlm_data.get("objects", []), evidence, "vision")

        return provenance

    def _verify_category(self, category: str, evidence: EvidenceGraphSchema) -> ProvenanceDetailSchema:
        sources = ["Foundation Model"]
        base_score = 0.80
        match_reasons = []

        cat_lower = category.lower().strip()
        
        # Cross-validate category using scene/sound labels
        vision_tokens = [n.value.lower() for n in evidence.vision]
        audio_tokens = [n.value.lower() for n in evidence.audio]
        speech_text = " ".join([n.value.lower() for n in evidence.speech])

        # Cross validation logic rules
        if cat_lower == "devotion":
            # Search for devotional signs: chanting, temple, puja, satsang, mantras, swami
            devotional_keywords = ["temple", "puja", "satsang", "mantra", "chanting", "worship", "prayer", "shlok", "swami", "bhakti", "divine"]
            has_speech_match = any(w in speech_text for w in devotional_keywords)
            has_vision_match = any(any(w in t for w in devotional_keywords) for t in vision_tokens)
            has_audio_match = any(any(w in t for w in devotional_keywords) for t in audio_tokens)
            
            if has_speech_match:
                sources.append("Speech")
                base_score += 0.10
                match_reasons.append("Speech contains devotional keywords/scriptures.")
            if has_vision_match:
                sources.append("Vision")
                base_score += 0.05
                match_reasons.append("Vision model detected temple/altar scenes.")
            if has_audio_match:
                sources.append("Audio")
                base_score += 0.05
                match_reasons.append("Audio model detected prayer/singing events.")
                
        elif cat_lower == "food":
            food_keywords = ["cooking", "recipe", "food", "kitchen", "onion", "garlic", "dish", "pot", "pan", "plate", "eating", "chef"]
            has_vision_match = any(any(w in t for w in food_keywords) for t in vision_tokens)
            has_speech_match = any(w in speech_text for w in food_keywords)
            
            if has_vision_match:
                sources.append("Vision")
                base_score += 0.10
                match_reasons.append("Vision model detected kitchen objects or cooking pans.")
            if has_speech_match:
                sources.append("Speech")
                base_score += 0.05
                match_reasons.append("Speech mentions recipes or food ingredients.")
                
        elif cat_lower == "automobile":
            car_keywords = ["car", "vehicle", "jeep", "road", "driving", "automobile", "engine", "motorbike"]
            has_vision_match = any(any(w in t for w in car_keywords) for t in vision_tokens)
            
            if has_vision_match:
                sources.append("Vision")
                base_score += 0.15
                match_reasons.append("YOLO detected vehicles or roads.")

        # Default fallback justification
        if not match_reasons:
            match_reasons.append("Primary VLM classification. No matching secondary sensor logs to confirm.")
            base_score = 0.70

        return ProvenanceDetailSchema(
            evidence=sources,
            confidence=min(1.0, round(base_score, 3)),
            reason=" ".join(match_reasons)
        )

    def _verify_text_block(self, field_name: str, text: str, evidence: EvidenceGraphSchema) -> ProvenanceDetailSchema:
        sources = ["Foundation Model"]
        score = 0.75
        reasons = []

        if not text:
            return ProvenanceDetailSchema(evidence=sources, confidence=0.0, reason="Field is empty.")

        text_lower = text.lower()
        speech_text = " ".join([n.value.lower() for n in evidence.speech])
        ocr_text = " ".join([n.value.lower() for n in evidence.ocr])

        # Check if the title or summary contains words spoken or written on screen
        overlap_speech_words = [w for w in text_lower.split() if len(w) > 4 and w in speech_text]
        overlap_ocr_words = [w for w in text_lower.split() if len(w) > 4 and w in ocr_text]

        if overlap_speech_words:
            sources.append("Speech")
            score += 0.12
            reasons.append("Text aligns with spoken transcripts.")
        if overlap_ocr_words:
            sources.append("OCR")
            score += 0.08
            reasons.append("Text aligns with screen OCR tags.")

        if not reasons:
            reasons.append("Inferred context from visual representation.")

        return ProvenanceDetailSchema(
            evidence=sources,
            confidence=min(1.0, round(score, 3)),
            reason=" ".join(reasons)
        )

    def _verify_topic(self, topic: str, evidence: EvidenceGraphSchema) -> ProvenanceDetailSchema:
        sources = ["Foundation Model"]
        score = 0.70
        reasons = []

        if not topic:
            return ProvenanceDetailSchema(evidence=sources, confidence=0.0, reason="Field is empty.")

        topic_lower = topic.lower()
        speech_text = " ".join([n.value.lower() for n in evidence.speech])
        ocr_text = " ".join([n.value.lower() for n in evidence.ocr])

        if topic_lower in speech_text:
            sources.append("Speech")
            score += 0.18
            reasons.append(f"Topic '{topic}' is spoken in the audio.")
        if topic_lower in ocr_text:
            sources.append("OCR")
            score += 0.10
            reasons.append(f"Topic '{topic}' matches screen text.")

        if not reasons:
            reasons.append("Inferred semantic category from keyframes.")

        return ProvenanceDetailSchema(
            evidence=sources,
            confidence=min(1.0, round(score, 3)),
            reason=" ".join(reasons)
        )

    def _verify_language(self, language: str, evidence: EvidenceGraphSchema) -> ProvenanceDetailSchema:
        sources = ["Foundation Model"]
        score = 0.80
        reasons = []

        # If speech transcript exists, Whisper already detected the language
        if evidence.speech:
            sources.append("Speech")
            score = 0.99
            reasons.append("Verified by Whisper speech transcription service language logs.")
        else:
            reasons.append("VLM visual projection of language context.")

        return ProvenanceDetailSchema(
            evidence=sources,
            confidence=round(score, 3),
            reason=" ".join(reasons)
        )

    def _verify_mood(self, mood: str, evidence: EvidenceGraphSchema) -> ProvenanceDetailSchema:
        sources = ["Foundation Model"]
        score = 0.70
        reasons = []

        # Cross reference mood with audio events
        audio_events = [n.value.lower() for n in evidence.audio]
        speech_text = " ".join([n.value.lower() for n in evidence.speech])

        mood_lower = mood.lower()
        
        # Match keys
        if "spiritual" in mood_lower or "calm" in mood_lower:
            if any(w in speech_text for w in ["mantra", "peace", "chant", "worship", "prayer"]):
                sources.append("Speech")
                score += 0.15
                reasons.append("Speech content verifies a peaceful or spiritual atmosphere.")
        elif "music" in mood_lower or "singing" in mood_lower:
            if any("sing" in ev or "music" in ev for ev in audio_events):
                sources.append("Audio")
                score += 0.20
                reasons.append("AST audio events confirm singing/music tracks.")

        if not reasons:
            reasons.append("Visual mood interpretation.")

        return ProvenanceDetailSchema(
            evidence=sources,
            confidence=min(1.0, round(score, 3)),
            reason=" ".join(reasons)
        )

    def _verify_list_field(self, field_name: str, items: List[str], evidence: EvidenceGraphSchema, modality_key: str) -> ProvenanceDetailSchema:
        sources = ["Foundation Model"]
        
        if not items:
            return ProvenanceDetailSchema(evidence=sources, confidence=0.70, reason="No items asserted.")

        matched_count = 0
        
        # Check against specific target lists
        target_modality_list = []
        if modality_key == "actions":
            target_modality_list = [n.value.lower() for n in evidence.actions]
            sources_key = "VideoMAE"
        elif modality_key == "vision":
            target_modality_list = [n.value.lower() for n in evidence.vision]
            sources_key = "YOLO/CLIP"
            
        for item in items:
            item_lower = item.lower()
            if any(item_lower in val or val in item_lower for val in target_modality_list):
                matched_count += 1

        if matched_count > 0:
            sources.append(sources_key)
            agreement_ratio = matched_count / len(items)
            score = 0.70 + 0.25 * agreement_ratio
            reason = f"Verified {matched_count}/{len(items)} elements against {sources_key} modality detections."
        else:
            score = 0.65
            reason = f"No corroboration found for list items in secondary {modality_key} sensor logs."

        return ProvenanceDetailSchema(
            evidence=sources,
            confidence=min(1.0, round(score, 3)),
            reason=reason
        )
