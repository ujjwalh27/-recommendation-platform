import os
import json

class DomainRuleEngine:
    """
    Multi-Signal Domain Rule Engine for HRCE.
    Combines Vision, Speech, OCR, and Temporal signals to compute candidate scores
    and resolve evidence conflicts.
    """

    def apply_rules(self, observations, temporal_analysis):
        vis_objs = observations.get("objects", []) if isinstance(observations.get("objects"), list) else observations.get("vision", {}).get("objects", [])
        vis_acts = observations.get("actions", []) if isinstance(observations.get("actions"), list) else observations.get("vision", {}).get("actions", [])
        sp_items = observations.get("speech", []) if isinstance(observations.get("speech"), list) else [observations.get("speech", {}).get("transcript", "")]
        ocr_items = observations.get("ocr", []) if isinstance(observations.get("ocr"), list) else observations.get("ocr", {}).get("detected_lines", [])

        text_bag = " ".join([str(x) for x in (vis_objs + vis_acts + sp_items + ocr_items)]).lower()


        scores = {
            "Abhishekam": 0.0,
            "Aarti": 0.0,
            "Pooja": 0.0,
            "Archana": 0.0,
            "Bhajan": 0.0,
            "Pravachan": 0.0,
            "Temple Darshan": 0.0,
            "Festival Procession": 0.0
        }

        applied_rules = []

        has_pouring = any(w in text_bag for w in ["pouring", "bathing", "doodh abhishek", "abhishekam"])
        has_aarti = any(w in text_bag for w in ["camphor", "kapoor", "aarti", "arti", "flame", "deepa", "lamp", "diya"])

        # Rule 1: Active Liquid Pouring Abhishekam Signals
        if has_pouring and ("milk" in text_bag or "doodh" in text_bag or "water" in text_bag or "abhishekam" in text_bag):
            scores["Abhishekam"] += 0.90
            applied_rules.append("Rule-1: Active liquid pouring signal detected -> Boost Abhishekam")

        # Rule 2: Flame / Lamp / Camphor Aarti Signals
        if has_aarti:
            scores["Aarti"] += 0.98
            applied_rules.append("Rule-2: Flame/Aarti signal detected -> Boost Aarti")

        # Rule 3: Devotional Music / Singing Signals
        if "bhajan" in text_bag or "singing" in text_bag or "tabla" in text_bag or "harmonium" in text_bag or "kirtan" in text_bag:
            scores["Bhajan"] += 0.80
            applied_rules.append("Rule-3: Music/Singing signal detected -> Boost Bhajan")

        # Rule 4: Scripture / Lecture / Pravachan Signals
        if "pravachan" in text_bag or "gita" in text_bag or "lecture" in text_bag or "katha" in text_bag or "teaching" in text_bag:
            scores["Pravachan"] += 0.85
            applied_rules.append("Rule-4: Scripture/Pravachan signal detected -> Boost Pravachan")

        # Rule 5: Temple View / Queue / Walkthrough Signals
        if "darshan" in text_bag or "temple tour" in text_bag or "queue" in text_bag or "sanctum" in text_bag:
            scores["Temple Darshan"] += 0.80
            applied_rules.append("Rule-5: Temple/Darshan signal detected -> Boost Temple Darshan")

        # Rule 6: Procession / Chariot Signals
        if "procession" in text_bag or "ratha" in text_bag or "chariot" in text_bag or "parade" in text_bag:
            scores["Festival Procession"] += 0.85
            applied_rules.append("Rule-6: Procession/Chariot signal detected -> Boost Festival Procession")

        # Rule 7: General Flowers / Bell Pooja Fallback
        if "flower" in text_bag or "bell" in text_bag or "pooja" in text_bag:
            scores["Pooja"] += 0.60
            if "108" in text_bag or "archana" in text_bag:
                scores["Archana"] += 0.80
            applied_rules.append("Rule-7: Flowers/Bell signal detected -> Boost Pooja/Archana")

        # Normalize Scores into Candidate Probabilities
        tot_score = sum(scores.values())
        if tot_score == 0:
            scores["Pooja"] = 1.0
            tot_score = 1.0

        candidates = []
        for cls_name, raw_sc in scores.items():
            prob = round(raw_sc / tot_score, 4)
            if prob > 0.01:
                candidates.append({"class": cls_name, "confidence": prob})

        candidates = sorted(candidates, key=lambda x: x["confidence"], reverse=True)

        return {
            "top_candidates": candidates,
            "primary_class": candidates[0]["class"],
            "primary_confidence": candidates[0]["confidence"],
            "applied_rules": applied_rules
        }
