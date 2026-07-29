# Daiv Recommendation Engine Integration Architecture

## 1. Recommendation Filter Keys
The hierarchical metadata generator exports explicit filter keys for Daiv's recommendation retrieval engine:

```json
"recommendation_filter_keys": {
  "deity_key": "hinduism:sai:shirdi_sai_baba",
  "ritual_key": "abhishekam:milk_abhishekam",
  "festival_key": "guru_purnima",
  "intent_key": "devotional_worship_&_prayer"
}
```

## 2. Direct Query Filtering Examples
- **Deity-Specific Feed**: Query videos where `deity_key == "hinduism:sai:shirdi_sai_baba"`.
- **Ritual-Specific Feed**: Query videos where `ritual_key == "abhishekam:milk_abhishekam"`.
- **Discourse/Teaching Feed**: Query videos where `intent_key == "teaching_&_discourse"`.
