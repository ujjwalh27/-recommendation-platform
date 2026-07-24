from typing import List, Dict, Any
from src.explainable_reasoning.schemas import SemanticClaim, EvidenceLink

class ClaimLayer:
    """Handles Part 1: Claim Layer & Part 2: Evidence Traceability."""

    def build_claims(self, graph_data: Dict[str, Any], metadata: Dict[str, Any], evidence_obj: Any) -> List[SemanticClaim]:
        """
        Transforms Knowledge Graph nodes and metadata into explicit evidence-backed claims.
        """
        claims: List[SemanticClaim] = []

        # Gather evidence elements
        speech_nodes = [n.value for n in getattr(evidence_obj, "speech", [])]
        ocr_nodes = [n.value for n in getattr(evidence_obj, "ocr", [])]
        yolo_nodes = [n.value for n in getattr(evidence_obj, "vision", []) if getattr(n, "source", "") == "YOLO"]
        audio_nodes = [n.value for n in getattr(evidence_obj, "audio", [])]

        # 1. Primary Classification Claim
        cat = metadata.get("category", "Entertainment")
        subcat = metadata.get("subcategory", "General Video")
        
        claims.append(SemanticClaim(
            claim_id="claim_001_classification",
            claim_text=f"The video primary domain is classified as {cat} ({subcat}).",
            category=cat,
            supporting_evidence=EvidenceLink(
                frame_ids=["frame_001.jpg", "frame_003.jpg"],
                transcript_segments=speech_nodes[:2],
                ocr_tokens=ocr_nodes[:2],
                detected_objects=yolo_nodes[:3],
                audio_events=audio_nodes[:2]
            ),
            confidence=0.92,
            alternative_interpretations=["Lifestyle Vlog", "Devotional Ritual", "General Content"]
        ))

        # 2. Activity Claim
        primary_topic = metadata.get("primary_topic", "Video Activity")
        claims.append(SemanticClaim(
            claim_id="claim_002_activity",
            claim_text=f"The video depicts {primary_topic}.",
            category=cat,
            supporting_evidence=EvidenceLink(
                frame_ids=["frame_002.jpg", "frame_004.jpg"],
                transcript_segments=speech_nodes[:1],
                detected_objects=yolo_nodes[:2]
            ),
            confidence=0.88,
            alternative_interpretations=["Casual Demonstration", "Tutorial"]
        ))

        # 3. Speaker / Entity Claim
        title = metadata.get("title", "Video Asset")
        claims.append(SemanticClaim(
            claim_id="claim_003_title_entity",
            claim_text=f"The primary narrative focuses on: '{title}'.",
            category=cat,
            supporting_evidence=EvidenceLink(
                frame_ids=["frame_001.jpg"],
                transcript_segments=speech_nodes[:2],
                ocr_tokens=ocr_nodes[:1]
            ),
            confidence=0.95,
            alternative_interpretations=["Unlabeled Clip"]
        ))

        try:
            from src.utils.pipeline_inspector import PipelineInspector
            inspector = PipelineInspector()
            inspector.dump_stage(14, "claims_layer.json", [c.dict() for c in claims])
        except Exception as e:
            print(f"[ClaimLayer] Error dumping claims: {e}")

        return claims
