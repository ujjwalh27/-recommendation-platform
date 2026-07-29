"""
Task 8 – Comparative Benchmark Harness
Compares retrieval quality Before Integration (description embeddings) vs After Integration (CMREE canonical embeddings).
"""

import time
from typing import List, Dict, Any, Tuple, Set
import numpy as np
from semantic_indexing.evaluation.retrieval_metrics import RetrievalMetricsCalculator


class ComparativeRetrievalBenchmark:
    """Benchmark harness evaluating Before vs After semantic indexing."""

    def __init__(self):
        self.metrics = RetrievalMetricsCalculator()

    def run_comparative_benchmark(
        self,
        test_queries: List[Dict[str, Any]],
        before_search_fn,
        after_search_fn,
        k: int = 10
    ) -> Dict[str, Any]:
        """
        Runs side-by-side comparative retrieval evaluation.
        test_queries list elements: {"query_id": str, "relevant_set": set, "query_vector": np.ndarray}
        """
        before_precisions, after_precisions = [], []
        before_recalls, after_recalls = [], []
        before_mrrs, after_mrrs = [], []
        before_ndcgs, after_ndcgs = [], []
        before_latencies, after_latencies = [], []

        for q in test_queries:
            qid = q["query_id"]
            relevant = q["relevant_ids"]

            # 1. Before Integration Run
            t0 = time.time()
            res_before = before_search_fn(qid, top_k=k)
            t_before = (time.time() - t0) * 1000.0
            ids_before = [r["video_id"] for r in res_before]

            before_precisions.append(self.metrics.precision_at_k(ids_before, relevant, k))
            before_recalls.append(self.metrics.recall_at_k(ids_before, relevant, k))
            before_mrrs.append(self.metrics.mean_reciprocal_rank(ids_before, relevant))
            before_ndcgs.append(self.metrics.ndcg_at_k(ids_before, relevant, k))
            before_latencies.append(t_before)

            # 2. After Integration Run
            t0 = time.time()
            res_after = after_search_fn(qid, top_k=k)
            t_after = (time.time() - t0) * 1000.0
            ids_after = [r["video_id"] for r in res_after]

            after_precisions.append(self.metrics.precision_at_k(ids_after, relevant, k))
            after_recalls.append(self.metrics.recall_at_k(ids_after, relevant, k))
            after_mrrs.append(self.metrics.mean_reciprocal_rank(ids_after, relevant))
            after_ndcgs.append(self.metrics.ndcg_at_k(ids_after, relevant, k))
            after_latencies.append(t_after)

        return {
            "before_integration": {
                "precision_at_k": round(float(np.mean(before_precisions)), 4),
                "recall_at_k": round(float(np.mean(before_recalls)), 4),
                "mrr": round(float(np.mean(before_mrrs)), 4),
                "ndcg_at_k": round(float(np.mean(before_ndcgs)), 4),
                "latency_ms": round(float(np.mean(before_latencies)), 2)
            },
            "after_integration": {
                "precision_at_k": round(float(np.mean(after_precisions)), 4),
                "recall_at_k": round(float(np.mean(after_recalls)), 4),
                "mrr": round(float(np.mean(after_mrrs)), 4),
                "ndcg_at_k": round(float(np.mean(after_ndcgs)), 4),
                "latency_ms": round(float(np.mean(after_latencies)), 2)
            }
        }
