import os
import sys

# Add project root to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.explainable_reasoning import ExplainableReasoningEngine

def main():
    print("==================================================")
    print("Testing Phase 5 Explainable AI Reasoning Engine")
    print("==================================================")

    test_video = "/Users/ujjwalhkumar/Downloads/daiv sample/Aditi Atul Jadhav.mp4"
    if not os.path.exists(test_video):
        print(f"Error: Test video file not found at: {test_video}")
        sys.path.exit(1)

    engine = ExplainableReasoningEngine()
    video_id = "xai_test_aditi"

    result = engine.process_video_with_explainability(test_video, video_id)

    print("\n==================================================")
    print("EXPLAINABLE AI REASONING PASSED SUCCESSFULLY!")
    print("==================================================")

    print(f"Video ID: {result['video_id']}")
    print(f"Claims Built: {len(result['claims'])}")
    print(f"Competing Hypotheses Generated: {len(result['hypotheses'])}")
    print(f"Conflicts Resolved: {len(result['conflicts'])}")
    print(f"Episodes Aggregated: {len(result['episodes'])}")

    print("\n=== SAMPLE CLAIM LAYER (Evidence Traceability) ===")
    c1 = result['claims'][0]
    print(f"Claim ID: {c1['claim_id']}")
    print(f"Claim Text: {c1['claim_text']}")
    print(f"Frames Link: {c1['supporting_evidence']['frame_ids']}")
    print(f"Transcript Segment Link: {c1['supporting_evidence']['transcript_segments'][:1]}")

    print("\n=== SAMPLE MULTI-HYPOTHESES RANKING ===")
    for h in result['hypotheses']:
        print(f"- [{h['hypothesis_id']}] {h['label']:<35} (Conf: {h['confidence']}) -> {h['selection_reasoning']}")

    print("\n=== SAMPLE CONFLICT RESOLUTION ===")
    for conf in result['conflicts']:
        print(f"- Trusted Source: {conf['trusted_source']}")
        print(f"  Rejected Source: {conf['rejected_source']}")
        print(f"  Reasoning: {conf['resolution_reasoning']}")

    print("\n=== INTERACTIVE XAI QUERY ANSWERS ===")
    q1 = result['sample_xai_answers']['why_classified']
    print(f"Q: {q1['query']}")
    print(f"A: {q1['primary_answer']}")
    print(f"Evidence Cited: {q1['evidence_cited']}")

    q2 = result['sample_xai_answers']['counterfactual_speech']
    print(f"\nQ (Counterfactual): {q2['query']}")
    print(f"A: {q2['primary_answer']}")

    print("\n==================================================")
    print("Phase 5 Explainable AI Verification Completed!")
    print("==================================================")

if __name__ == "__main__":
    main()
