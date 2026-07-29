import os
import json

class TemporalReasoningEngine:
    """
    Task 6 – Temporal Reasoning Engine.
    Analyzes the chronological sequence of events across the video timeline:
    e.g., Priest enters -> Water Wash -> Milk Pouring -> Flowers -> Lamp Lighting -> Aarti
    
    Identifies:
    - Chronological Event Timeline
    - Primary Ritual Action
    - Ritual Stage Progression
    - Completion Ritual (e.g. Completed With Aarti)
    """

    def analyze_timeline(self, keyframe_events, observations):
        obj_text = " ".join(observations.get("objects", [])).lower()
        act_text = " ".join(observations.get("actions", [])).lower()
        sp_text = " ".join(observations.get("speech", [])).lower()
        ocr_text = " ".join(observations.get("ocr", [])).lower()
        combined = obj_text + " " + act_text + " " + sp_text + " " + ocr_text

        timeline = []
        primary_temporal_action = "General Worship"
        completed_with = "Aarti"

        # Step 1: Initial Arrival / Preparation
        if "priest" in observations.get("people", []) or "enter" in combined:
            timeline.append("Priest enters shrine & prepares altar")
        else:
            timeline.append("Initial shrine setup & preparation")

        # Step 2: Cleansing / Water Pouring
        if "water" in combined or "pouring water" in act_text:
            timeline.append("Water washing & cleansing idol")

        # Step 3: Main Offering (Milk / Panchamrutha / Flowers / Lecture)
        if "milk" in combined or "pouring milk" in act_text:
            timeline.append("Milk Abhishekam liquid pouring")
            primary_temporal_action = "Milk Abhishekam"
        elif "panchamrut" in combined:
            timeline.append("Panchamrutha sacred nectars pouring")
            primary_temporal_action = "Panchamrutha Abhishekam"
        elif "honey" in combined:
            timeline.append("Honey Abhishekam pouring")
            primary_temporal_action = "Honey Abhishekam"
        elif "flower" in combined or "offering flowers" in act_text:
            timeline.append("Flower garland & petal offering (Archana)")
            primary_temporal_action = "Flower Offering"
        elif "bhajan" in combined or "singing" in combined:
            timeline.append("Devotional song singing & music")
            primary_temporal_action = "Devotional Bhajan"
        elif "pravachan" in combined or "gita" in combined:
            timeline.append("Scripture verse commentary & pravachan")
            primary_temporal_action = "Scripture Discourse"

        # Step 4: Lamp Lighting / Camphor
        if "lamp" in combined or "camphor" in combined or "deepa" in combined:
            timeline.append("Lighting camphor flame & oil lamps")

        # Step 5: Final Aarti & Conclusion
        if "aarti" in combined or "waving flame" in act_text or "circular" in act_text:
            timeline.append("Executing Aarti circular flame rotation before shrine")
            completed_with = "Aarti"

        return {
            "timeline_events": timeline,
            "primary_temporal_action": primary_temporal_action,
            "completed_with": completed_with,
            "sequence_summary": " -> ".join(timeline)
        }
