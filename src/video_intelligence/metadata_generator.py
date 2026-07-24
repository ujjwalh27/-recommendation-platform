from typing import Dict, Any
from src.video_intelligence.schemas import VideoMetadataReport, ProvenanceDetailSchema

def _to_str_list(val):
    if not val:
        return []
    if not isinstance(val, list):
        val = [val]
    res = []
    for item in val:
        if isinstance(item, dict):
            v_strs = [str(v) for v in item.values() if v]
            res.append(" - ".join(v_strs) if v_strs else str(item))
        else:
            res.append(str(item))
    return res

class MetadataGenerator:
    """Formats refined semantic attributes and computed provenance maps into a standardized recommendation-ready output."""

    def generate_report(self, refined_data: Dict[str, Any], confidence_map: Dict[str, ProvenanceDetailSchema]) -> Dict[str, Any]:
        """
        Builds the final structured metadata dictionary matching the target schema.
        """
        # Build pydantic model for validation with sanitized list fields
        report = VideoMetadataReport(
            title=str(refined_data.get("title", "Unlabeled Video Asset")),
            summary=str(refined_data.get("summary", "")),
            category=str(refined_data.get("category", "Entertainment")),
            subcategory=str(refined_data.get("subcategory", "General Video")),
            primary_topic=str(refined_data.get("primary_topic", "General")),
            secondary_topics=_to_str_list(refined_data.get("secondary_topics")),
            entities=_to_str_list(refined_data.get("entities")),
            people=_to_str_list(refined_data.get("people")),
            locations=_to_str_list(refined_data.get("locations")),
            activities=_to_str_list(refined_data.get("activities")),
            objects=_to_str_list(refined_data.get("objects")),
            events=_to_str_list(refined_data.get("events")),
            keywords=_to_str_list(refined_data.get("keywords")),
            recommendation_keywords=_to_str_list(refined_data.get("recommendation_keywords")),
            language=str(refined_data.get("language", "English")),
            mood=str(refined_data.get("mood", "Normal")),
            emotion=str(refined_data.get("emotion", "Neutral")),
            target_audience=_to_str_list(refined_data.get("target_audience", ["General"])),
            reasoning=str(refined_data.get("reasoning", "")),
            confidence=confidence_map
        )
        
        # Return dict representation
        return report.dict()
