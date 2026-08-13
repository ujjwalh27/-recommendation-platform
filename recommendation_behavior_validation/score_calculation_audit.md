# Score Calculation Audit & Formula Verification

## Candidate Signal Breakdown
- `interest`: 0.4000 (Weight: 0.35)
- `creator_affinity`: 0.5000 (Weight: 0.2)
- `similarity`: 0.8500 (Weight: 0.15)
- `collaborative_filtering`: 0.5000 (Weight: 0.1)
- `popularity`: 0.8000 (Weight: 0.1)
- `freshness`: 0.9772 (Weight: 0.05)
- `exploration`: 0.0225 (Weight: 0.05)

## Numerical Accuracy Audit
- **Calculated Expected Score**: `0.547500`
- **Actual Recommendation Score**: `0.547500`
- **Absolute Error**: `0.0000000000`
- **Tolerance Goal ($\le 10^-6$)**: `PASS`
