# Forensic Report: Fixed Architecture

```text
                  USER INTERACTION (Like / Save / Comment / Watch >=85%)
                                     │
                                     ▼
                   Deterministic Idempotent Event ID Generation
                   (evt_{userId}_{videoId}_{isLiked}_{isSaved})
                                     │
                                     ▼
                          HTTP POST /feedback Payload
                                     │
                                     ▼
                            FastAPI /feedback Handler
                                     │
                                     ▼
                 UserInterestProfileStore.process_event()
                          SINGLE AUTHORITATIVE WRITE
                                     │
                    ┌────────────────┴────────────────┐
                    ▼                                 ▼
             Persistent Disk State             In-Memory Store
         (interest_profiles.json &            (threading.RLock)
          interaction_events.json)                    │
                    │                                 │
                    └────────────────┬────────────────┘
                                     ▼
                      HTTP GET /feed Recommendation
                          100% READ-ONLY OPERATION
                                     │
                    ┌────────────────┴────────────────┐
                    ▼                                 ▼
           Candidate Generator                 Rule-Based Scorer
        (Reads Profile Snapshot)           (Reads Profile Snapshot)
                    │                                 │
                    └────────────────┬────────────────┘
                                     ▼
                        Personalized Feed Response
                     [ZERO Profile State Mutation]
```

## Guarantees Enforced
1. **Single Writer**: Only `UserInterestProfileStore.process_event()` updates raw scores & category interest vectors.
2. **Read-Only Feed Engine**: Candidate retrieval, Collaborative Filtering, and Scorer never mutate profile state.
3. **Idempotency**: Duplicate event IDs are identified and safely ignored without state changes.
4. **Read-Only Scrolling**: Navigation across videos generates 0 feedback HTTP requests unless an explicit engagement event occurred.
