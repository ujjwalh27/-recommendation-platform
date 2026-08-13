# Forensic Multi-Process / Worker State Report

## Server Deployment Topology Audit

- **FastAPI Execution Command**:
  `uvicorn backend.app:app --host 0.0.0.0 --port 8000`
- **Worker Configuration**: `--workers 1` (Single Process).
- **Process ID (PID)**: Unique single process managing `UserInterestProfileStore`.

---

## Single Process Thread Safety
- `UserInterestProfileStore` uses `threading.RLock()` for thread-safe concurrency.
- Multithreaded feedback requests (e.g. concurrent HTTP requests from frontends) are serialized safely.
- Monotonic version integrity is preserved across concurrent threads.

---

## Multi-Worker Deployment Recommendation
If the application is deployed in production with multiple uvicorn worker processes (`--workers N`):
1. In-memory dictionary state is local to each process worker.
2. File-backed locking or shared cache (e.g., Redis or PostgreSQL atomic updates) should be enabled.
3. For single-process development and evaluation server, single-instance `UserInterestProfileStore` guarantees 100% consistency.
