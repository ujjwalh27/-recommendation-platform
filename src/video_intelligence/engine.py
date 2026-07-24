import time
from typing import Dict, Any, List
from sentence_transformers import SentenceTransformer
from src.video_intelligence.orchestrator import VideoIntelligenceOrchestrator

class VideoIntelligenceEngine:
    """The production-grade entry point client-facing interface for the Video Intelligence Engine (VIE)."""

    def __init__(self):
        self.orchestrator = VideoIntelligenceOrchestrator()
        self._embedding_model = None

    @property
    def embedding_model(self) -> SentenceTransformer:
        if not self._embedding_model:
            print("[VIE-Engine] Loading SentenceTransformer 'all-MiniLM-L6-v2'...")
            self._embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        return self._embedding_model

    def analyze_video(self, video_path: str, video_id: str) -> Dict[str, Any]:
        """
        Processes a video file to generate explainable, confidence-scored semantic metadata
        and vector embeddings suitable for downstream recommendation systems.
        
        Returns:
            Dict representing the unified report containing metadata, graph structure, and vector embeddings.
        """
        # 1. Run the core pre-processing and reasoning orchestrator cascade
        result = self.orchestrator.process_video(video_path, video_id)
        
        metadata = result["metadata"]
        hierarchy = result["hierarchy"]
        report_path = result["validation_report_path"]

        # 2. Extract validated metadata to construct the semantic embedding text block
        # Only include fields with a confidence score above 0.50 to prevent noise injection
        validated_parts = []
        
        # Core fields
        for field in ["title", "summary", "category", "subcategory", "primary_topic", "mood", "emotion", "language"]:
            val = metadata.get(field, "")
            prov = metadata.get("confidence", {}).get(field)
            if val and prov:
                # If confidence is > 0.50, include it
                conf = prov.get("confidence", 0.0) if isinstance(prov, dict) else prov.confidence
                if conf >= 0.50:
                    validated_parts.append(str(val))

        # List fields
        for field in ["secondary_topics", "entities", "activities", "objects", "keywords", "recommendation_keywords"]:
            val_list = metadata.get(field, [])
            prov = metadata.get("confidence", {}).get(field)
            if val_list and prov:
                conf = prov.get("confidence", 0.0) if isinstance(prov, dict) else prov.confidence
                if conf >= 0.50:
                    validated_parts.extend([str(item) for item in val_list if item])

        # String-join all elements into a semantic context block
        embedding_text = " ".join(validated_parts)
        if not embedding_text.strip():
            # Fallback to simple title/summary
            embedding_text = f"{metadata.get('title', '')} {metadata.get('summary', '')}"

        # 3. Generate MiniLM Vector Embedding (Step 10 integration)
        t_embed_start = time.time()
        print("[VIE-Engine] Generating SentenceTransformer embeddings...")
        emb_vector = self.embedding_model.encode(embedding_text, normalize_embeddings=True)
        embed_time = round(time.time() - t_embed_start, 3)

        # 4. Construct the consolidated database record
        record = {
            "video_id": video_id,
            "video_path": video_path,
            "metadata": metadata,
            "hierarchy": hierarchy,
            "embedding_text": embedding_text,
            "embedding": emb_vector.tolist(),
            "validation_report_path": report_path,
            "metrics": {
                "total_execution_time_sec": result["execution_time_sec"],
                "vector_embedding_time_sec": embed_time
            }
        }
        
        return record
