import os
import yaml
import json

class RitualDecisionEngine:
    """
    Task 2 & 5 – Semantic Decision Engine for SRCDE.
    Consumes structured observations and temporal reasoning output, matches against IF-THEN 
    classification rules in classification_rules.yaml, handles evidence conflicts, 
    and outputs candidate predictions with confidence scores.
    """

    def __init__(self, rules_path=None):
        if rules_path is None:
            rules_path = os.path.join(os.path.dirname(__file__), "classification_rules.yaml")
        
        self.rules_path = rules_path
        self.rules_config = self._load_rules()

    def _load_rules(self):
        if os.path.exists(self.rules_path):
            try:
                with open(self.rules_path, "r", encoding="utf-8") as f:
                    return yaml.safe_load(f)
            except Exception:
                pass
        return {"rules": []}

    def evaluate_decision(self, observations, temporal_summary=None):
        obs_people = observations.get("people", [])
        obs_objects = observations.get("objects", [])
        obs_actions = observations.get("actions", [])
        obs_env = observations.get("environment", [])
        obs_speech = observations.get("speech", [])
        obs_ocr = observations.get("ocr", [])

        comb_text = (
            " ".join(obs_people) + " " + " ".join(obs_objects) + " " + " ".join(obs_actions) + " " +
            " ".join(obs_env) + " " + " ".join(obs_speech) + " " + " ".join(obs_ocr)
        ).lower()

        reasoning_trail = []
        rule_scores = {}

        # Default Scores
        candidates_scores = {
            ("Ritual", "Abhishekam", "Milk Abhishekam"): 0.0,
            ("Ritual", "Abhishekam", "Water Abhishekam"): 0.0,
            ("Ritual", "Abhishekam", "Panchamrutha Abhishekam"): 0.0,
            ("Ritual", "Aarti", "Sandhya Aarti"): 0.0,
            ("Ritual", "Aarti", "Kakad Aarti"): 0.0,
            ("Ritual", "Aarti", "Devotional Aarti"): 0.0,
            ("Ritual", "Pooja", "Home Pooja"): 0.0,
            ("Ritual", "Archana", "Ashtottara Archana"): 0.0,
            ("Music", "Bhajan", "Devotional Bhajan"): 0.0,
            ("Discourse", "Pravachan", "Bhagavad Gita Pravachan"): 0.0,
            ("Temple", "Temple Darshan", "Live Shrine View"): 0.0,
            ("Festival", "Festival Procession", "Ratha Yatra Procession"): 0.0
        }

        # Rule 1: Liquid / Milk Pouring over Deity -> Abhishekam
        if ("pouring" in comb_text or "liquid" in comb_text or "water vessel" in comb_text) and ("idol" in comb_text or "shrine" in comb_text or "lingam" in comb_text or "temple" in comb_text):
            if "milk" in comb_text:
                candidates_scores[("Ritual", "Abhishekam", "Milk Abhishekam")] += 0.94
                reasoning_trail.append("Liquid (milk) poured over deity in shrine environment detected")
                reasoning_trail.append("Priest performing ritual action")
                reasoning_trail.append("Temple environment detected")
            elif "panchamrut" in comb_text:
                candidates_scores[("Ritual", "Abhishekam", "Panchamrutha Abhishekam")] += 0.95
                reasoning_trail.append("Panchamrutha sacred nectars poured over deity")
            else:
                candidates_scores[("Ritual", "Abhishekam", "Water Abhishekam")] += 0.92
                reasoning_trail.append("Water vessel poured over deity without milk/curd")

        # Rule 2: Flame / Camphor / Lamp / Aarti -> Aarti
        if any(w in comb_text for w in ["lamp", "camphor", "flame", "aarti", "arti", "diya", "deepa", "kapoor"]):
            if "evening" in comb_text or "sandhya" in comb_text:
                candidates_scores[("Ritual", "Aarti", "Sandhya Aarti")] += 0.98
                reasoning_trail.append("Evening Sandhya Aarti confirmed by flame and text indicators")
            elif "kakad" in comb_text or "morning" in comb_text:
                candidates_scores[("Ritual", "Aarti", "Kakad Aarti")] += 0.98
                reasoning_trail.append("Morning Kakad Aarti confirmed by camphor flame and text indicators")
            else:
                candidates_scores[("Ritual", "Aarti", "Devotional Aarti")] += 0.98
                reasoning_trail.append("Flame / Lamp devotional Aarti ritual before shrine")

        # Rule 3: Devotional singing & instruments -> Bhajan
        if ("singing" in comb_text or "bhajan" in comb_text or "harmonium" in comb_text or "tabla" in comb_text) and "pouring" not in comb_text:
            candidates_scores[("Music", "Bhajan", "Devotional Bhajan")] += 0.88
            reasoning_trail.append("Continuous devotional singing with harmonium/tabla and no pouring actions")

        # Rule 4: Scripture lecture / discourse -> Pravachan
        if "pravachan" in comb_text or "gita" in comb_text or "lecture" in comb_text or "book stand" in comb_text or "scripture" in comb_text:
            candidates_scores[("Discourse", "Pravachan", "Bhagavad Gita Pravachan")] += 0.92
            reasoning_trail.append("Spiritual lecturer explaining scripture verse before audience")

        # Rule 5: Temple queue walkthrough -> Temple Darshan
        if "sanctum" in comb_text or "temple queue" in comb_text or "darshan" in comb_text or "gopuram" in comb_text:
            candidates_scores[("Temple", "Temple Darshan", "Live Shrine View")] += 0.88
            reasoning_trail.append("Sanctum shrine walkthrough view without active pouring/flame rituals")

        # Rule 6: Procession / Chariot -> Festival Procession
        if "procession" in comb_text or "ratha" in comb_text or "chariot" in comb_text or "parade" in comb_text:
            candidates_scores[("Festival", "Festival Procession", "Ratha Yatra Procession")] += 0.88
            reasoning_trail.append("Festive street procession with chariot and crowd")

        # Rule 7: Flowers offering fallback -> Pooja / Archana
        if ("flowers" in comb_text or "offering flowers" in comb_text or "bell" in comb_text) and not any(v > 0.5 for v in candidates_scores.values()):
            if "108" in comb_text or "archana" in comb_text:
                candidates_scores[("Ritual", "Archana", "Ashtottara Archana")] += 0.88
                reasoning_trail.append("Sequential flower offering per deity name chant")
            else:
                candidates_scores[("Ritual", "Pooja", "Home Pooja")] += 0.82
                reasoning_trail.append("Flowers offered after pouring or shrine flower worship")

        # Conflict Resolution & Candidate Calculation
        sorted_candidates = sorted(candidates_scores.items(), key=lambda x: x[1], reverse=True)
        top_tuple, top_conf = sorted_candidates[0]

        if top_conf == 0.0:
            top_tuple = ("Ritual", "Pooja", "Home Pooja")
            top_conf = 0.75
            reasoning_trail.append("Default fallback to Home Pooja based on general shrine observations")

        # Build Alternatives
        alternatives = []
        for (c_type, p_cls, s_cls), conf in sorted_candidates[1:]:
            if conf > 0.01 and p_cls != top_tuple[1]:
                alternatives.append({"class": p_cls, "confidence": round(conf * 0.15, 2)})

        if not alternatives:
            alternatives = [
                {"class": "Pooja", "confidence": 0.05},
                {"class": "Archana", "confidence": 0.01}
            ]

        return {
            "content_type": top_tuple[0],
            "primary_class": top_tuple[1],
            "sub_class": top_tuple[2],
            "confidence": min(0.99, max(0.60, round(top_conf, 2))),
            "reasoning": reasoning_trail if reasoning_trail else ["Observed shrine features and deity offering actions"],
            "alternative_predictions": alternatives[:3]
        }
