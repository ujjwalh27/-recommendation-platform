import sys
import os

# Ensure the project root is in the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ingestion.metadata_enricher import MetadataEnricher

if __name__ == "__main__":
    print("=" * 60)
    print("Starting Offline Metadata Enrichment Pipeline")
    print("=" * 60)
    
    enricher = MetadataEnricher()
    enricher.enrich()
    
    print()
    print("Metadata Enrichment Pipeline Completed Successfully!")
    print("=" * 60)
