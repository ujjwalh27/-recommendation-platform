# Failure Injection & Resilience Test Report

## Fault Tolerance Matrix

| Failure Scenario | Injected Condition | System Behavior | HTTP Response | Crash Status |
| :--- | :--- | :--- | :--- | :--- |
| **Empty Upload** | 0-byte file | Rejected at API boundary | `400 Bad Request` | ✅ No Crash |
| **Corrupted Codec** | Malformed MP4 header | OpenCV validation failure catch | `422 Unprocessable` | ✅ No Crash |
| **Unsupported Format** | `.avi` file upload | MIME extension check rejection | `415 Unsupported` | ✅ No Crash |
| **Oversized Upload** | 2.5 GB file | Gateway payload boundary limit | `413 Payload Too Large`| ✅ No Crash |
| **Ollama Service Down** | Local VLM offline | Fallback to Vision-rule heuristics | `200 OK (Degraded)` | ✅ No Crash |
| **Whisper ASR Down** | ASR pipeline offline | Fallback to Vision + OCR evidence | `200 OK (Degraded)` | ✅ No Crash |
| **Disk Space Full** | Low disk space | Rejects new job, returns error | `507 Storage Full` | ✅ No Crash |
