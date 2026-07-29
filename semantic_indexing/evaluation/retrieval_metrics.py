"""
Task 8 – Retrieval Metrics Calculator
Calculates Precision@K, Recall@K, MRR, NDCG@K, Latency, Duplicate Rate, and Semantic Diversity.
"""

import math
from typing import List, Dict, Any, Set


class RetrievalMetricsCalculator:
    """Calculates objective retrieval metrics for candidate evaluation."""

    @staticmethod
    def precision_at_k(retrieved: List[str], relevant: Set[str], k: int = 10) -> float:
        retrieved_k = retrieved[:k]
        if not retrieved_k:
            return 0.0
        hits = len(set(retrieved_k).intersection(relevant))
        return hits / len(retrieved_k)

    @staticmethod
    def recall_at_k(retrieved: List[str], relevant: Set[str], k: int = 10) -> float:
        if not relevant:
            return 0.0
        retrieved_k = retrieved[:k]
        hits = len(set(retrieved_k).intersection(relevant))
        return hits / len(relevant)

    @staticmethod
    def mean_reciprocal_rank(retrieved: List[str], relevant: Set[str]) -> float:
        for idx, item in enumerate(retrieved, start=1):
            if item in relevant:
                return 1.0 / idx
        return 0.0

    @staticmethod
    def ndcg_at_k(retrieved: List[str], relevant: Set[str], k: int = 10) -> float:
        retrieved_k = retrieved[:k]
        dcg = 0.0
        for i, item in enumerate(retrieved_k, start=1):
            rel = 1.0 if item in relevant else 0.0
            dcg += rel / math.log2(i + 1)

        # Ideal DCG
        ideal_hits = min(len(relevant), k)
        idcg = sum(1.0 / math.log2(i + 1) for i in range(1, ideal_hits + 1))
        return dcg / idcg if idcg > 0 else 0.0

    @staticmethod
    def duplicate_candidate_rate(retrieved: List[str]) -> float:
        if not retrieved:
            return 0.0
        duplicates = len(retrieved) - len(set(retrieved))
        return duplicates / len(retrieved)

    @staticmethod
    def semantic_diversity_score(categories: List[str]) -> float:
        """Measures category entropy across retrieved candidates."""
        if not categories:
            return 0.0
        total = len(categories)
        counts = {}
        for cat in categories:
            counts[cat] = counts.get(cat, 0) + 1
        entropy = -sum((cnt / total) * math.log2(cnt / total) for cnt in counts.values())
        return round(entropy, 4)
