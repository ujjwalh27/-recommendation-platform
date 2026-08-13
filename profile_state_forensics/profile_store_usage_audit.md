# Forensic ProfileStore Usage & Mapping Audit

Mapping of all occurrences of interest vectors, profiles, and user state objects across the system.

| Code File | Component Class / Function | Usage Type | Classified Category | Source of Truth |
|---|---|---|---|---|
| `src/recommender/profile_store.py` | `UserInterestProfileStore` | Core Store Initialization & Mutations | **INITIALIZATION / WRITE** | Authoritative Single Source of Truth |
| `src/recommender/service.py` | `RecommenderService.__init__` | Instantiates `self.profile_store` | **INITIALIZATION** | References `UserInterestProfileStore` |
| `src/recommender/service.py` | `get_recommendations()` | Retrieves profile copy via `profile_store.get_profile()` | **READ** | Read-Only Snapshot |
| `src/recommender/service.py` | `submit_feedback()` | Delegates event to `profile_store.process_event()` | **WRITE** | Single Writer Delegation |
| `src/recommender/service.py` | `reset_user_profile()` | Delegates reset to `profile_store.reset_profile()` | **WRITE** | Single Writer Delegation |
| `src/candidate_generation/candidate_generator.py` | `generate()` | Consumes interest vector for candidate retrieval | **READ** | Read-Only View |
| `src/ranking/scorer.py` | `calculate_candidate_score()` | Consumes interest vector for candidate scoring | **READ** | Read-Only View |
| `backend/app.py` | `get_user_profile()` | Calls `service.interest_profiles` property | **READ** | Delegates to `profile_store.profiles` |
| `backend/app.py` | `inspect_user_profile()` | Calls `service.profile_store.get_profile()` | **READ** | Direct Read-Only Inspection |

---

## Single Runtime Profile Object Verification
- Shadowing instances found: **0**.
- Legacy in-memory profile dictionaries: **0**.
- Duplicate profile stores instantiated: **0** (Shared instance in `service.py`).
