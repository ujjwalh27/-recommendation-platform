from typing import List, Dict, Any
from src.video_intelligence.schemas import (
    SemanticGraphHierarchySchema,
    SemanticSceneSchema,
    SemanticRelationSchema,
    EvidenceGraphSchema
)

class KnowledgeBuilder:
    """Assembles the hierarchical semantic graph representation preserving full model provenance and relationships."""

    def build_hierarchy(
        self,
        video_id: str,
        duration: float,
        vlm_data: Dict[str, Any],
        evidence: EvidenceGraphSchema,
        confidence: Dict[str, Any],
        keyframes: List[Dict[str, Any]]
    ) -> SemanticGraphHierarchySchema:
        """
        Synthesizes raw VLM context and sensor evidence into a structured Hierarchical Knowledge Graph.
        """
        # 1. Map scenes based on sampled frames
        scenes = []
        for idx, kf in enumerate(keyframes):
            t_start = kf["timestamp"]
            # Set end time to next frame timestamp, or duration end
            t_end = keyframes[idx+1]["timestamp"] if idx < len(keyframes) - 1 else duration
            
            scenes.append(SemanticSceneSchema(
                timestamp_start=t_start,
                timestamp_end=t_end,
                keyframe_path=kf["image_path"],
                description=f"Scene keyframe {idx} displaying visual elements: {', '.join(vlm_data.get('objects', []))[:100]}"
            ))

        # 2. Extract concepts & relationships (e.g. entities doing activities)
        entities = vlm_data.get("entities", [])
        activities = vlm_data.get("activities", [])
        
        relationships = []
        # Infer basic relationships: Entity -> performs -> Activity
        for ent in entities:
            for act in activities:
                relationships.append(SemanticRelationSchema(
                    subject=ent,
                    predicate="performs_activity",
                    object=act
                ))
                
        # 3. Compile concepts (mood, emotion, category)
        concepts = list(set([
            vlm_data.get("category", ""),
            vlm_data.get("mood", ""),
            vlm_data.get("emotion", "")
        ]))
        concepts = [c for c in concepts if c]

        # 4. Compile topics
        topics = [vlm_data.get("primary_topic", "")] + vlm_data.get("secondary_topics", [])
        topics = [t for t in topics if t]

        # 5. Build final schema instance
        return SemanticGraphHierarchySchema(
            video_id=video_id,
            duration=duration,
            scenes=scenes,
            entities=entities,
            relationships=relationships,
            concepts=concepts,
            topics=topics,
            activities=activities,
            evidence=evidence,
            confidence=confidence
        )
