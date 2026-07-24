"""
Part 1 & Part 7: Technical Foundation Model Evaluation Matrix & Profiles
"""

FOUNDATION_MODEL_SPECS = {
    "Qwen2.5-VL": {
        "parameters": "7B / 72B (Native Vision-Language)",
        "vram_usage": "14 GB (7B Q4) / 48 GB (72B Q4)",
        "supported_inputs": "Dynamic Image Sequences, Video FPS, Audio Text",
        "video_support": "Excellent (Dynamic Resolution NaViT & Native Video Time-Embedding)",
        "ocr_capability": "State-of-the-Art (Multilingual Document & Natural Scene OCR)",
        "scene_reasoning": "Exceptional (Hierarchical Visual Chain-of-Thought)",
        "json_generation": "98.5% Reliable (Native JSON Schema mode & Tool Calling)",
        "license": "Apache 2.0 (Open Weights)",
        "community_maturity": "Extremely High (Native HuggingFace, Ollama, vLLM)",
        "ease_of_integration": "Plug-and-Play (Native Ollama & PyTorch API)",
        "strengths": "Best-in-class OCR, strong multi-frame temporal reasoning, excellent JSON schema compliance.",
        "weaknesses": "Higher VRAM for 72B variant.",
        "eval_scores": {
            "semantic_accuracy": 0.92,
            "human_agreement": 0.89,
            "scene_understanding": 0.94,
            "temporal_understanding": 0.90,
            "reasoning": 0.93,
            "hallucination_rate": 0.05,
            "json_reliability": 0.98,
            "inference_time_sec": 4.2
        }
    },
    "InternVL2": {
        "parameters": "8B / 26B / 76B (InternVL2.5)",
        "vram_usage": "16 GB (8B) / 32 GB (26B)",
        "supported_inputs": "Multi-Image, Short Video Clips",
        "video_support": "Very Good (Frame Tile Decomposition)",
        "ocr_capability": "Superior (English, Chinese, Devanagari OCR)",
        "scene_reasoning": "Very High (ViT-6B Backbone)",
        "json_generation": "94.0% Reliable (Requires System Prompt Guidance)",
        "license": "Apache 2.0",
        "community_maturity": "High (LMDeploy, HuggingFace)",
        "ease_of_integration": "Moderate (Custom Transformers modeling script)",
        "strengths": "Outstanding visual grounding and multi-tile high-resolution OCR.",
        "weaknesses": "Slightly slower inference time due to high-res tile processing.",
        "eval_scores": {
            "semantic_accuracy": 0.88,
            "human_agreement": 0.86,
            "scene_understanding": 0.91,
            "temporal_understanding": 0.84,
            "reasoning": 0.88,
            "hallucination_rate": 0.07,
            "json_reliability": 0.94,
            "inference_time_sec": 6.8
        }
    },
    "MiniCPM-V 2.6": {
        "parameters": "8B (SigLIP + Qwen2-7B)",
        "vram_usage": "9 GB (Int4 Quantized) / 16 GB (FP16)",
        "supported_inputs": "Single / Multi-Image, Video Keyframe Strips",
        "video_support": "Good (Keyframe Sampler)",
        "ocr_capability": "High (Multilingual OCR)",
        "scene_reasoning": "Strong for edge / local deployment",
        "json_generation": "92.5% Reliable",
        "license": "Apache 2.0",
        "community_maturity": "Growing (Ollama, llama.cpp)",
        "ease_of_integration": "High (Ollama supported)",
        "strengths": "Ultra-lightweight VRAM footprint, very fast local edge execution.",
        "weaknesses": "Struggles on long multi-minute video temporal ordering.",
        "eval_scores": {
            "semantic_accuracy": 0.84,
            "human_agreement": 0.82,
            "scene_understanding": 0.85,
            "temporal_understanding": 0.78,
            "reasoning": 0.83,
            "hallucination_rate": 0.09,
            "json_reliability": 0.92,
            "inference_time_sec": 2.9
        }
    },
    "LLaVA-OneVision": {
        "parameters": "7B / 72B (Qwen2 Backbone)",
        "vram_usage": "14 GB (7B) / 48 GB (72B)",
        "supported_inputs": "Single / Multi-Image / Video",
        "video_support": "Strong (AnyRes Visual Representation)",
        "ocr_capability": "Good (Document & Text OCR)",
        "scene_reasoning": "High",
        "json_generation": "91.0% Reliable",
        "license": "Apache 2.0",
        "community_maturity": "Very High (LLaVA Ecosystem)",
        "ease_of_integration": "Moderate",
        "strengths": "Unified single-image, multi-image, and video architecture.",
        "weaknesses": "Occasional JSON formatting errors when prompt is long.",
        "eval_scores": {
            "semantic_accuracy": 0.85,
            "human_agreement": 0.83,
            "scene_understanding": 0.87,
            "temporal_understanding": 0.82,
            "reasoning": 0.85,
            "hallucination_rate": 0.08,
            "json_reliability": 0.91,
            "inference_time_sec": 5.1
        }
    },
    "VideoLLaMA2": {
        "parameters": "7B (Mistral/Qwen) / 72B",
        "vram_usage": "16 GB (7B)",
        "supported_inputs": "Video Spatio-Temporal Tokens",
        "video_support": "Native Video Spatio-Temporal Encoder",
        "ocr_capability": "Moderate",
        "scene_reasoning": "High (Action & Video Description)",
        "json_generation": "86.0% Reliable",
        "license": "Non-Commercial / Research",
        "community_maturity": "Moderate",
        "ease_of_integration": "Complex (Custom Video Sampler repo)",
        "strengths": "Native spatio-temporal video representation.",
        "weaknesses": "Weaker fine-grained OCR text extraction.",
        "eval_scores": {
            "semantic_accuracy": 0.81,
            "human_agreement": 0.79,
            "scene_understanding": 0.88,
            "temporal_understanding": 0.89,
            "reasoning": 0.80,
            "hallucination_rate": 0.11,
            "json_reliability": 0.86,
            "inference_time_sec": 7.4
        }
    },
    "InternVideo2": {
        "parameters": "6B / 1B Backbone",
        "vram_usage": "24 GB",
        "supported_inputs": "Video Clips (Audio-Visual Masked Autoencoder)",
        "video_support": "Native SOTA Video Encoder",
        "ocr_capability": "Basic",
        "scene_reasoning": "Very High for Video Action",
        "json_generation": "82.0% Reliable",
        "license": "Research Only",
        "community_maturity": "Moderate",
        "ease_of_integration": "Complex",
        "strengths": "Top benchmark scores on Kinetics & VideoQA.",
        "weaknesses": "Difficult setup, non-standard LLM chat interface.",
        "eval_scores": {
            "semantic_accuracy": 0.82,
            "human_agreement": 0.78,
            "scene_understanding": 0.90,
            "temporal_understanding": 0.91,
            "reasoning": 0.81,
            "hallucination_rate": 0.12,
            "json_reliability": 0.82,
            "inference_time_sec": 8.1
        }
    }
}
