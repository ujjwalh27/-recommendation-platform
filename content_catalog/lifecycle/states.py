"""
Processing Lifecycle States & Enum Definitions
"""

from enum import Enum


class ProcessingState(str, Enum):
    RECEIVED = "RECEIVED"
    PROCESSING = "PROCESSING"
    CMREE_COMPLETE = "CMREE_COMPLETE"
    EMBEDDING_COMPLETE = "EMBEDDING_COMPLETE"
    INDEXED = "INDEXED"
    PUBLISHED = "PUBLISHED"
    FAILED = "FAILED"


class PublicationAction(str, Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    SKIP = "SKIP"
    FAIL = "FAIL"
