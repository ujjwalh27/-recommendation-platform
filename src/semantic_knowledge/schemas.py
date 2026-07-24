from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class GraphNode(BaseModel):
    id: str
    name: str
    type: str  # One of ENTITY_TYPES or 'Scene' or 'Event' or 'Topic'
    properties: Dict[str, Any] = {}
    confidence: float = 1.0
    source: str = "KnowledgeEngine"
    timestamp: Optional[float] = None

class GraphEdge(BaseModel):
    subject_id: str
    predicate: str  # One of RELATIONSHIP_PREDICATES
    object_id: str
    confidence: float = 1.0
    timestamp: Optional[float] = None
    provenance: str = "Inferred"

class SceneSegment(BaseModel):
    scene_id: str
    timestamp_start: float
    timestamp_end: float
    duration: float
    keyframes: List[str] = []
    transcript: str = ""
    objects: List[str] = []
    actions: List[str] = []
    environment: str = ""
    audio_events: List[str] = []
    confidence: float = 1.0

class KnowledgeGraphData(BaseModel):
    video_id: str
    duration: float
    nodes: List[GraphNode] = []
    edges: List[GraphEdge] = []
    scenes: List[SceneSegment] = []

class MetadataProjection(BaseModel):
    title: str
    summary: str
    category: str
    subcategory: str
    primary_topic: str
    secondary_topics: List[str] = []
    tags: List[str] = []
    keywords: List[str] = []
    recommendation_keywords: List[str] = []
    target_audience: List[str] = []
    reasoning: str

class GraphQueryResult(BaseModel):
    query_type: str
    count: int
    nodes: List[GraphNode] = []
    edges: List[GraphEdge] = []
    sequence: List[str] = []

class EvaluationMetrics(BaseModel):
    entity_precision: float
    relationship_precision: float
    scene_accuracy: float
    temporal_accuracy: float
    concept_accuracy: float
    ontology_mapping_rate: float
    graph_completeness: float
    explainability_score: float
