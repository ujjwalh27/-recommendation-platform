# System Architecture

## High-Level Architecture

The Recommendation Platform follows a layered architecture.

```
                    User
                      │
                      ▼
             React Frontend
                      │
                      ▼
             Spring Boot APIs
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
 Recommendation Engine      Analytics Engine
          │                       │
          └───────────┬───────────┘
                      ▼
                PostgreSQL
                      │
                      ▼
                    Redis
```

---

# Architecture Layers

## Presentation Layer

Responsible for displaying the application to the user.

Components include:

- Home Page
- Video Feed
- Video Card
- Video Player
- Analytics Panel

---

## Behaviour Layer

Captures every interaction performed by the user.

Examples:

- Play
- Pause
- Seek
- Replay
- Completion
- Like
- Save
- Share

---

## Session Layer

Groups user actions into meaningful watch sessions.

Responsibilities:

- Start Session
- Update Session
- End Session
- Calculate Watch Time
- Calculate Completion

---

## Recommendation Layer

Responsible for selecting the best videos.

Pipeline:

User Behaviour

↓

Interest Profile

↓

Candidate Generation

↓

Business Rules

↓

Ranking Engine

↓

Final Feed

---

## Backend Layer

Spring Boot services expose REST APIs for:

- Users
- Videos
- Sessions
- Behaviour Events
- Recommendations

---

## Database Layer

Stores persistent information including:

- Users
- Videos
- Behaviour Events
- Watch Sessions
- Interest Profiles

---

## Cache Layer

Redis stores:

- Recommendation Cache
- Trending Videos
- User Sessions
- Frequently Requested Feeds

---

# Data Flow

```
User

↓

Video Feed

↓

Video Player

↓

Behaviour Tracker

↓

Watch Session Manager

↓

Backend API

↓

PostgreSQL

↓

Recommendation Engine

↓

Updated Feed
```

---

# Design Principles

The system is designed using:

- Separation of Concerns
- Feature-Based Architecture
- Layered Backend
- Modular Components
- Scalable APIs
- Event-Driven Behaviour Tracking

---

# Future Expansion

Future enhancements include:

- AI Ranking Models
- Real-Time Recommendations
- Collaborative Filtering
- Content-Based Filtering
- Hybrid Recommendation Engine
- A/B Testing
- Analytics Dashboard