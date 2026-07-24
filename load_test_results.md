# Production Load Testing Results

## Performance vs Concurrency Curve

| Concurrent Users | Avg Latency (s) | P95 Latency (s) | P99 Latency (s) | Throughput (QPS) | CPU Load (%) | RAM Usage | Failure Rate |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1 User** | 18.2s | 19.5s | 20.8s | 0.055 | 24.5% | 4.2 GB | **0.0%** |
| **5 Users** | 19.4s | 22.1s | 24.5s | 0.258 | 48.2% | 5.1 GB | **0.0%** |
| **10 Users** | 21.8s | 26.4s | 31.0s | 0.458 | 74.0% | 5.8 GB | **0.0%** |
| **25 Users** | 28.5s | 38.2s | 46.1s | **0.877** | 88.5% | 6.9 GB | **0.0%** |
| **50 Users** | 44.2s | 62.0s | 78.5s | 1.130 | 96.2% | 7.8 GB | 0.4% |
| **100 Users** | 89.5s | 125.0s | 160.0s | 1.117 | 99.8% | 8.4 GB | 3.2% |

## Maximum Sustainable Throughput
- **Optimal Operating Range**: Up to **25 concurrent users** per node (0.877 QPS / ~3,150 videos/hour).
- **Hard Concurrency Limit**: Set queue limit to **35 concurrent requests** per instance.
