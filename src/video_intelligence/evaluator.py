import os
from typing import Dict, Any, List
from src.video_intelligence.schemas import SemanticGraphHierarchySchema

class HumanEvaluator:
    """Generates structured Markdown human-validation templates for auditing the semantic accuracy of processed videos."""

    def __init__(self, output_dir: str = "docs/validation_reports"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_report(self, video_id: str, metadata: Dict[str, Any], hierarchy: SemanticGraphHierarchySchema) -> str:
        """
        Synthesizes a structured Markdown validation sheet and saves it to disk.
        
        Returns:
            Path to the saved report.
        """
        report_path = os.path.join(self.output_dir, f"validation_report_{video_id}.md")
        
        # 1. Gather scene details
        scene_lines = []
        for s in hierarchy.scenes:
            scene_lines.append(f"- **Scene [{s.timestamp_start:.1f}s - {s.timestamp_end:.1f}s]**: {s.description}")
            
        # 2. Gather transcript segments
        speech_text = " ".join([n.value for n in hierarchy.evidence.speech])
        if not speech_text:
            speech_text = "*No audio transcript detected.*"

        # 3. Gather evidence details
        ocr_lines = [f"  - `{n.value}` (Confidence: {n.confidence:.2f})" for n in hierarchy.evidence.ocr]
        vision_lines = [f"  - `{n.value}` (Confidence: {n.confidence:.2f})" for n in hierarchy.evidence.vision]
        action_lines = [f"  - `{n.value}` (Confidence: {n.confidence:.2f})" for n in hierarchy.evidence.actions]
        audio_lines = [f"  - `{n.value}` (Confidence: {n.confidence:.2f})" for n in hierarchy.evidence.audio]

        # 4. Gather confidence & provenance
        prov_lines = []
        for field, detail in metadata.get("confidence", {}).items():
            # If detail is dict, convert to class
            evidence = detail.get("evidence", []) if isinstance(detail, dict) else detail.evidence
            score = detail.get("confidence", 0.0) if isinstance(detail, dict) else detail.confidence
            reason = detail.get("reason", "") if isinstance(detail, dict) else detail.reason
            prov_lines.append(
                f"| **{field.upper()}** | {score:.2f} | {', '.join(evidence)} | {reason} |"
            )

        report_content = f"""# Video Intelligence Engine: Human Validation Report

## Video Asset Details
* **Video ID**: `{video_id}`
* **Duration**: `{hierarchy.duration:.2f} seconds`

---

## 👁️ Visual Timeline & Scenes
{chr(10).join(scene_lines)}

---

## 🎙️ Audio Transcript (Speech-to-Text)
> {speech_text}

---

## 🧠 Semantic Understanding (Generated Metadata)
* **Title**: {metadata.get("title", "")}
* **Summary**: {metadata.get("summary", "")}
* **Category**: {metadata.get("category", "")} | **Subcategory**: {metadata.get("subcategory", "")}
* **Primary Topic**: {metadata.get("primary_topic", "")}
* **Secondary Topics**: {", ".join(metadata.get("secondary_topics", [])) if metadata.get("secondary_topics") else "*None*"}
* **Language**: {metadata.get("language", "")}
* **Mood**: {metadata.get("mood", "")} | **Emotion**: {metadata.get("emotion", "")}
* **Target Audience**: {", ".join(metadata.get("target_audience", [])) if metadata.get("target_audience") else "*None*"}
* **Reasoning Explanation**: {metadata.get("reasoning", "")}

---

## 📊 Secondary Modality Evidence
* **OCR Screen Detections**:
{chr(10).join(ocr_lines) if ocr_lines else "  - *No text blocks scanned.*"}
* **Visual Object Detections (YOLO/CLIP)**:
{chr(10).join(vision_lines) if vision_lines else "  - *No objects detected.*"}
* **Human Action Detections (VideoMAE)**:
{chr(10).join(action_lines) if action_lines else "  - *No actions classified.*"}
* **Audio Set Sound Events (AST)**:
{chr(10).join(audio_lines) if audio_lines else "  - *No sound events detected.*"}

---

## 📈 Provenance & Confidence Evaluation
| Field Name | Confidence Score | Evidence Sources | Algorithmic Reason / Justification |
| :--- | :--- | :--- | :--- |
{chr(10).join(prov_lines)}

---

## ✍️ Human Auditor Review Feedback
*Please fill out this block to track semantic alignment performance:*

* **Title Accuracy**: [ ] Correct  |  [ ] Partially Correct  |  [ ] Incorrect
* **Summary Accuracy**: [ ] Correct  |  [ ] Partially Correct  |  [ ] Incorrect
* **Topic & Tag Relevance**: [ ] Correct  |  [ ] Partially Correct  |  [ ] Incorrect
* **Category Classification**: [ ] Correct  |  [ ] Partially Correct  |  [ ] Incorrect

### Review Comments & Notes
```text
[Enter feedback details, discrepancies, or notes here]
```

**Auditor Name**: \_\_\_\_\_\_\_\_\_\_\_\_  
**Date Evaluated**: \_\_\_\_\_\_\_\_\_\_\_\_
"""

        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report_content)
            
        print(f"[Evaluator] Saved human validation sheet: {report_path}")
        return report_path
