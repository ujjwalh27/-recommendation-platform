"""
Deterministic Content Hasher (SHA-256)
Computes immutable SHA-256 hash over raw video files.
"""

import hashlib
import os


class ContentHasher:
    """Computes SHA-256 hashes of video files for deterministic duplicate detection."""

    @staticmethod
    def compute_file_hash(file_path: str, chunk_size: int = 65536) -> str:
        """Computes SHA-256 hash of a file at file_path."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Video file not found: {file_path}")

        hasher = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(chunk_size):
                hasher.update(chunk)
                
        return hasher.hexdigest()

    @staticmethod
    def compute_bytes_hash(file_bytes: bytes) -> str:
        """Computes SHA-256 hash over raw in-memory video bytes."""
        hasher = hashlib.sha256()
        hasher.update(file_bytes)
        return hasher.hexdigest()
