# Content Hashing Specification

## Implementation Overview
Content hashing in ACPCS provides an immutable fingerprint for every video asset.

- **Algorithm**: `SHA-256` (256-bit Secure Hash Algorithm)
- **Chunk Size**: `64 KB` (65,536 bytes) streaming read buffer for memory efficiency.
- **Python Module**: `content_catalog/duplicate_detection/hasher.py`

## Code Interface

```python
class ContentHasher:
    @staticmethod
    def compute_file_hash(file_path: str, chunk_size: int = 65536) -> str:
        hasher = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(chunk_size):
                hasher.update(chunk)
        return hasher.hexdigest()
```

## Performance & Overhead
- **Processing Time**: < 15ms per 20MB video file.
- **Memory Footprint**: Fixed 64KB RAM usage regardless of video size.
