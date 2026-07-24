import time
from typing import Dict, Any

# Package imports
from src.semantic_knowledge.scene_graph import SceneGraphBuilder
from src.semantic_knowledge.entity_extractor import MultimodalEntityExtractor
from src.semantic_knowledge.relationship_builder import RelationshipBuilder
from src.semantic_knowledge.ontology import DomainOntology
from src.semantic_knowledge.reasoning import SemanticReasoningEngine
from src.semantic_knowledge.graph_storage import NetworkXGraphStorage
from src.semantic_knowledge.graph_queries import GraphQueryEngine
from src.semantic_knowledge.metadata_view import MetadataViewProjection
from src.semantic_knowledge.graph_embeddings import GraphEmbeddingBuilder
from src.semantic_knowledge.evaluation import GraphEvaluator

# Foundation orchestrator import
from src.video_intelligence.orchestrator import VideoIntelligenceOrchestrator

class SemanticKnowledgeEngine:
    """The flagship Semantic Knowledge Engine (SKE) transforming videos into structured Knowledge Graphs."""

    def __init__(self):
        self.vie_orchestrator = VideoIntelligenceOrchestrator()
        self.scene_builder = SceneGraphBuilder()
        self.entity_extractor = MultimodalEntityExtractor()
        self.relationship_builder = RelationshipBuilder()
        self.ontology = DomainOntology()
        self.reasoner = SemanticReasoningEngine()
        self.storage = NetworkXGraphStorage()
        self.query_engine = GraphQueryEngine()
        self.metadata_projection = MetadataViewProjection()
        self.embedding_builder = GraphEmbeddingBuilder()
        self.evaluator = GraphEvaluator()

    def process_video_to_knowledge_graph(self, video_path: str, video_id: str) -> Dict[str, Any]:
        """
        Executes the end-to-end Semantic Knowledge Engine pipeline:
        Video -> Scene Graph -> Entity Extractor -> Relationship Builder -> Ontology -> Semantic Reasoning 
        -> NetworkX Storage -> Graph Queries -> Metadata View -> Graph Embeddings -> Evaluation Metrics.
        """
        print(f"[SKE-Engine] Initiating Semantic Knowledge Engine processing for: {video_id}")
        t_start = time.time()

        # Step 0: Execute underlying Multimodal Sensor Pipeline & Preprocessing
        vie_result = self.vie_orchestrator.process_video(video_path, video_id)
        raw_vlm_data = vie_result["metadata"]
        evidence = vie_result.get("evidence", self.vie_orchestrator.preprocessor)

        # Re-extract keyframe metadata and duration from prep data
        prep_data = self.vie_orchestrator.preprocessor.process(video_path, video_id)
        keyframes = prep_data["frames"]
        duration = vie_result["hierarchy"].get("duration", 15.0)

        # Step 1: Scene Segmentation
        scenes = self.scene_builder.build_scenes(keyframes, duration, evidence)
        scene_nodes = self.scene_builder.scenes_to_nodes(scenes)

        # Step 2: Entity Extraction (across 14 categories)
        entity_nodes = self.entity_extractor.extract_entities(scenes, raw_vlm_data, evidence)

        # Combine Scene & Entity Nodes
        all_initial_nodes = scene_nodes + entity_nodes

        # Step 3 & 4: Relationship Extraction & Temporal Knowledge Sequencing
        relationships = self.relationship_builder.build_relationships(all_initial_nodes, scenes, raw_vlm_data)

        # Step 6: Ontology Application (IS_A hierarchy)
        parent_nodes, is_a_edges = self.ontology.apply_ontology(all_initial_nodes)

        # Combine with parent nodes & edges
        all_nodes = all_initial_nodes + parent_nodes
        all_edges = relationships + is_a_edges

        # Step 7: Semantic Reasoning (Infer unobserved concepts with evidence citations)
        inferred_nodes, inferred_edges = self.reasoner.infer_concepts(all_nodes, all_edges)

        final_nodes = all_nodes + inferred_nodes
        final_edges = all_edges + inferred_edges

        # Step 8: NetworkX Graph Storage & Serialization
        G, graph_file_path = self.storage.create_graph(video_id, duration, final_nodes, final_edges, scenes)

        # Step 9: Graph Queries (Sample Query Traversals)
        temporal_seq = self.query_engine.find_temporal_sequence(G)
        people_rel = self.query_engine.find_people_to_place_relationships(G)

        # Step 10: Derived Metadata View Projection
        metadata_view = self.metadata_projection.project_metadata(G, raw_vlm_data)

        # Step 11: Graph Vector Embedding Generation (MiniLM)
        embedding_text, embedding_vector = self.embedding_builder.generate_vector(G)

        # Step 12: Graph Quality Metric Evaluation
        evaluation_metrics = self.evaluator.evaluate_graph(G)

        total_duration = round(time.time() - t_start, 2)
        print(f"[SKE-Engine] Successfully constructed Semantic Knowledge Graph for {video_id} in {total_duration}s")

        return {
            "video_id": video_id,
            "video_path": video_path,
            "evidence": evidence,
            "graph_summary": {
                "node_count": G.number_of_nodes(),
                "edge_count": G.number_of_edges(),
                "scene_count": len(scenes),
                "rdf_triples_count": len(self.storage.to_rdf_triples(G)),
                "storage_path": graph_file_path
            },
            "metadata": metadata_view.dict(),
            "embedding_text": embedding_text,
            "embedding": embedding_vector,
            "queries": {
                "temporal_sequence": temporal_seq.sequence,
                "people_place_edge_count": people_rel.count
            },
            "metrics": evaluation_metrics.dict(),
            "execution_time_sec": total_duration
        }
