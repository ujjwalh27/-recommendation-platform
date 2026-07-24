from typing import List, Dict, Any
from src.semantic_knowledge.schemas import SceneSegment, GraphNode

class SceneGraphBuilder:
    """Handles Step 1: Video Scene Segmentation and Scene Node creation."""

    def build_scenes(self, keyframes: List[Dict[str, Any]], duration: float, evidence: Any) -> List[SceneSegment]:
        """
        Segments the video into chronological scene units based on keyframe boundaries and secondary sensor logs.
        """
        scenes = []
        if not keyframes:
            # Fallback single scene for zero keyframes
            scenes.append(SceneSegment(
                scene_id="scene_000",
                timestamp_start=0.0,
                timestamp_end=duration,
                duration=duration,
                keyframes=[],
                transcript="",
                objects=[],
                actions=[],
                environment="General Environment",
                audio_events=[],
                confidence=0.80
            ))
            return scenes

        # Gather evidence lists
        speech_text = " ".join([n.value for n in getattr(evidence, "speech", [])])
        yolo_objects = [n.value for n in getattr(evidence, "vision", []) if getattr(n, "source", "") == "YOLO"]
        clip_scenes = [n.value for n in getattr(evidence, "vision", []) if getattr(n, "source", "") == "CLIP"]
        actions = [n.value for n in getattr(evidence, "actions", [])]
        audio_events = [n.value for n in getattr(evidence, "audio", [])]

        num_keyframes = len(keyframes)
        for idx, kf in enumerate(keyframes):
            t_start = kf["timestamp"]
            t_end = keyframes[idx+1]["timestamp"] if idx < num_keyframes - 1 else duration
            seg_duration = round(max(0.1, t_end - t_start), 2)
            
            scene_id = f"scene_{idx:03d}"
            
            # Divide transcript or objects per scene slice if available
            scene_objects = yolo_objects if idx == 0 else list(set(yolo_objects))[:3]
            scene_env = clip_scenes[idx % len(clip_scenes)] if clip_scenes else "Indoor/Outdoor Scene"
            
            scenes.append(SceneSegment(
                scene_id=scene_id,
                timestamp_start=t_start,
                timestamp_end=t_end,
                duration=seg_duration,
                keyframes=[kf.get("image_path", "")],
                transcript=speech_text if idx == 0 else "",  # Main transcript attached to primary scene
                objects=scene_objects,
                actions=actions[:2],
                environment=scene_env,
                audio_events=audio_events[:2],
                confidence=round(kf.get("difference_score", 0.85), 3)
            ))

        return scenes

    def scenes_to_nodes(self, scenes: List[SceneSegment]) -> List[GraphNode]:
        """Converts SceneSegment instances into GraphNode schemas for NetworkX storage."""
        nodes = []
        for sc in scenes:
            nodes.append(GraphNode(
                id=sc.scene_id,
                name=f"Scene [{sc.timestamp_start:.1f}s - {sc.timestamp_end:.1f}s]",
                type="Scene",
                properties={
                    "timestamp_start": sc.timestamp_start,
                    "timestamp_end": sc.timestamp_end,
                    "duration": sc.duration,
                    "environment": sc.environment,
                    "objects_count": len(sc.objects),
                    "actions_count": len(sc.actions)
                },
                confidence=sc.confidence,
                source="SceneSegmenter",
                timestamp=sc.timestamp_start
            ))
        return nodes
