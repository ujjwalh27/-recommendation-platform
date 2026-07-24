# Hallucination Casebook & Verification

## 1. Verified Hallucination Count
- **Total Statements Evaluated**: 800 (8 statements per video across 100 videos)
- **Verified Hallucinations**: 12 statements
- **Verified Hallucination Rate**: **`1.50%`** (consistent with reported 1.53%)

## 2. Detailed Casebook Entries

### Case 1: Unsubstantiated Festival Attribution
- **Generated Statement**: *"Diwali Festival Celebration"*
- **Ground Truth**: General Home Worship Puja
- **Supporting Evidence**: Marigold flowers and oil lamps visible, but no text cue.
- **Classification Reason**: **Hallucination (Assumed)** — model inferred a specific festival name without text/speech verification.

### Case 2: Studio Setting Over-Generalization
- **Generated Statement**: *"Audition monologue in a studio setting"*
- **Ground Truth**: Personal vlog monologue
- **Supporting Evidence**: Person speaking into camera.
- **Classification Reason**: **Hallucination (Assumed)** — legacy artifact from text-only prompt fallback.
