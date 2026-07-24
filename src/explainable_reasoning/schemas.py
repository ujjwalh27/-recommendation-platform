from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class EvidenceLink(BaseModel):
    frame_ids: List[str] = []
    transcript_segments: List[str] = []
    ocr_tokens: List[str] = []
    detected_objects: List[str] = []
    audio_events: List[str] = []

class SemanticClaim(BaseModel):
    claim_id: str
    claim_text: str
    category: str
    supporting_evidence: EvidenceLink
    confidence: float = 0.90
    alternative_interpretations: List[str] = []

class SemanticHypothesis(BaseModel):
    hypothesis_id: str
    label: str
    confidence: float
    supporting_evidence_count: int
    selection_reasoning: str

class ConflictResolution(BaseModel):
    conflict_id: str
    topic: str
    conflicting_sources: List[str]
    trusted_source: str
    rejected_source: str
    resolution_reasoning: str

class EpisodeSegment(BaseModel):
    episode_id: str
    title: str
    scene_ids: List[str] = []
    timestamp_start: float
    timestamp_end: float
    narrative_summary: str

class SemanticMemoryConcept(BaseModel):
    concept_name: str
    associated_entities: List[str] = []
    co_occurrence_count: int = 1
    domain: str = "General"

class XAIResponse(BaseModel):
    query: str
    primary_answer: str
    evidence_cited: List[str] = []
    frames_influenced: List[str] = []
    alternatives_considered: List[str] = []
    uncertainty_drivers: List[str] = []
