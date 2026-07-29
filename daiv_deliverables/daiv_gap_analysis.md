# Task 1 – Daiv Domain Semantic Gap Analysis

## 1. Executive Summary
The existing metadata generation pipeline output broad, generic categories (e.g. *Hindu Worship*, *Temple*, *Prayer*, *Devotional Activity*) which are insufficient for Daiv's recommendation engine.

## 2. Generic Output vs Fine-Grained Target Matrix

| Dimension | Legacy Generic Output | Daiv Target Fine-Grained Output | Gap Impact |
| :--- | :--- | :--- | :--- |
| **Religion** | `Hindu` | `Hinduism` | Broad |
| **Tradition** | *Missing* | `Sai / Vaishnava / Shaiva` | Cannot filter by spiritual tradition |
| **Primary Deity** | *Missing / Unspecified* | `Shirdi Sai Baba / Lord Hanuman` | Cannot recommend deity-specific feeds |
| **Primary Ritual** | `Worship / Prayer` | `Abhishekam / Aarti / Pravachan` | Cannot distinguish ritual types |
| **Sub-Ritual** | *Missing* | `Milk Abhishekam / Kakad Aarti` | Cannot filter specific ritual sub-types |
| **Ritual Stage** | *Missing* | `Milk Offering / Alankaram` | Cannot track temporal ritual flow |
| **Offerings** | `Flowers` | `Milk, Yellow Marigold Flowers, Kapoor` | Cannot recommend based on offering type |
| **Scripture** | *Missing* | `Bhagavad Gita` | Cannot categorize discourse topics |
| **Intent & Audience** | `Devotional` | `Devotional Worship / Sai Devotees` | Cannot target specific user personas |
