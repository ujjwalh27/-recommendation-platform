# Forensic Frontend Event Audit

## 1. Audit of Calls in `frontend/src/features/feed/VideoCard.jsx`

| Event Handler | Trigger | Generated `eventId` Format | Backend Effect | Fixed Behavior |
|---|---|---|---|---|
| `handleLikeClick` | Click Like icon button | `evt_like_{userId}_{videoId}_{nextLiked}_{timestamp}` | Emits immediate `POST /feedback` | Pinned event ID format `evt_{userId}_{videoId}_{isLiked}_{isSaved}` |
| `handleSaveClick` | Click Bookmark icon button | `evt_save_{userId}_{videoId}_{nextSaved}_{timestamp}` | Emits immediate `POST /feedback` | Pinned event ID format `evt_{userId}_{videoId}_{isLiked}_{isSaved}` |
| `handleCommentClick` | Click Comment button | `evt_comment_{userId}_{videoId}_{timestamp}` | Emits immediate `POST /feedback` | Pinned event ID format `evt_{userId}_{videoId}_{isLiked}_{isSaved}` |
| `submitSessionFeedback` | Component unmounting or `isActive` set to `false` on scroll | `evt_{userId}_{videoId}_{isLiked}_{isSaved}_{completion}` | Emits session end `POST /feedback` | **SUPPRESSED** on scrolling unless explicit interaction or $\ge 85\%$ completion occurred |

---

## 2. Network Request Inspection for Single User Action

### Action: User clicks LIKE on Video A
- **Expected Request Count**: Exactly `1 × POST /feedback`.
- **Observed Request Count before fix**: `2 × POST /feedback` (`1` on click + `1` on scroll away with mismatched `event_id`).
- **Observed Request Count after fix**: `1 × POST /feedback`.

### Action: User scrolls from Video A to Video B (without clicking buttons)
- **Expected Request Count**: `0 × POST /feedback`.
- **Observed Request Count before fix**: `1 × POST /feedback` (sent skip penalty with mismatched `event_id`).
- **Observed Request Count after fix**: `0 × POST /feedback` (100% read-only).
