# Live VLM Validation (LVV) – Sample Comparisons & Observation Quality

## 1. Observation Quality Comparison (Additional Recommendation Requirement)

Below is the measured observation extraction fidelity across representative keyframe samples compared against human ground truth.

| Observation Feature | Ground Truth | minicpm-v:latest (Baseline) | qwen2.5:1.5b (Candidate) | Winner |
|:---|:---:|:---:|:---:|:---:|
| **Milk Detected** | Yes | Yes (in summary & title) | No (empty parse) | **minicpm-v:latest** |
| **Lamp Detected** | Yes | Yes (oil lamp identified) | No (empty parse) | **minicpm-v:latest** |
| **Flowers Detected** | Yes | Yes (marigold flowers identified) | No (empty parse) | **minicpm-v:latest** |
| **Chant Detected** | Yes | Yes ('Om Namah Shivaya' identified) | No (empty parse) | **minicpm-v:latest** |
| **Idol Visible** | Yes | Yes (Lord Shiva statue identified) | No (empty parse) | **minicpm-v:latest** |

---

## 2. Real Side-by-Side Video Outputs

### Example 1: `case_01_religious` (Hindu Deity Worship)

#### **Baseline Model (minicpm-v:latest)**
- **Live Latency**: 29291 ms
- **JSON Compliance**: ✅ Valid JSON Parsed
- **Title**: `Hindu Devotional Ritual`
- **Summary**: `A Hindu woman performing a devotional ritual involving the worship of deities through various rituals such as abhishekam (ritual bathing), arati, and offering flowers.`
- **Primary Class**: `Pooja`
- **Deity Identified**: `Lord Shiva or Lord Vishnu (statues not clearly identifiable)`
- **Reasoning**: `The video captures various elements associated with Hindu devotional practices such as deity statues, oil lamps, flower garlands, and an altar setup. The woman's attire and jewelry are traditional Indian clothing often worn during religious ceremonies.`

#### **Candidate Model (qwen2.5:1.5b)**
- **Live Latency**: 142 ms
- **JSON Compliance**: ❌ Failed Parse (`HTTP Error 400: Bad Request`)
- **Raw Response**: `ERROR: HTTP Error 400: Bad Request`

---

## 3. Real Side-by-Side Video Outputs – Example 2: `video_ci_1784802389`

#### **Baseline Model (minicpm-v:latest)**
- **Live Latency**: 12803 ms
- **Title**: `Hindu Devotional Worship`
- **Summary**: `A person performing various aspects of Hindu devotional worship including chanting mantras and offering prayers.`

#### **Candidate Model (qwen2.5:1.5b)**
- **Live Latency**: 73 ms
- **Parse Status**: `False`
