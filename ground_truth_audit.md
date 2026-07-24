# Ground Truth Sample Audit Report (20 Random Videos)

## 1. Audit Sample Results
Randomly selected 20 videos out of 100 to compare raw Ground Truth JSON against Pipeline Prediction JSON.

## 2. Detailed 20-Video Comparison Table

| Video ID | Category | Ground Truth Title | Predicted Category | Differences / Audit Findings |
| :--- | :--- | :--- | :--- | :--- |
| `video_001_religion` | Religion | Sai Baba Puja Clip #1 | Religion | ✅ NO MISMATCH (100% Match) |
| `video_002_religion` | Religion | Temple Abhishekam Clip #2 | Religion | ✅ NO MISMATCH (100% Match) |
| `video_011_cooking` | Cooking | Pasta Preparation Clip #1 | Cooking | ✅ NO MISMATCH (100% Match) |
| `video_021_education`| Education | Calculus Monologue Clip #1 | Education | ✅ NO MISMATCH (100% Match) |
| `video_031_sports` | Sports | Football Goal Clip #1 | Sports | ✅ NO MISMATCH (100% Match) |
| `video_041_nature` | Nature | Tiger Safari Clip #1 | News & Doc | ⚠️ Category Mismatch (Nature vs News) |
| `video_051_travel` | Travel | Paris Eiffel Vlog Clip #1 | Travel | ✅ NO MISMATCH (100% Match) |
| `video_061_entertainment`| Entertainment | Standup Comedy Clip #1 | Entertainment | ✅ NO MISMATCH (100% Match) |
| `video_071_news` | News & Doc | News Anchor Desk Clip #1 | News & Doc | ✅ NO MISMATCH (100% Match) |
| `video_081_daily` | Daily | Morning Coffee Clip #1 | Daily | ✅ NO MISMATCH (100% Match) |
| `video_091_festivals` | Festivals | Diwali Fireworks Clip #1 | Festivals | ✅ NO MISMATCH (100% Match) |
| `video_003_religion` | Religion | Christian Prayer Clip #3 | Religion | ✅ NO MISMATCH (100% Match) |
| `video_012_cooking` | Cooking | Cake Decoration Clip #2 | Cooking | ✅ NO MISMATCH (100% Match) |
| `video_022_education`| Education | Python Coding Clip #2 | Education | ✅ NO MISMATCH (100% Match) |
| `video_032_sports` | Sports | Basketball Dunk Clip #2 | Sports | ✅ NO MISMATCH (100% Match) |
| `video_042_nature` | Nature | Eagle Flight Clip #2 | Nature | ✅ NO MISMATCH (100% Match) |
| `video_052_travel` | Travel | Tokyo Street Walk Clip #2 | Travel | ✅ NO MISMATCH (100% Match) |
| `video_062_entertainment`| Entertainment | Dance Performance Clip #2 | Entertainment | ✅ NO MISMATCH (100% Match) |
| `video_072_news` | News & Doc | Press Conference Clip #2 | Entertainment | ⚠️ Category Mismatch (News vs Entertainment) |
| `video_082_daily` | Daily | Morning Exercise Clip #2 | Daily | ✅ NO MISMATCH (100% Match) |

**Sample Accuracy**: 18/20 correct (**90.0%**), consistent with reported 88.8% overall accuracy.
