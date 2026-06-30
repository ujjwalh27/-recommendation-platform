# Watch Session Management

## Overview

A Watch Session represents the complete interaction between a user and a single video.

Instead of storing every event independently, related behaviour events are grouped into one session. This provides a structured summary of user engagement and becomes the primary input for recommendation algorithms.

A watch session begins when a user starts watching a video and ends when the video finishes or the user leaves the session.

---

# Objectives

The Watch Session module is responsible for:

- Starting a watch session
- Maintaining session state
- Updating watch statistics
- Recording engagement metrics
- Ending sessions
- Providing summarized data to the recommendation engine

---

# Session Lifecycle

```
User Opens Video

↓

Session Created

↓

Video Starts Playing

↓

Behaviour Events

↓

Session Updated

↓

Video Ends / User Leaves

↓

Session Closed

↓

Stored in Database
```

---

# Session Creation

A new session is created when:

- The user presses Play for the first time
- The video becomes active in the feed (future enhancement)

Current implementation:

```
WatchSessionManager.start()
```

---

# Session State

A watch session can exist in one of the following states.

| State | Description |
|--------|-------------|
| PLAYING | Video is actively playing |
| PAUSED | Playback paused |
| ENDED | Video finished |
| ABANDONED | User left before completion (future) |

---

# Session Object

Current session structure:

```javascript
{
    sessionId,
    userId,
    videoId,

    title,
    creator,
    category,

    state,

    startedAt,
    endedAt,

    duration,

    watchTime,
    completion,

    playCount,
    pauseCount,
    seekCount,
    replayCount,

    liked,
    saved,
    shared,

    events
}
```

---

# Session Statistics

Each session continuously updates the following metrics.

## Watch Time

Amount of time the user watched.

Example:

```
watchTime = 26.4 seconds
```

---

## Completion Percentage

Measures how much of the video has been watched.

Formula:

```
Completion %

=

Watch Time

─────────────── × 100

Video Duration
```

---

## Play Count

Number of times playback started.

---

## Pause Count

Number of pauses during playback.

---

## Seek Count

Number of seeking operations.

---

## Replay Count

Number of complete replays.

---

## Engagement

Future versions will include:

- Likes
- Saves
- Shares
- Comments

---

# Session Updates

Behaviour events continuously update the active session.

Example:

```
PLAY

↓

State = PLAYING

↓

WATCH_PROGRESS

↓

Watch Time Updated

↓

PAUSE

↓

Pause Count++

↓

PLAY

↓

Continue Session

↓

ENDED

↓

Session Closed
```

---

# Relationship with Behaviour Tracking

BehaviourTracker captures raw events.

WatchSessionManager transforms those events into meaningful statistics.

Architecture:

```
VideoPlayer

↓

BehaviourTracker

↓

WatchSessionManager

↓

Analytics Dashboard

↓

Recommendation Engine
```

---

# Relationship with Recommendation Engine

The recommendation engine will primarily use session summaries instead of raw events.

Example:

```
Session

↓

Completion = 96%

Replay = 2

Liked = Yes

Saved = Yes

↓

Increase Interest Score
```

Example:

```
Session

↓

Completion = 8%

Skipped

↓

Decrease Interest Score
```

---

# Future Database Table

Table:

```
watch_sessions
```

Example columns:

| Column | Description |
|---------|-------------|
| session_id | Unique session |
| user_id | User |
| video_id | Video |
| started_at | Start timestamp |
| ended_at | End timestamp |
| completion | Completion % |
| watch_time | Seconds watched |
| replay_count | Number of replays |
| liked | Boolean |
| saved | Boolean |
| shared | Boolean |

---

# Session Workflow

```
User

↓

Play Video

↓

Create Session

↓

Track Behaviour

↓

Update Session

↓

End Session

↓

Save Session

↓

Update User Interest Profile

↓

Generate Better Recommendations
```

---

# Future Enhancements

The Watch Session Manager will later support:

- Resume previous sessions
- Multiple devices
- Offline synchronization
- Real-time session streaming
- Background synchronization
- Session expiration
- Session recovery

---

# Design Principles

The Watch Session module follows:

- Single Responsibility Principle
- Event-driven updates
- Immutable session history
- Real-time statistics
- Backend synchronization

---

# Summary

The Watch Session Manager converts low-level user behaviour into high-level engagement metrics.

These metrics become the primary source of truth for recommendation generation, analytics, and user interest profiling.