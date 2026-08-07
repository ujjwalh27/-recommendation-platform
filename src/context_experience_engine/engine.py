from typing import Dict, Any, Optional
from .rule_engine import CEEERuleEngine
from .perceptual_layer import PerceptualMetadataEnricher
from .emotional_layer import EmotionalMetadataEnricher
from .semantic_document_builder import SemanticDocumentBuilder
from .signal_fusion.fusion_engine import MultimodalSignalFusionEngine
from .evidence_graph.graph import EvidenceGraphBuilder
from .provenance.trace_generator import ReasoningTraceGenerator


class ContextExperienceEnrichmentEngine:
    """
    Multimodal Signal Fusion & Advanced Context Reasoning Engine (MSFACR / CEEE v2.0).
    Aggregates structured signals across 7 perception models (MiniCPM, YOLO, VideoMAE, Whisper, AST, OCR, CLIP),
    builds unified Evidence Documents and Evidence Graphs, evaluates multimodal rules, calculates dynamic weighted
    confidence scores, generates human-readable reasoning traces, and synthesizes enriched semantic documents for vector embeddings.
    """

    def __init__(self, rules_dir: Optional[str] = None):
        self.fusion_engine = MultimodalSignalFusionEngine()
        self.rule_engine = CEEERuleEngine(rules_dir=rules_dir)
        self.perceptual_layer = PerceptualMetadataEnricher(self.rule_engine)
        self.emotional_layer = EmotionalMetadataEnricher(self.rule_engine)
        self.graph_builder = EvidenceGraphBuilder()
        self.trace_generator = ReasoningTraceGenerator()
        self.doc_builder = SemanticDocumentBuilder()

    def enrich(
        self,
        observation: Dict[str, Any],
        canonical_metadata: Dict[str, Any],
        raw_report: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Main execution pipeline:
        1. Multimodal Signal Fusion -> Evidence Document
        2. Infer Layer 2 Perceptual Metadata
        3. Infer Layer 3 Emotional Metadata
        4. Construct Evidence Graph (DAG)
        5. Generate Reasoning Traces & Provenance
        6. Synthesize Upgraded Semantic Document for Vector Search
        """
        raw_report = raw_report or {}
        metadata = raw_report.get("metadata", {})

        # Step 1: Multimodal Signal Fusion
        fusion_output = self.fusion_engine.process(observation, canonical_metadata, raw_report)
        evidence_doc = fusion_output["evidence_document"]

        # Step 2: Layer 2 Perceptual Metadata Inference
        perceptual_meta = self.perceptual_layer.enrich(evidence_doc, canonical_metadata)

        # Step 3: Layer 3 Emotional Metadata Inference
        emotional_meta = self.emotional_layer.enrich(evidence_doc, canonical_metadata)

        # Step 4: Evidence Graph Construction (DAG)
        evidence_graph = self.graph_builder.build_graph(evidence_doc, perceptual_meta, emotional_meta)

        # Step 5: Human-readable Reasoning Traces & Provenance Generation
        reasoning_traces = self.trace_generator.generate_traces(perceptual_meta, emotional_meta)

        # Step 6: Upgraded Semantic Document Synthesis
        embedding_text = self.doc_builder.build_document(
            canonical_metadata=canonical_metadata,
            perceptual_metadata=perceptual_meta,
            emotional_metadata=emotional_meta,
            evidence_doc=evidence_doc,
            raw_summary=metadata.get("summary", ""),
            title=metadata.get("title", "")
        )

        ceee_metadata = {
            "perceptual_metadata": perceptual_meta,
            "emotional_metadata": emotional_meta,
            "evidence_document": evidence_doc,
            "evidence_graph": evidence_graph,
            "reasoning_traces": reasoning_traces,
            "engine_version": "2.0-msfacr-signal-fusion",
            "explainability": {
                "perceptual_fields_count": len(perceptual_meta),
                "emotional_fields_count": len(emotional_meta),
                "active_models_count": len(fusion_output.get("active_models", [])),
                "evidence_graph_nodes": evidence_graph.get("graph_metadata", {}).get("total_nodes", 0),
                "evidence_graph_edges": evidence_graph.get("graph_metadata", {}).get("total_edges", 0),
                "fusion_status": "MULTIMODAL_SIGNALS_FUSED"
            }
        }

        return {
            "perceptual_metadata": perceptual_meta,
            "emotional_metadata": emotional_meta,
            "evidence_document": evidence_doc,
            "evidence_graph": evidence_graph,
            "reasoning_traces": reasoning_traces,
            "ceee_metadata": ceee_metadata,
            "embedding_text": embedding_text
        }
