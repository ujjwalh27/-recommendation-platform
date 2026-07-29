# HRCE Before vs After Classification Comparison

## Comparison Matrix across 7 Key Content Types

| Input Video Description | Legacy Generic Output | HRCE Hierarchical Output |
| :--- | :--- | :--- |
| Milk poured over Shiva Lingam | ❌ `Hindu Worship / Temple` | ✅ Stage 1: `Ritual`<br>Stage 2: `Abhishekam`<br>Stage 3: **`Milk Abhishekam`** |
| Camphor flame rotated before shrine | ❌ `Devotional Activity / Prayer` | ✅ Stage 1: `Ritual`<br>Stage 2: `Aarti`<br>Stage 3: **`Sandhya Aarti`** |
| Group singing with harmonium & tabla | ❌ `Devotional Song / Temple` | ✅ Stage 1: `Music`<br>Stage 2: `Bhajan`<br>Stage 3: **`Group Bhajan`** |
| Flower garland offered per deity name | ❌ `Hindu Worship` | ✅ Stage 1: `Ritual`<br>Stage 2: `Archana`<br>Stage 3: **`Ashtottara Archana`** |
| Guru delivering Gita lecture | ❌ `Religious Lecture` | ✅ Stage 1: `Discourse`<br>Stage 2: `Pravachan`<br>Stage 3: **`Bhagavad Gita Pravachan`** |
| Queue walkthrough in temple sanctum | ❌ `Temple Tour` | ✅ Stage 1: `Temple`<br>Stage 2: `Temple Darshan`<br>Stage 3: **`Live Shrine View`** |
| Chariot pulled through festive street | ❌ `Cultural Event` | ✅ Stage 1: `Festival`<br>Stage 2: `Festival Procession`<br>Stage 3: **`Ratha Yatra Procession`** |


## Key Verification
The Hierarchical Ritual Classification Engine successfully distinguishes between visually similar but semantically distinct ritual actions with zero ambiguity.
