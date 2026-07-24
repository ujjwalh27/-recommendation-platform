import time
from typing import Dict, Any, List

from src.explainable_reasoning.claim_layer import ClaimLayer
from src.explainable_reasoning.hypotheses_engine import HypothesesEngine
from src.explainable_reasoning.conflict_resolver import ConflictResolver
from src.explainable_reasoning.episode_engine import EpisodeEngine
from src.explainable_reasoning.semantic_memory import SemanticMemory
from src.explainable_reasoning.xai_engine import XAIQueryEngine
from src.semantic_knowledge.graph_builder import SemanticKnowledgeEngine

class ExplainableReasoningEngine:
    """The flagship Phase 5 Explainable AI Reasoning Engine."""

    def __init__(self):
        self.ske_engine = SemanticKnowledgeEngine()
        self.claim_layer = ClaimLayer()
        self.hypotheses_engine = HypothesesEngine()
        self.conflict_resolver = ConflictResolver()
        self.episode_engine = EpisodeEngine()
        self.semantic_memory = SemanticMemory()
        self.xai_engine = XAIQueryEngine()

    def process_video_with_explainability(self, video_path: str, video_id: str) -> Dict[str, Any]:
        """
        Executes end-to-end Explainable AI reasoning pipeline over SKE Knowledge Graphs.
        """
        print(f"[XAI-Engine] Initiating Explainable AI Reasoning for: {video_id}")
        t_start = time.time()

        # Step 0: Execute SKE Knowledge Graph Builder
        ske_result = self.ske_engine.process_video_to_knowledge_graph(video_path, video_id)
        metadata = ske_result["metadata"]
        evidence_obj = ske_result.get("evidence", self.ske_engine.vie_orchestrator.preprocessor)

        # Step 1 & 2: Claims Layer & Evidence Traceability
        claims = self.claim_layer.build_claims(ske_result, metadata, evidence_obj)

        # Step 3: Multiple Hypotheses Generation & Ranking
        hypotheses = self.hypotheses_engine.generate_hypotheses(claims, metadata)

        # Step 4: Multi-Modal Conflict Resolution
        conflicts = self.conflict_resolver.resolve_conflicts(evidence_obj, metadata)

        # Step 5: Episode Timeline Aggregation
        scenes_raw = ske_result.get("scenes", [])
        episodes = self.episode_engine.build_episodes(scenes_raw, metadata)

        # Step 6: Semantic Memory Accumulation
        self.semantic_memory.update_memory(metadata.get("category", "General"), metadata.get("keywords", []))

        # Sample Interactive XAI Queries
        sample_q1 = self.xai_engine.answer_query("Why was this classified as Devotional?", claims, hypotheses, conflicts, metadata)
        sample_q2 = self.xai_engine.answer_query("How would decision change if speech evidence were unavailable?", claims, hypotheses, conflicts, metadata)

        total_time = round(time.time() - t_start, 2)
        print(f"[XAI-Engine] Completed Explainable AI Reasoning in {total_time}s")

        return {
            "video_id": video_id,
            "video_path": video_path,
            "claims": [c.dict() for c in claims],
            "hypotheses": [h.dict() for h in hypotheses],
            "conflicts": [c.dict() for c in conflicts],
            "episodes": [e.dict() for e in episodes],
            "knowledge_graph_summary": ske_result["graph_summary"],
            "metadata_view": metadata,
            "embedding_text": ske_result["embedding_text"],
            "embedding_vector": ske_result["embedding"],
            "sample_xai_answers": {
                "why_classified": sample_q1.dict(),
                "counterfactual_speech": sample_q2.dict()
            },
            "metrics": ske_result["metrics"],
            "execution_time_sec": total_time
        }
