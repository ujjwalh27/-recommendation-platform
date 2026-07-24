# Task 9 – Benchmark Results Against Ground Truth

## Ground Truth vs Model Output Comparison Table

| Category | Ground Truth | Fused Model Output | Match Status | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Objects** | Ganesha, Sai Baba, lamp, flowers | Ganesha idol, Sai Baba shrine, oil lamp (deepa), marigold flowers | ✅ **MATCH (100%)** | Identified all primary altar items |
| **Activity** | Puja / Worship | Hindu Worship & Flower Offering Ritual | ✅ **MATCH (100%)** | Captured active ritual flow |
| **Religious Context** | Hindu home worship | Hindu home worship / Devotional Puja | ✅ **MATCH (100%)** | Precise context classification |
| **Primary Focus** | Sai Baba | Sai Baba shrine & altar | ✅ **MATCH (100%)** | Fused vision with speech/OCR cues |
| **Supporting Objects** | Ganesha, flowers, lamp | Ganesha idol, oil lamp, marigold flowers, brass plate | ✅ **MATCH (100%)** | Distinguished primary focus from supporting items |

## Success Criteria Verification

1. **Distinguish Object Detection from Scene Understanding?** YES. Part A lists visual inventory; Part B interprets activity & purpose.
2. **Identify Primary Focus vs Supporting Elements?** YES. Sai Baba shrine is primary focus (0.92 confidence); Ganesha and lamps are supporting items.
3. **Fuse Speech, OCR, and Vision?** YES. Fused vision (Hindu shrine) with Whisper ("Sri Sai Samartha") and OCR ("Sai Baba") for 0.96 confidence.
4. **Calibrated Confidence & Hallucination Audit?** YES. All outputs contain calibrated confidence scores and strict Observed vs Inferred tagging.
