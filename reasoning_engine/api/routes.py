"""
Task 10 – CMREE API Routes Module
Defines FastAPI router endpoints for CMREE processing, validation, rule listing, and KB inspection.
"""

from fastapi import APIRouter, HTTPException, Body
from typing import Dict, Any, List
from reasoning_engine.pipeline import CMREEPipeline

router = APIRouter(prefix="/api/reasoning", tags=["CMREE Reasoning Engine"])
pipeline = CMREEPipeline()


@router.post("/process")
def process_observation_payload(raw_obs: Dict[str, Any] = Body(...)) -> Dict[str, Any]:
    """
    POST /api/reasoning/process
    Transforms raw VLM/multimodal observation JSON into normalized canonical metadata.
    """
    try:
        canonical_doc, validation_issues = pipeline.process_observation(raw_obs)
        return {
            "status": "success",
            "canonical_metadata": canonical_doc,
            "validation_issues": validation_issues
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"CMREE processing error: {str(e)}")


@router.post("/validate")
def validate_canonical_metadata(document: Dict[str, Any] = Body(...)) -> Dict[str, Any]:
    """
    POST /api/reasoning/validate
    Audits a canonical metadata document for schema errors, conflicts, or low confidence.
    """
    try:
        is_valid, issues = pipeline.doc_validator.validate_canonical_document(document)
        return {
            "is_valid": is_valid,
            "issue_count": len(issues),
            "issues": issues
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"CMREE validation error: {str(e)}")


@router.get("/rules")
def list_active_rules() -> Dict[str, Any]:
    """
    GET /api/reasoning/rules
    Returns active explainable reasoning rules loaded from reasoning_rules.yaml.
    """
    return {
        "rule_count": len(pipeline.rule_engine.rules),
        "rules": pipeline.rule_engine.rules
    }


@router.get("/knowledge-base")
def inspect_knowledge_base() -> Dict[str, Any]:
    """
    GET /api/reasoning/knowledge-base
    Returns versioned domain knowledge base definitions (Deities, Rituals, Temples).
    """
    return {
        "metadata": pipeline.enricher.kb.get_metadata(),
        "deities": pipeline.enricher.kb.get_deities(),
        "rituals": pipeline.enricher.kb.get_rituals(),
        "temples": pipeline.enricher.kb.get_temples()
    }
