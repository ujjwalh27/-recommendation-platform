# Content Publication Workflow Specification

## Lifecycle State Machine

The processing lifecycle enforces state transitions:

```
 RECEIVED -> PROCESSING -> CMREE_COMPLETE -> EMBEDDING_COMPLETE -> INDEXED -> PUBLISHED
                                                                          \
                                                                           -> FAILED
```

## Pre-Condition Checklist

Before publishing content to the production catalog and live recommendation feed, `ContentPublisher` validates:

1. `observation_generation == SUCCESS` (Visual frames, Whisper transcript, OCR extracted)
2. `cmree == SUCCESS` (Rule-based reasoning engine emitted canonical metadata)
3. `canonical_metadata != None` (Metadata present and non-empty)
4. `embedding != None` (384-dimensional vector successfully computed)
5. `faiss_indexing == SUCCESS` (Vector safely indexed)

---

## Action Decision Matrix

| Existing Hash Match? | Metadata / Vector Changed? | Publication Action | Catalog State | FAISS Index Action |
|---|---|---|---|---|
| **No** | N/A | `CREATE` | Published (v1) | Insert New Vector |
| **Yes** | **No** | `SKIP` | Skipped (v1) | No Action (Log "No Changes") |
| **Yes** | **Yes** | `UPDATE` | Published (v+1) | In-Place Replace Vector |
| Pre-condition Fail | N/A | `FAIL` | Blocked | Block Publication |
