"""
Task 2 – Canonical Semantic Document Builder
Constructs normalized, structured semantic documents exclusively from CMREE Canonical Metadata fields.
"""

from typing import Dict, Any, List


class CanonicalSemanticDocumentBuilder:
    """Builds structured text documents for embedding generation exclusively from CMREE Canonical Metadata."""

    def build_document(self, canonical_metadata: Dict[str, Any]) -> str:
        """
        Constructs a structured semantic document string from a CMREE canonical metadata dict.
        """
        doc_dict = canonical_metadata.get("canonical_metadata", canonical_metadata)

        content_type = doc_dict.get("primary_category") or doc_dict.get("content_type", "Temple Ritual")
        primary_ritual = doc_dict.get("primary_ritual", "Devotional Worship")
        ritual_family = doc_dict.get("ritual_family", "Pooja")
        primary_deity = doc_dict.get("primary_deity", "Lord Shiva")
        tradition = doc_dict.get("tradition", "Universal Devotional")
        temple = doc_dict.get("temple") or "Generic Mandir"
        
        offerings = doc_dict.get("offerings", [])
        offerings_str = ", ".join(offerings) if offerings else "Flowers"
        
        language = doc_dict.get("language", "Hindi")
        keywords = doc_dict.get("keywords", [])
        keywords_str = " ".join(keywords) if keywords else f"{content_type} {primary_ritual} {primary_deity}"

        # Structured multi-line block representation
        semantic_doc = (
            f"Content Type:\n{content_type}\n"
            f"Primary Ritual:\n{primary_ritual}\n"
            f"Ritual Family:\n{ritual_family}\n"
            f"Primary Deity:\n{primary_deity}\n"
            f"Tradition:\n{tradition}\n"
            f"Temple:\n{temple}\n"
            f"Offerings:\n{offerings_str}\n"
            f"Language:\n{language}\n"
            f"Keywords:\n{keywords_str}"
        )

        return semantic_doc

    def build_dense_embedding_text(self, canonical_metadata: Dict[str, Any]) -> str:
        """
        Constructs a single-line pipe-delimited text optimal for SentenceTransformers / E5 / BGE tokenizers.
        """
        doc_dict = canonical_metadata.get("canonical_metadata", canonical_metadata)

        category = doc_dict.get("primary_category", "Temple Ritual")
        ritual = doc_dict.get("primary_ritual", "Devotional Worship")
        family = doc_dict.get("ritual_family", "Pooja")
        deity = doc_dict.get("primary_deity", "Lord Shiva")
        temple = doc_dict.get("temple") or ""
        tradition = doc_dict.get("tradition", "")
        offerings = ", ".join(doc_dict.get("offerings", []))
        keywords = " ".join(doc_dict.get("keywords", []))

        parts = [
            f"Category: {category}",
            f"Primary Ritual: {ritual}",
            f"Ritual Family: {family}",
            f"Primary Deity: {deity}"
        ]
        if temple: parts.append(f"Temple: {temple}")
        if tradition: parts.append(f"Tradition: {tradition}")
        if offerings: parts.append(f"Offerings: {offerings}")
        if keywords: parts.append(f"Keywords: {keywords}")

        return " | ".join(parts)
