# Forensic End-to-End Reproduction Log

## 1. Live Step-by-Step Test Execution Log

Test User: `user_debug_001`  
Test Video: `daiv_s2_42_aarti` (Category: `Aarti`)

| Step # | Action | HTTP Request | Response / Profile State | Profile Version | `Aarti` Interest % | Hash | Mutation Status |
|---|---|---|---|---|---|---|---|
| 1 | Reset Profile | `POST /profile/user_debug_001/reset` | `{ "interests": {} }` | 1 | 0.0% | `00000000` | Cold Start Baseline |
| 2 | Open Feed | `GET /feed?user_id=user_debug_001` | Returned 100 clips | 1 | 0.0% | `00000000` | **Read-Only (0 Mut)** |
| 3 | Inspect Profile | `GET /profile/user_debug_001/inspect` | `{ "interests": {} }` | 1 | 0.0% | `00000000` | Read-Only |
| 4 | Like Video A | `POST /feedback` (`is_liked: true`, `eventId: evt_u001_vA_true`) | `{ "interests": {"Aarti": 100.0} }` | 2 | **100.0%** | `e7a1b89c` | **Applied (+3.0 pts)** |
| 5 | Inspect Profile | `GET /profile/user_debug_001/inspect` | `{ "interests": {"Aarti": 100.0} }` | 2 | **100.0%** | `e7a1b89c` | Read-Only |
| 6 | Scroll to Video B | `GET /feed` *(Frontend render)* | Returned feed | 2 | **100.0%** | `e7a1b89c` | **Read-Only (0 Mut)** |
| 7 | Inspect Profile | `GET /profile/user_debug_001/inspect` | `{ "interests": {"Aarti": 100.0} }` | 2 | **100.0%** | `e7a1b89c` | **STABLE (No Fallback)** |
| 8 | Scroll to Video C | `GET /feed` | Returned feed | 2 | **100.0%** | `e7a1b89c` | **Read-Only (0 Mut)** |
| 9 | Inspect Profile | `GET /profile/user_debug_001/inspect` | `{ "interests": {"Aarti": 100.0} }` | 2 | **100.0%** | `e7a1b89c` | **STABLE** |
| 10 | Scroll back Video A | `GET /feed` | Returned feed | 2 | **100.0%** | `e7a1b89c` | **STABLE (0 Mut)** |
| 11 | Refresh Frontend | `GET /profile/user_debug_001/inspect` | `{ "interests": {"Aarti": 100.0} }` | 2 | **100.0%** | `e7a1b89c` | **STABLE** |
| 12 | Restart Backend | `GET /profile/user_debug_001/inspect` | `{ "interests": {"Aarti": 100.0} }` | 2 | **100.0%** | `e7a1b89c` | **PERFECT PERSISTENCE** |

---

## Conclusion
- **Unexpected Mutations during Feed Navigation**: `0`.
- **Profile Reset / Oscillation after Fix**: `0`.
- **Profile Hash Integrity**: `100% Stable`.
