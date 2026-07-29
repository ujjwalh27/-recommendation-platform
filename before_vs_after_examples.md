# SRCDE Before vs After Classification Examples

## Example 1: Water Abhishekam

### ❌ Before (Descriptive Paragraph Output)
> *"The video shows a man performing religious rituals in a temple using water and flowers..."*

### ✅ After (SRCDE Target JSON Schema Output)
```json
{
  "classification": {
    "content_type": "Ritual",
    "primary_class": "Abhishekam",
    "sub_class": "Water Abhishekam"
  },
  "confidence": 0.92,
  "observations": {
    "people": [
      "priest",
      "devotee"
    ],
    "objects": [
      "lingam",
      "water vessel",
      "kalash"
    ],
    "actions": [
      "pouring water"
    ],
    "speech": [
      "Om Namah Shivaya"
    ],
    "ocr": [
      "Water Abhishekam"
    ]
  },
  "reasoning": [
    "Water vessel poured over deity without milk/curd"
  ],
  "alternative_predictions": [
    {
      "class": "Pooja",
      "confidence": 0.05
    },
    {
      "class": "Archana",
      "confidence": 0.01
    }
  ],
  "explanation": "Strong evidence for Abhishekam (Water Abhishekam). Confirmed with 92% confidence based on multimodal vision, speech, and OCR observation rules."
}
```

---

## Example 2: Milk Abhishekam

### ❌ Before (Descriptive Paragraph Output)
> *"A priest pouring milk over a statue in a Hindu temple with prayers..."*

### ✅ After (SRCDE Target JSON Schema Output)
```json
{
  "classification": {
    "content_type": "Ritual",
    "primary_class": "Abhishekam",
    "sub_class": "Milk Abhishekam"
  },
  "confidence": 0.94,
  "observations": {
    "people": [
      "priest",
      "devotee"
    ],
    "objects": [
      "idol",
      "milk",
      "water vessel",
      "lamp"
    ],
    "actions": [
      "pouring milk",
      "offering flowers"
    ],
    "speech": [
      "Om Sai Ram"
    ],
    "ocr": [
      "Milk Abhishekam Live"
    ]
  },
  "reasoning": [
    "Liquid (milk) poured over deity in shrine environment detected",
    "Priest performing ritual action",
    "Temple environment detected"
  ],
  "alternative_predictions": [
    {
      "class": "Pooja",
      "confidence": 0.05
    },
    {
      "class": "Archana",
      "confidence": 0.01
    }
  ],
  "explanation": "Strong evidence for Abhishekam (Milk Abhishekam). Confirmed with 94% confidence based on multimodal vision, speech, and OCR observation rules."
}
```

---

## Example 3: Sandhya Aarti

### ❌ Before (Descriptive Paragraph Output)
> *"Traditional religious ritual with lamps and singing..."*

### ✅ After (SRCDE Target JSON Schema Output)
```json
{
  "classification": {
    "content_type": "Ritual",
    "primary_class": "Aarti",
    "sub_class": "Sandhya Aarti"
  },
  "confidence": 0.95,
  "observations": {
    "people": [
      "priest",
      "devotee"
    ],
    "objects": [
      "camphor",
      "aarti plate",
      "lamp",
      "flame"
    ],
    "actions": [
      "circular waving motion",
      "waving flame"
    ],
    "speech": [
      "Aarti Kije Hanuman Lala Ki"
    ],
    "ocr": [
      "Evening Sandhya Aarti"
    ]
  },
  "reasoning": [
    "Evening Sandhya Aarti confirmed by flame rotation and OCR/speech text"
  ],
  "alternative_predictions": [
    {
      "class": "Pooja",
      "confidence": 0.05
    },
    {
      "class": "Archana",
      "confidence": 0.01
    }
  ],
  "explanation": "Strong evidence for Aarti (Sandhya Aarti). Confirmed with 95% confidence based on multimodal vision, speech, and OCR observation rules."
}
```
