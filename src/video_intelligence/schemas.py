from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

# --- Modality Evidence Schemas ---
class EvidenceNodeSchema(BaseModel):
    source: str
    value: str
    confidence: float
    timestamp: Optional[float] = None

class SemanticFrameAnalysis(BaseModel):
    timestamp: float
    environment: str = "Indoor"
    objects: List[str] = []
    activities: List[str] = []
    human_interactions: List[str] = []
    religious_context: Optional[str] = None
    cultural_context: Optional[str] = None
    indoor_outdoor: str = "Indoor"
    scene_summary: str = ""

class UnifiedPerceptionEvidence(BaseModel):
    speech: Dict[str, Any] = {}
    vision: Dict[str, Any] = {}
    ocr: List[Dict[str, Any]] = []
    objects: List[Dict[str, Any]] = []
    actions: List[Dict[str, Any]] = []
    scene: List[Dict[str, Any]] = []
    confidence: Dict[str, float] = {}
    frame_analyses: List[SemanticFrameAnalysis] = []

class EvidenceGraphSchema(BaseModel):
    speech: List[EvidenceNodeSchema] = []
    ocr: List[EvidenceNodeSchema] = []
    vision: List[EvidenceNodeSchema] = []
    actions: List[EvidenceNodeSchema] = []
    audio: List[EvidenceNodeSchema] = []

# --- Raw VLM Response Schema ---
class VLMResponseSchema(BaseModel):
    title: str
    summary: str
    category: str
    subcategory: str
    primary_topic: str
    secondary_topics: List[str] = []
    entities: List[str] = []
    people: List[str] = []
    locations: List[str] = []
    activities: List[str] = []
    objects: List[str] = []
    events: List[str] = []
    keywords: List[str] = []
    recommendation_keywords: List[str] = []
    language: str
    mood: str
    emotion: str
    target_audience: List[str] = []
    reasoning: str

# --- Hierarchical Semantic Representation ---
class SemanticSceneSchema(BaseModel):
    timestamp_start: float
    timestamp_end: float
    keyframe_path: str
    description: str

class SemanticRelationSchema(BaseModel):
    subject: str
    predicate: str
    object: str

class SemanticGraphHierarchySchema(BaseModel):
    video_id: str
    duration: float
    scenes: List[SemanticSceneSchema] = []
    entities: List[str] = []
    relationships: List[SemanticRelationSchema] = []
    concepts: List[str] = []
    topics: List[str] = []
    activities: List[str] = []
    evidence: EvidenceGraphSchema
    confidence: Dict[str, Any] = {}

# --- Provenance Explanation Schema ---
class ProvenanceDetailSchema(BaseModel):
    evidence: List[str] = Field(..., description="Modality sources that support this decision")
    confidence: float = Field(..., description="Calculated confidence score between 0.0 and 1.0")
    reason: str = Field(..., description="Human-readable reason justifying the score and sources")

# --- Final Recommendation-Ready Output ---
class VideoMetadataReport(BaseModel):
    title: str
    summary: str
    category: str
    subcategory: str
    primary_topic: str
    secondary_topics: List[str] = []
    entities: List[str] = []
    people: List[str] = []
    locations: List[str] = []
    activities: List[str] = []
    objects: List[str] = []
    events: List[str] = []
    keywords: List[str] = []
    recommendation_keywords: List[str] = []
    language: str
    mood: str
    emotion: str
    target_audience: List[str] = []
    reasoning: str
    confidence: Dict[str, ProvenanceDetailSchema] = {}
