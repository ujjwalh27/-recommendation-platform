import os

# Storage settings
GRAPH_STORAGE_DIR = os.environ.get("GRAPH_STORAGE_DIR", "datasets/processed/knowledge_graphs")
TEMP_DIR = "datasets/processed/ske_temp"

# Entity Categories (14 distinct types)
ENTITY_TYPES = [
    "Person",
    "Location",
    "Building",
    "Animal",
    "Object",
    "Vehicle",
    "ReligiousSymbol",
    "Product",
    "Brand",
    "Food",
    "Music",
    "Organization",
    "Concept",
    "Event"
]

# Standard Relationship Predicates
RELATIONSHIP_PREDICATES = [
    "LOCATED_AT",
    "PERFORMS",
    "PREPARES",
    "LISTEN_TO",
    "PLAYS",
    "OBSERVES",
    "CONTAINS",
    "IS_A",
    "TRANSITIONS_TO",
    "USES_OBJECT",
    "EXPRESSES_EMOTION",
    "PART_OF"
]
