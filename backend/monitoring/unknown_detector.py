import os
import json
import time
from typing import Dict, Any, List

PROPOSALS_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "production_monitoring", "taxonomy_proposals.json")

class UnknownKnowledgeDetector:
    """
    Module 6 – Unknown Knowledge Detection & Taxonomy Review Queue Manager.
    Detects entities outside current taxonomy and manages approval workflow.
    """

    def __init__(self):
        os.makedirs(os.path.dirname(PROPOSALS_FILE), exist_ok=True)
        if not os.path.exists(PROPOSALS_FILE):
            self._init_seed_proposals()

    def get_proposals(self) -> List[Dict[str, Any]]:
        if os.path.exists(PROPOSALS_FILE):
            try:
                with open(PROPOSALS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return []

    def approve_proposal(self, proposal_id: str) -> Dict[str, Any]:
        proposals = self.get_proposals()
        target = next((p for p in proposals if p.get("proposal_id") == proposal_id), None)
        updated = [p for p in proposals if p.get("proposal_id") != proposal_id]
        with open(PROPOSALS_FILE, "w", encoding="utf-8") as f:
            json.dump(updated, f, indent=2)

        if target:
            # Update dbb_taxonomy.json if approved
            tax_path = os.path.join(os.path.dirname(__file__), "..", "..", "src", "semantic_knowledge", "dbb_taxonomy.json")
            if os.path.exists(tax_path):
                with open(tax_path, "r", encoding="utf-8") as f:
                    tax = json.load(f)
                category = target.get("proposed_category", "rituals")
                val = target.get("entity_name")
                if category in tax and isinstance(tax[category], list) and val not in tax[category]:
                    tax[category].append(val)
                    with open(tax_path, "w", encoding="utf-8") as f:
                        json.dump(tax, f, indent=2)

        return {"status": "SUCCESS", "message": f"Proposal {proposal_id} approved and merged into dbb_taxonomy.json"}

    def reject_proposal(self, proposal_id: str) -> Dict[str, Any]:
        proposals = self.get_proposals()
        updated = [p for p in proposals if p.get("proposal_id") != proposal_id]
        with open(PROPOSALS_FILE, "w", encoding="utf-8") as f:
            json.dump(updated, f, indent=2)
        return {"status": "SUCCESS", "message": f"Proposal {proposal_id} rejected."}

    def _init_seed_proposals(self):
        seed = [
            {
                "proposal_id": "prop_001",
                "entity_type": "New Ritual",
                "proposed_category": "rituals",
                "entity_name": "Chandi Homa",
                "occurrences_count": 14,
                "first_detected": "2026-07-25 14:00:00",
                "sample_video_ids": ["video_ci_1002", "video_ci_1009"],
                "status": "Pending"
            },
            {
                "proposal_id": "prop_002",
                "entity_type": "New Temple",
                "proposed_category": "temples",
                "entity_name": "Shree Mahakaleshwar Ujjain",
                "occurrences_count": 8,
                "first_detected": "2026-07-26 11:20:00",
                "sample_video_ids": ["video_ci_1015"],
                "status": "Pending"
            }
        ]
        with open(PROPOSALS_FILE, "w", encoding="utf-8") as f:
            json.dump(seed, f, indent=2)
