# Forensic Report: Live Request Trace

## 1. End-to-End Request Flow for GET /feed

```text
Frontend (VideoFeed.jsx)
   │  GET /feed?user_id=user_1&limit=100
   ▼
Backend (backend/app.py: get_feed)
   │  Calls service.get_recommendations("user_1", limit=100)
   ▼
RecommenderService (src/recommender/service.py)
   │  Calls self.profile_store.get_profile("user_1") [READ-ONLY snapshot]
   ▼
UserInterestProfileStore (src/recommender/profile_store.py)
   │  Returns copy of profile (version, raw_scores, interests, creator_affinities)
   │  Logs [RECOMMENDATION_PROFILE_READ]
   ▼
CandidateGenerator & RuleBasedScorer
   │  Consumes read-only profile snapshot
   │  Computes match scores & ranks 100 candidate videos
   ▼
Response Payload
   │  Returns ranked feed list (200 OK)
   │  [MUTATION COUNT: 0 | VERSION CHANGE: 0]
```

---

## 2. End-to-End Request Flow for POST /feedback

```text
Frontend User Interaction (Click LIKE)
   │  handleLikeClick in VideoCard.jsx
   │  Constructs eventId: "evt_like_user_1_video_A_true"
   ▼
HTTP POST /feedback Payload:
   {
     "user_id": "user_1",
     "video_id": "video_A",
     "event_id": "evt_like_user_1_video_A_true",
     "watch_completion_rate": 0.5,
     "is_liked": true,
     "is_saved": false
   }
   ▼
Backend (backend/app.py: feedback)
   │  Calls service.submit_feedback(...)
   ▼
RecommenderService (src/recommender/service.py)
   │  Delegates to self.profile_store.process_event(...)
   ▼
UserInterestProfileStore (src/recommender/profile_store.py)
   │  Acquires RLock
   │  Checks idempotency (processed_event_ids)
   │  Calculates engagement score & category delta
   │  Applies 0.95 recency decay to inactive categories
   │  Updates raw_scores & calculates L1 normalized interests
   │  Increments version (v1 -> v2)
   │  Persists to datasets/processed/interest_profiles.json & interaction_events.json
   │  Logs [USER_PROFILE_UPDATE]
   │  Releases RLock
   ▼
HTTP Response (200 OK)
   {
     "status": "success",
     "user_id": "user_1",
     "version": 2,
     "interests": { "Aarti": 100.0 }
   }
```

---

## 3. End-to-End Trace of the Oscillation Defect

| Step | Action | Endpoint Called | `event_id` | Backend Version | Category Interest | Status |
|---|---|---|---|---|---|---|
| 1 | Open Feed | `GET /feed` | N/A | 1 | `{}` | Read-only |
| 2 | Click LIKE on Video A | `POST /feedback` | `evt_like_u1_vidA_true` | 2 | `Aarti: 100.0%` | Applied (+3.0 pts) |
| 3 | Read Profile | `GET /profile/user_1` | N/A | 2 | `Aarti: 100.0%` | Read-only |
| 4 | Scroll to Video B | `POST /feedback` *(Unmount)* | `evt_u1_vidA_true_false_0.05` *(Mismatch!)* | 3 | `{}` *(Cold Start)* | **DEFECT: Unintended Skip Penalty (-5.0 pts)** |
| 5 | Read Profile | `GET /profile/user_1` | N/A | 3 | `{}` | Profile fell back to 0% |
| 6 | Scroll back to Video A | `GET /feed` | N/A | 3 | `{}` | Read-only |
