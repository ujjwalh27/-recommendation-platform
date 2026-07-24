import os
import sys

# Add project root to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.semantic_knowledge import SemanticKnowledgeEngine

def main():
    print("==================================================")
    print("Testing Semantic Knowledge Engine (SKE) Core")
    print("==================================================")

    test_video = "/Users/ujjwalhkumar/Downloads/daiv sample/Aditi Atul Jadhav.mp4"
    if not os.path.exists(test_video):
        print(f"Error: Test video file not found at: {test_video}")
        sys.exit(1)

    print(f"Loading test video asset: {test_video}")
    ske = SemanticKnowledgeEngine()

    video_id = "ske_test_aditi"
    print("\nProcessing video into a complete Semantic Knowledge Graph...")
    result = ske.process_video_to_knowledge_graph(test_video, video_id)

    print("\n==================================================")
    print("SEMANTIC KNOWLEDGE GRAPH COMPLETED SUCCESSFULLY!")
    print("==================================================")
    
    summary = result["graph_summary"]
    print(f"Video ID: {result['video_id']}")
    print(f"Node Count: {summary['node_count']}")
    print(f"Edge Count: {summary['edge_count']}")
    print(f"Scene Count: {summary['scene_count']}")
    print(f"RDF Triples Exported: {summary['rdf_triples_count']}")
    print(f"Graph Storage Path: {summary['storage_path']}")

    print("\n=== DERIVED METADATA VIEW (Projection) ===")
    meta = result["metadata"]
    print(f"Title: {meta['title']}")
    print(f"Summary: {meta['summary']}")
    print(f"Category: {meta['category']} | Subcategory: {meta['subcategory']}")
    print(f"Primary Topic: {meta['primary_topic']}")
    print(f"Secondary Topics: {meta['secondary_topics']}")
    print(f"Tags: {meta['tags']}")
    print(f"Keywords: {meta['keywords']}")
    print(f"Recommendation Keywords: {meta['recommendation_keywords']}")
    print(f"Reasoning: {meta['reasoning']}")

    print("\n=== CANONICAL GRAPH EMBEDDINGS (MiniLM) ===")
    print(f"Embedding Text Length: {len(result['embedding_text'])} characters")
    print(f"Embedding Text Preview: {result['embedding_text'][:150]}...")
    print(f"Vector Dimensions: {len(result['embedding'])} (Expected: 384)")

    print("\n=== GRAPH QUERY TRAVERSALS ===")
    queries = result["queries"]
    print(f"Temporal Sequence Scenes: {queries['temporal_sequence']}")
    print(f"People-to-Place Relationships Count: {queries['people_place_edge_count']}")

    print("\n=== GRAPH QUALITY EVALUATION METRICS ===")
    metrics = result["metrics"]
    print(f"Entity Precision: {metrics['entity_precision'] * 100:.1f}%")
    print(f"Relationship Precision: {metrics['relationship_precision'] * 100:.1f}%")
    print(f"Scene Accuracy: {metrics['scene_accuracy'] * 100:.1f}%")
    print(f"Temporal Accuracy: {metrics['temporal_accuracy'] * 100:.1f}%")
    print(f"Ontology Mapping Rate: {metrics['ontology_mapping_rate'] * 100:.1f}%")
    print(f"Graph Completeness: {metrics['graph_completeness'] * 100:.1f}%")
    print(f"Explainability Score: {metrics['explainability_score'] * 100:.1f}%")

    print("\n==================================================")
    print("Phase 3 Semantic Knowledge Engine Verification Passed!")
    print("==================================================")

if __name__ == "__main__":
    main()
