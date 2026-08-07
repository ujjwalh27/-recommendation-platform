# Reasoning Trace Examples & Provenance Demonstrations

## Example 1: `lighting` (Warm / Oil Lamp Lit)

```json
{
  "value": "Warm / Oil Lamp Lit",
  "confidence": 0.93,
  "evidence": [
    {
      "source": "YOLO",
      "value": "detected objects [lamp, diya, flame]"
    },
    {
      "source": "MiniCPM",
      "value": "summary described 'flame'"
    },
    {
      "source": "AST",
      "value": "audio event 'bells'"
    }
  ],
  "rules": [
    "RULE_LIGHTING_001"
  ],
  "reason": "Multiple oil lamps detected by YOLO and flame worship descriptions in MiniCPM."
}
```

### Human-Readable Trace:
> `Field: Lighting -> Value: Warm / Oil Lamp Lit | Confidence: 0.93 | Applied Rules: [RULE_LIGHTING_001] | Evidence: ✓ [YOLO] detected objects [lamp, diya, flame] | ✓ [MiniCPM] summary described 'flame' | ✓ [AST] audio event 'bells'`

---

## Example 2: `environment` (Temple Sanctum)

```json
{
  "value": "Temple Sanctum",
  "confidence": 0.94,
  "evidence": [
    {
      "source": "CLIP",
      "value": "classified scene as temple_sanctum"
    },
    {
      "source": "YOLO",
      "value": "detected objects [lamp, altar, statue]"
    },
    {
      "source": "MiniCPM",
      "value": "summary described 'shrine'"
    }
  ],
  "rules": [
    "RULE_ENV_001"
  ],
  "reason": "CLIP temple classification, YOLO altar/lamp objects, and MiniCPM sanctum narrative confirm an inner shrine."
}
```

### Human-Readable Trace:
> `Field: Environment -> Value: Temple Sanctum | Confidence: 0.94 | Applied Rules: [RULE_ENV_001] | Evidence: ✓ [CLIP] classified scene as temple_sanctum | ✓ [YOLO] detected objects [lamp, altar, statue] | ✓ [MiniCPM] summary described 'shrine'`

---

## Example 3: `emotional_tone` (Solemn & Reverent)

```json
{
  "value": "Solemn & Reverent",
  "confidence": 0.91,
  "evidence": [
    {
      "source": "AST",
      "value": "audio event 'bells'"
    },
    {
      "source": "YOLO",
      "value": "detected objects [lamp]"
    }
  ],
  "rules": [
    "RULE_TONE_002"
  ],
  "reason": "Ringing ceremonial bells and lit flame lamps evoke deep reverence."
}
```

### Human-Readable Trace:
> `Field: Emotional Tone -> Value: Solemn & Reverent | Confidence: 0.91 | Applied Rules: [RULE_TONE_002] | Evidence: ✓ [AST] audio event 'bells' | ✓ [YOLO] detected objects [lamp]`
