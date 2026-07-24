from typing import List, Dict, Any
from src.explainable_reasoning.schemas import EpisodeSegment

class EpisodeEngine:
    """Handles Part 5: Episode Reasoning & Scene Aggregation."""

    def build_episodes(self, scenes: List[Any], metadata: Dict[str, Any]) -> List[EpisodeSegment]:
        """
        Groups individual scenes into higher-level thematic narrative Episodes.
        """
        episodes: List[EpisodeSegment] = []
        if not scenes:
            return episodes

        total_scenes = len(scenes)
        mid = total_scenes // 2

        topic = metadata.get("primary_topic", "Video Event")
        cat = metadata.get("category", "General")

        if total_scenes <= 3:
            # Single main episode
            episodes.append(EpisodeSegment(
                episode_id="ep_001_main",
                title=f"Complete Episode: {topic}",
                scene_ids=[s.get("scene_id", f"scene_{idx}") for idx, s in enumerate(scenes)],
                timestamp_start=scenes[0].get("timestamp_start", 0.0),
                timestamp_end=scenes[-1].get("timestamp_end", 60.0),
                narrative_summary=f"Unified narrative episode covering {topic} within {cat} domain."
            ))
        else:
            # Episode 1: Introduction & Preparation
            sc1 = scenes[:mid]
            episodes.append(EpisodeSegment(
                episode_id="ep_001_intro_prep",
                title=f"Episode 1: Introduction & Preparation ({topic})",
                scene_ids=[s.get("scene_id", f"scene_{idx}") for idx, s in enumerate(sc1)],
                timestamp_start=sc1[0].get("timestamp_start", 0.0),
                timestamp_end=sc1[-1].get("timestamp_end", 30.0),
                narrative_summary=f"Initial setup, ambient introduction, and preliminary actions for {topic}."
            ))

            # Episode 2: Main Activity & Conclusion
            sc2 = scenes[mid:]
            episodes.append(EpisodeSegment(
                episode_id="ep_002_core_conclusion",
                title=f"Episode 2: Core Execution & Conclusion ({topic})",
                scene_ids=[s.get("scene_id", f"scene_{idx}") for idx, s in enumerate(sc2)],
                timestamp_start=sc2[0].get("timestamp_start", 30.0),
                timestamp_end=sc2[-1].get("timestamp_end", 60.0),
                narrative_summary=f"Main performance, primary demonstration, and concluding remarks for {topic}."
            ))

        return episodes
