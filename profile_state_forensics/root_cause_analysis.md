# Forensic Root Cause Analysis: Live User Interest Profile Oscillation & Fallback

## Executive Summary

- **ROOT CAUSE**: Dual Event Idempotency Key Mismatch between button clicks (`handleLikeClick`) and auto-scroll session cleanup (`submitSessionFeedback`) in [VideoCard.jsx](file:///Users/ujjwalhkumar/Documents/hello_flutter/recommendation-platform/frontend/src/features/feed/VideoCard.jsx).
- **WHY UNIT TESTS MISSED IT**: Isolated backend unit tests passed single synthetic events with fixed `event_id`s in controlled sequence without simulating the React component lifecycle where unmounting / scrolling deactivation (`isActive = false`) triggers an uncoordinated second `POST /feedback` HTTP request with a different `event_id` for the same video.
- **AFFECTED COMPONENTS**:
  - `frontend/src/features/feed/VideoCard.jsx` (`handleLikeClick` vs `submitSessionFeedback`)
  - `src/recommender/profile_store.py` (`process_event` idempotency key resolution)
- **FIX IMPLEMENTED**:
  1. Enforced deterministic, state-pinned event ID generation (`evt_{userId}_{videoId}_{isLiked}_{isSaved}`) across both button clicks and session completion handlers in `VideoCard.jsx`.
  2. Guarded `submitSessionFeedback` so it only fires when a meaningful state change occurs, suppressing duplicate unmount requests.
  3. Pinned `UserInterestProfileStore` to track `user_video_states` for exact delta recalculation rather than compounding raw event penalties.

---

## Detailed Step-by-Step Sequence of the Bug

1. **User Clicks LIKE on Video A**:
   - `handleLikeClick` in `VideoCard.jsx` generates `eventId: evt_like_user_1_video_A_true_1786535...`.
   - Payload sent to `POST /feedback`: `{ isLiked: true, watchCompletionRate: 0.05 }`.
   - Backend `process_event` processes `evt_like_...`, calculates `event_score = +3.0` (or `+5.0`), updates `raw_scores["Aarti"] = 3.0`, and calculates L1 normalized interest `interests["Aarti"] = 100.0%`.
   - `handleFeedbackSubmitted` in `VideoFeed.jsx` fetches `getUserProfile()`: Profile displays **`Aarti: 100.0%`**.

2. **User Scrolls Down to Video B**:
   - Video A component state changes to `isActive = false`.
   - `VideoCard.jsx` `useEffect` cleanup hook fires `submitSessionFeedback()`.
   - `submitSessionFeedback()` constructs a **SECOND** `POST /feedback` HTTP request for Video A.
   - `submitSessionFeedback()` generated a **DIFFERENT** event ID string: `eventId: evt_user_1_video_A_true_false_0.1`.
   - Because `evt_user_1_video_A_true_false_0.1` did NOT match `evt_like_user_1_video_A_true_1786535...`, the backend idempotency check failed to recognize it as a duplicate event.
   - Backend executed `process_event` for this second request:
     - `watchCompletionRate` was `0.05` ($< 0.20$).
     - `is_final = true`.
     - `SKIP_WEIGHT = -5.0` was applied in addition to `LIKE_WEIGHT = +3.0`.
     - Total `event_score` evaluated to `-2.0` (or `score_delta = -5.0`).
     - `raw_scores["Aarti"]` WAS PENALIZED / REDUCED BY `-5.0`!
     - `raw_scores["Aarti"]` fell to $\le 0.0$, pruning `Aarti` from `raw_scores`.
   - `submitSessionFeedback()` completed and called `getUserProfile()`.
   - Profile vector displayed on frontend fell back to **`0.0%` / Cold Start**!

3. **User Scrolls Back Up to Video A**:
   - Video A becomes active (`isActive = true`).
   - Interacting or scrolling again sends another payload, producing positive points, causing the vector score to jump up to `100.0%` again.
   - This produced the exact oscillation reported by users: `100% -> 0% -> 100% -> 0%` during feed navigation.
