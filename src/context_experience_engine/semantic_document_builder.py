from typing import Dict, Any


class SemanticDocumentBuilder:
    """
    Synthesizes CMREE Canonical Metadata + CEEE Perceptual Metadata + CEEE Emotional Metadata + Evidence Summary
    into an upgraded semantic document for SentenceTransformer (`all-MiniLM-L6-v2`) embeddings and FAISS search.
    """

    def build_document(
        self,
        canonical_metadata: Dict[str, Any],
        perceptual_metadata: Dict[str, Any],
        emotional_metadata: Dict[str, Any],
        evidence_doc: Dict[str, Any] = None,
        raw_summary: str = "",
        title: str = ""
    ) -> str:
        """
        Constructs a structured, weighted semantic context string.
        """
        parts = []

        # 1. Title & High-level Summary
        if title:
            parts.append(f"Title: {title}")
        if raw_summary:
            parts.append(f"Summary: {raw_summary}")

        # 2. CMREE Canonical Metadata Section
        cat = canonical_metadata.get("primary_category", "")
        rit = canonical_metadata.get("primary_ritual", "")
        fam = canonical_metadata.get("ritual_family", "")
        deity = canonical_metadata.get("primary_deity", "")
        temple = canonical_metadata.get("temple", "")
        tradition = canonical_metadata.get("tradition", "")
        offerings = canonical_metadata.get("offerings", [])

        canonical_str_parts = []
        if cat:
            canonical_str_parts.append(f"Category: {cat}")
        if rit:
            canonical_str_parts.append(f"Ritual: {rit}")
        if fam:
            canonical_str_parts.append(f"Family: {fam}")
        if deity:
            canonical_str_parts.append(f"Deity: {deity}")
        if temple:
            canonical_str_parts.append(f"Temple: {temple}")
        if tradition:
            canonical_str_parts.append(f"Tradition: {tradition}")
        if offerings:
            off_str = ", ".join(offerings) if isinstance(offerings, list) else str(offerings)
            canonical_str_parts.append(f"Offerings: {off_str}")

        if canonical_str_parts:
            parts.append(f"Canonical Metadata: {' | '.join(canonical_str_parts)}")

        # 3. Layer 2 Perceptual Metadata Section
        perc_parts = []
        for field in ["environment", "lighting", "camera_distance", "camera_motion", "crowd_size", "motion_level", "decoration_level", "scene_density"]:
            val_obj = perceptual_metadata.get(field, {})
            val = val_obj.get("value") if isinstance(val_obj, dict) else str(val_obj)
            if val and val != "Normal" and val != "Unspecified":
                perc_parts.append(f"{field.replace('_', ' ').title()}: {val}")

        if perc_parts:
            parts.append(f"Perceptual Context: {', '.join(perc_parts)}")

        # 4. Layer 3 Emotional Metadata Section
        emo_parts = []
        for field in ["energy_level", "emotional_tone", "devotional_intensity", "ambience", "pace", "immersiveness"]:
            val_obj = emotional_metadata.get(field, {})
            val = val_obj.get("value") if isinstance(val_obj, dict) else str(val_obj)
            if val and val != "Normal" and val != "Unspecified":
                emo_parts.append(f"{field.replace('_', ' ').title()}: {val}")

        if emo_parts:
            parts.append(f"Experiential & Emotional Context: {', '.join(emo_parts)}")

        # 5. Multimodal Evidence Summary Section (New MSFACR extension)
        if evidence_doc:
            ev_summary_items = []
            vis_objs = evidence_doc.get("visual", {}).get("objects", [])
            if vis_objs:
                ev_summary_items.append(f"Objects detected: {', '.join(vis_objs[:4])}")
            ast_evs = [k for k, v in evidence_doc.get("audio", {}).items() if v is True and k != "silence"]
            if ast_evs:
                ev_summary_items.append(f"Audio events: {', '.join(ast_evs)}")

            if ev_summary_items:
                parts.append(f"Evidence Summary: {' | '.join(ev_summary_items)}")

        # Clean and return full document string
        full_doc = " ".join(parts).strip()
        return full_doc
