# Behavioral Specification of Daiv Recommendation Engine

## 1. Profile State Architecture

| Field | Source / Origin | Type | Default / Baseline | Bounds | Mutable |
|---|---|---|---|---|---|
| `category_interests` | L1 Normalization of `raw_scores` | `Dict[str, float]` | Aarti: 40.0%, Pooja: 35.0%, Abhishekam: 25.0% | $[0.0, 100.0]$ | Yes |
| `deity_interests` | Derived from deity interaction deltas | `Dict[str, float]` | Shiva: 45.0%, Krishna: 35.0%, Vishnu: 20.0% | $[0.0, 100.0]$ | Yes |
| `ritual_interests` | Derived from ritual interaction deltas | `Dict[str, float]` | Aarti: 40.0%, Pooja: 35.0%, Abhishekam: 25.0% | $[0.0, 100.0]$ | Yes |
| `creator_affinities` | Accumulated creator interaction points | `Dict[str, float]` | Empty `{}` | $[0.0, \infty)$ | Yes |
| `raw_scores` | Unnormalized category raw points | `Dict[str, float]` | Aarti: 40.0, Pooja: 35.0, Abhishekam: 25.0 | $[0.0, \infty)$ | Yes |
| `watch_history` | Sequence of watched video sessions | `List[Dict]` | `[]` | Unlimited | Yes |
| `version` | Monotonically increasing counter | `int` | `1` | $[1, \infty)$ | Yes |
| `last_event_id` | String ID of most recent applied event | `str` | `None` | String | Yes |

## 2. Recommendation Signals & Formulas

| Signal Name | Class | Weight | Source Field | Calculation Formula | Bounds | Gating / Threshold | Higher Better | Negative Allowed |
|---|---|---|---|---|---|---|---|---|
| `interest` | `InterestSignal` | 0.35 | `user_profile.interests`, `deity_interests`, `ritual_interests` | $\min(1.0, rac{\max(	ext{cat}, 	ext{fam}, 	ext{rit}) + 	ext{deity\_boost} + 	ext{family\_boost}}{100.0})$ | $[0.0, 1.0]$ | Category Interest Gate ($\le 1.5\% ightarrow 0.0$) | Yes | No |
| `creator_affinity` | `CreatorAffinitySignal` | 0.20 | `user_profile.creator_affinities` | $\min(1.0, rac{	ext{affinity\_score}}{10.0})$ | $[0.0, 1.0]$ | None | Yes | No |
| `similarity` | `SimilaritySignal` | 0.15 | `candidate.similarity_score` | `float(cand.similarity_score)` | $[0.0, 1.0]$ | None | Yes | No |
| `collaborative_filtering` | `CollaborativeFilteringSignal` | 0.10 | `candidate.cf_score` | `float(cand.cf_score)` | $[0.0, 1.0]$ | None | Yes | No |
| `popularity` | `PopularitySignal` | 0.10 | `engagement_rate`, `views`, `created_time` | If age < 30d: 0.8 else $0.7 \cdot \min(1, rac{	ext{er}}{0.15}) + 0.3 \cdot \min(1, rac{\ln(1+	ext{views})}{18})$ | $[0.0, 1.0]$ | None | Yes | No |
| `freshness` | `FreshnessSignal` | 0.05 | `created_time` | $\exp(-0.0231 \cdot 	ext{age\_days})$ | $[0.0, 1.0]$ | If missing: 0.5 | Yes | No |
| `exploration` | `RandomExplorationSignal` | 0.05 | Pseudorandom generator | $	ext{random.random()} \cdot 0.1$ | $[0.0, 0.1]$ | None | N/A | No |

## 3. Explicit Button Weight Scale

- `LIKE`: $+1.5$ raw points
- `SAVE`: $+1.5$ raw points
- `SHARE`: $+1.5$ raw points
- `COMMENT`: $+1.0$ raw points
- `UNLIKE`: $-1.5$ raw points (exact score reversion)
- `UNSAVE`: $-1.5$ raw points (exact score reversion)
