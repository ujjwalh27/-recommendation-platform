import os
import sys
import json
import time
import threading
import copy
from typing import Dict, Any, List, Optional
from src.utils.paths import get_path
from src.users.personas import PERSONAS, get_persona_baseline_scores

class UserInterestProfileStore:
    """
    Single Authoritative Source of Truth for User Interest Profiles.
    
    Provides thread-safe atomic updates, monotonically increasing versioning,
    per-video session delta tracking, cold-start persona baselines, multi-vector
    interest derivation, event sourcing, idempotency validation, snapshotting,
    and corrupt state recovery.
    """
    
    CATEGORY_CANONICAL_MAP = {
        "Aarti": "Aarti",
        "Devotional Aarti": "Aarti",
        "Flame Worship & Lamp Ritual": "Aarti",
        "Flame Worship": "Aarti",
        
        "Abhishekam": "Abhishekam",
        "Milk / Panchamrutha / Water Abhishekam": "Abhishekam",
        "Panchamrutha Abhishekam": "Abhishekam",
        "Water Abhishekam": "Abhishekam",
        
        "Pooja": "Pooja",
        "Devotional Ritual & Worship": "Pooja",
        "Shrine Worship": "Pooja",
        "Temple Worship": "Pooja",
        
        "Bhajan": "Bhajan",
        "Devotional Hymns & Songs": "Bhajan",
        "Kirtan / Nama Sankeerthana": "Bhajan",
        "Kirtan": "Bhajan",
        "Devotional Singing": "Bhajan",
        
        "Festival Processions": "Festival Processions",
        "Sacred Chariot & Street Procession": "Festival Processions",
        "Procession": "Festival Processions",
        "Chariot Procession": "Festival Processions",
        
        "Meditation / Chanting": "Meditation / Chanting",
        "Silent Reflection & Mantra Japa": "Meditation / Chanting",
        "Chanting": "Meditation / Chanting",
        "Meditation": "Meditation / Chanting",
        
        "Homa / Yajna": "Homa / Yajna",
        "Sacred Fire Altar Ritual": "Homa / Yajna",
        "Havan": "Homa / Yajna",
        
        "Annadanam": "Annadanam",
        "Sacred Food Service & Prasad": "Annadanam",
        
        "Pravachan / Spiritual Discourses": "Pravachan / Spiritual Discourses",
        "Spiritual Discourses": "Pravachan / Spiritual Discourses",
        
        "Temple Darshan": "Temple Darshan",
        "Temple Darshan & Deity Viewing": "Temple Darshan",
        "Temple Darshan & Monumental Statues": "Temple Darshan",
        "Temple Darshan & Sanctum View": "Temple Darshan",
        "Any other devotional or temple-related activities": "Temple Darshan"
    }

    LEGACY_KEYS = {"Pooja & Aarti", "Temple Ritual", "Devotion", "Lifestyle & Culture", "Bhajan & Kirtan", "Archana & Mantras", "Entertainment"}

    def __init__(self):
        self._lock = threading.RLock()
        
        self.profiles_path = get_path("datasets/processed/interest_profiles.json")
        self.events_path = get_path("datasets/processed/interaction_events.json")
        self.snapshots_dir = get_path("datasets/processed/profile_snapshots")
        os.makedirs(self.snapshots_dir, exist_ok=True)
        
        self.profiles: Dict[str, Dict[str, Any]] = {}
        self.events: List[Dict[str, Any]] = []
        self.processed_event_ids: set = set()
        self._session_states: Dict[str, Dict[str, Any]] = {}  # Key: "user_id_video_id"
        
        self._load_storage()

    def _load_storage(self):
        """Loads profiles and raw events from disk."""
        with self._lock:
            # Load raw interaction events
            if os.path.exists(self.events_path):
                try:
                    with open(self.events_path, "r", encoding="utf-8") as f:
                        self.events = json.load(f)
                        self.processed_event_ids = {e.get("event_id") for e in self.events if e.get("event_id")}
                except Exception as e:
                    print(f"[ProfileStore] Error loading events: {e}")
                    self.events = []
                    self.processed_event_ids = set()
            else:
                self.events = []
                self.processed_event_ids = set()
                self._persist_events()

            # Load profiles
            if os.path.exists(self.profiles_path):
                try:
                    with open(self.profiles_path, "r", encoding="utf-8") as f:
                        raw_profiles = json.load(f)
                    
                    for uid, prof in raw_profiles.items():
                        if self.validate_integrity(prof):
                            self.profiles[uid] = self._normalize_profile_schema(uid, prof)
                        else:
                            print(f"[ProfileStore] Corrupted profile detected for {uid}. Reconstructing from events...")
                            reconstructed = self._rebuild_profile_from_events_nolock(uid)
                            self.profiles[uid] = reconstructed
                except Exception as e:
                    print(f"[ProfileStore] Error loading profiles: {e}")
                    self.profiles = {}
            else:
                self.profiles = {}
                self._persist_profiles()

    def _normalize_profile_schema(self, user_id: str, prof: Dict[str, Any]) -> Dict[str, Any]:
        """Ensures all standard profile keys exist with valid baseline and schema."""
        persona = prof.get("persona", "Devotional Practitioner")
        baseline = get_persona_baseline_scores(persona)
        
        raw_scores = prof.get("raw_scores", {})
        if not raw_scores:
            raw_scores = dict(baseline)

        # Consolidate legacy or subcategory keys into canonical main categories
        consolidated = {}
        for k, v in raw_scores.items():
            c_k = self.CATEGORY_CANONICAL_MAP.get(k, k)
            if c_k not in self.LEGACY_KEYS:
                consolidated[c_k] = consolidated.get(c_k, 0.0) + float(v)

        total_score = sum(consolidated.values())
        interests = {}
        if total_score > 0.05:
            for k, score in consolidated.items():
                if score > 0.05:
                    interests[k] = round((score / total_score) * 100.0, 1)

        # Deities and Rituals normalized derivation
        deity_raw = prof.get("deity_raw_scores", {})
        deity_interests = {}
        t_deity = sum(deity_raw.values())
        if t_deity > 0:
            for d, s in deity_raw.items():
                deity_interests[d] = round((s / t_deity) * 100.0, 1)

        ritual_raw = prof.get("ritual_raw_scores", {})
        ritual_interests = {}
        t_ritual = sum(ritual_raw.values())
        if t_ritual > 0:
            for r, s in ritual_raw.items():
                ritual_interests[r] = round((s / t_ritual) * 100.0, 1)

        sorted_interests = dict(sorted(interests.items(), key=lambda x: x[1], reverse=True))

        return {
            "user_id": str(user_id),
            "version": int(prof.get("version", 1)),
            "persona": persona,
            "raw_scores": consolidated,
            "category_interests": sorted_interests,
            "interests": sorted_interests,
            "deity_raw_scores": deity_raw,
            "deity_interests": dict(sorted(deity_interests.items(), key=lambda x: x[1], reverse=True)),
            "ritual_raw_scores": ritual_raw,
            "ritual_interests": dict(sorted(ritual_interests.items(), key=lambda x: x[1], reverse=True)),
            "temple_interests": prof.get("temple_interests", {}),
            "creator_affinities": prof.get("creator_affinities", {}),
            "last_event_id": prof.get("last_event_id", None),
            "last_updated": prof.get("last_updated", time.strftime('%Y-%m-%d %H:%M:%S')),
            "metadata": prof.get("metadata", {})
        }

    def validate_integrity(self, profile: Dict[str, Any]) -> bool:
        """Validates that profile contains no NaN, Infinity, negative values, or corrupt structure."""
        if not isinstance(profile, dict):
            return False
        
        user_id = profile.get("user_id")
        if not user_id:
            return False
            
        raw_scores = profile.get("raw_scores", {})
        if not isinstance(raw_scores, dict):
            return False

        for k, v in raw_scores.items():
            if not isinstance(v, (int, float)):
                return False
            if v != v or v == float('inf') or v == float('-inf'):  # NaN check
                return False
            if v < 0:
                return False

        return True

    def get_profile(self, user_id: str, persona: str = "Devotional Practitioner") -> Dict[str, Any]:
        """
        READ-ONLY operation.
        Returns a deep copy of the current authoritative user profile.
        Does NOT mutate profile state.
        """
        with self._lock:
            user_id = str(user_id)
            if user_id not in self.profiles:
                # Cold-start baseline initialization from assigned persona
                baseline = get_persona_baseline_scores(persona)
                total_b = sum(baseline.values())
                interests = {k: round((v / total_b) * 100.0, 1) for k, v in baseline.items()} if total_b > 0 else {}
                sorted_interests = dict(sorted(interests.items(), key=lambda x: x[1], reverse=True))

                self.profiles[user_id] = {
                    "user_id": user_id,
                    "version": 1,
                    "persona": persona,
                    "raw_scores": dict(baseline),
                    "category_interests": sorted_interests,
                    "interests": sorted_interests,
                    "deity_raw_scores": {},
                    "deity_interests": {},
                    "ritual_raw_scores": {},
                    "ritual_interests": {},
                    "temple_interests": {},
                    "creator_affinities": {},
                    "last_event_id": None,
                    "last_updated": time.strftime('%Y-%m-%d %H:%M:%S'),
                    "metadata": {}
                }
                self._persist_profiles()

            prof = self.profiles[user_id]
            print(f"[RECOMMENDATION_PROFILE_READ] user_id={user_id} profile_version={prof['version']} profile_timestamp={prof['last_updated']} profile_source=store")
            return copy.deepcopy(prof)

    def process_event(
        self,
        user_id: str,
        event_id: str,
        event_type: str,
        video_id: str,
        engagement_payload: Dict[str, Any],
        video_meta: Dict[str, Any],
        persona: str = "Devotional Practitioner"
    ) -> Dict[str, Any]:
        """
        Atomically processes a user feedback interaction event using per-video session state deltas.
        """
        with self._lock:
            user_id = str(user_id)
            video_id = str(video_id)

            # Idempotency Check
            if event_id and event_id in self.processed_event_ids:
                print(f"[ProfileStore] Duplicate event_id '{event_id}' ignored (Idempotent).")
                prof = self.profiles.get(user_id, self.get_profile(user_id, persona))
                return {
                    "status": "ignored_duplicate",
                    "event_id": event_id,
                    "user_id": user_id,
                    "profile": copy.deepcopy(prof)
                }

            # Record raw event for event sourcing
            ts = time.strftime('%Y-%m-%d %H:%M:%S')
            raw_event = {
                "event_id": event_id or f"evt_{int(time.time()*1000)}_{user_id}",
                "user_id": user_id,
                "video_id": video_id,
                "event_type": event_type,
                "timestamp": ts,
                "engagement": engagement_payload,
                "video_meta": {
                    "category": video_meta.get("category"),
                    "ritual_family": video_meta.get("ritual_family"),
                    "primary_ritual": video_meta.get("primary_ritual"),
                    "primary_deity": video_meta.get("primary_deity"),
                    "creator": video_meta.get("creator")
                }
            }
            self.events.append(raw_event)
            if event_id:
                self.processed_event_ids.add(event_id)
            self._persist_events()

            # Ensure profile exists
            if user_id not in self.profiles:
                self.get_profile(user_id, persona)

            profile = self.profiles[user_id]
            old_version = profile["version"]
            old_interests = copy.deepcopy(profile["interests"])

            # Extract engagement signals
            watch_completion_rate = float(engagement_payload.get("watch_completion_rate", 0.0))
            replay_count = int(engagement_payload.get("replay_count", 0))
            is_liked = bool(engagement_payload.get("is_liked", False))
            is_saved = bool(engagement_payload.get("is_saved", False))
            is_shared = bool(engagement_payload.get("is_shared", False))
            is_commented = bool(engagement_payload.get("is_commented", False))
            is_final = bool(engagement_payload.get("is_final", False))

            # Explicit Interaction Scoring Formula (Driven strictly by button clicks)
            event_score = 0.0
            if is_liked:
                event_score += 1.5
            if is_saved:
                event_score += 1.5
            if is_shared:
                event_score += 1.5
            if is_commented:
                event_score += 1.0

            # Session State Delta Calculation
            sess_key = f"{user_id}_{video_id}"
            raw_scores = profile["raw_scores"]
            baseline = get_persona_baseline_scores(persona)

            if sess_key in self._session_states:
                prev_score = self._session_states[sess_key].get("event_score", 0.0)
                score_delta = event_score - prev_score
                self._session_states[sess_key]["event_score"] = event_score
            else:
                score_delta = event_score
                self._session_states[sess_key] = {"event_score": event_score, "video_id": video_id}

            # Resolve canonical category
            raw_category = video_meta.get("category", "") or video_meta.get("primary_category", "")
            category = self.CATEGORY_CANONICAL_MAP.get(raw_category, raw_category)
            if not category or category in self.LEGACY_KEYS:
                category = "Temple Darshan"

            # Apply score delta to category raw scores
            if score_delta != 0.0:
                raw_scores[category] = max(0.0, raw_scores.get(category, 0.0) + score_delta)

            # Prune non-baseline scores near zero
            for k in list(raw_scores.keys()):
                if raw_scores[k] <= 0.05:
                    del raw_scores[k]

            profile["raw_scores"] = raw_scores

            # Derive L1 Normalized Category Interests
            total_score = sum(raw_scores.values())
            interests = {}
            if total_score > 0.05:
                for k, s in raw_scores.items():
                    if s > 0.05:
                        interests[k] = round((s / total_score) * 100.0, 1)

            sorted_interests = dict(sorted(interests.items(), key=lambda x: x[1], reverse=True))
            profile["category_interests"] = sorted_interests
            profile["interests"] = sorted_interests

            # Update Primary Deity Interests
            deity = video_meta.get("primary_deity")
            if deity and score_delta != 0.0:
                deity_raw = profile.setdefault("deity_raw_scores", {})
                deity_raw[deity] = max(0.0, deity_raw.get(deity, 0.0) + score_delta)
                t_deity = sum(deity_raw.values())
                if t_deity > 0:
                    d_interests = {d: round((s / t_deity) * 100.0, 1) for d, s in deity_raw.items()}
                    profile["deity_interests"] = dict(sorted(d_interests.items(), key=lambda x: x[1], reverse=True))

            # Update Ritual Family Interests
            ritual = video_meta.get("ritual_family") or video_meta.get("primary_ritual")
            if ritual and score_delta != 0.0:
                ritual_raw = profile.setdefault("ritual_raw_scores", {})
                ritual_raw[ritual] = max(0.0, ritual_raw.get(ritual, 0.0) + score_delta)
                t_ritual = sum(ritual_raw.values())
                if t_ritual > 0:
                    r_interests = {r: round((s / t_ritual) * 100.0, 1) for r, s in ritual_raw.items()}
                    profile["ritual_interests"] = dict(sorted(r_interests.items(), key=lambda x: x[1], reverse=True))

            # Update Creator Affinities
            creator = video_meta.get("creator")
            if creator and score_delta != 0.0:
                affinities = profile.setdefault("creator_affinities", {})
                affinities[creator] = max(0.0, affinities.get(creator, 0.0) + score_delta)

            # Monotonic version increment
            new_version = old_version + 1
            profile["version"] = new_version
            profile["last_event_id"] = raw_event["event_id"]
            profile["last_updated"] = ts

            # Persist profile to disk and create periodic snapshot
            self._persist_profiles()
            if new_version % 5 == 0:
                self._create_snapshot_nolock(user_id)

            # Observability log
            print(f"[USER_PROFILE_UPDATE] user_id={user_id} event_id={raw_event['event_id']} event_type={event_type} "
                  f"version_before={old_version} version_after={new_version} "
                  f"interests_before={old_interests} interests_after={sorted_interests} timestamp={ts}")
            sys.stdout.flush()

            return {
                "status": "applied",
                "event_id": raw_event["event_id"],
                "user_id": user_id,
                "profile": copy.deepcopy(profile)
            }

    def reset_profile(self, user_id: str) -> Dict[str, Any]:
        """Resets a user profile to cold-start baseline state and removes past events for clean event-sourcing."""
        with self._lock:
            user_id = str(user_id)
            ts = time.strftime('%Y-%m-%d %H:%M:%S')

            # Filter out historical events for this user
            removed_event_ids = {e.get("event_id") for e in self.events if e.get("user_id") == user_id and e.get("event_id")}
            self.events = [e for e in self.events if e.get("user_id") != user_id]
            self.processed_event_ids -= removed_event_ids

            # Remove session states for this user
            for k in list(self._session_states.keys()):
                if k.startswith(f"{user_id}_"):
                    del self._session_states[k]

            persona = self.profiles.get(user_id, {}).get("persona", "Devotional Practitioner")
            baseline = get_persona_baseline_scores(persona)
            total_b = sum(baseline.values())
            interests = {k: round((v / total_b) * 100.0, 1) for k, v in baseline.items()} if total_b > 0 else {}
            sorted_interests = dict(sorted(interests.items(), key=lambda x: x[1], reverse=True))

            new_prof = {
                "user_id": user_id,
                "version": 1,
                "persona": persona,
                "raw_scores": dict(baseline),
                "category_interests": sorted_interests,
                "interests": sorted_interests,
                "deity_raw_scores": {},
                "deity_interests": {},
                "ritual_raw_scores": {},
                "ritual_interests": {},
                "temple_interests": {},
                "creator_affinities": {},
                "last_event_id": None,
                "last_updated": ts,
                "metadata": {}
            }
            self.profiles[user_id] = new_prof
            self._persist_profiles()
            self._persist_events()
            return copy.deepcopy(new_prof)

    def rebuild_profile_from_events(self, user_id: str) -> Dict[str, Any]:
        """Event-Sourced Deterministic Profile Recovery."""
        with self._lock:
            return self._rebuild_profile_from_events_nolock(user_id)

    def _rebuild_profile_from_events_nolock(self, user_id: str) -> Dict[str, Any]:
        """Reconstructs profile deterministically by replaying all raw user events."""
        user_events = [e for e in self.events if e.get("user_id") == str(user_id)]
        persona = self.profiles.get(str(user_id), {}).get("persona", "Devotional Practitioner")
        baseline = get_persona_baseline_scores(persona)
        total_b = sum(baseline.values())
        interests = {k: round((v / total_b) * 100.0, 1) for k, v in baseline.items()} if total_b > 0 else {}
        sorted_interests = dict(sorted(interests.items(), key=lambda x: x[1], reverse=True))

        prof = {
            "user_id": str(user_id),
            "version": 1,
            "persona": persona,
            "raw_scores": dict(baseline),
            "category_interests": sorted_interests,
            "interests": sorted_interests,
            "deity_raw_scores": {},
            "deity_interests": {},
            "ritual_raw_scores": {},
            "ritual_interests": {},
            "temple_interests": {},
            "creator_affinities": {},
            "last_event_id": None,
            "last_updated": time.strftime('%Y-%m-%d %H:%M:%S'),
            "metadata": {}
        }
        
        session_scores = {}

        for ev in user_events:
            eng = ev.get("engagement", {})
            v_meta = ev.get("video_meta", {})
            vid = ev.get("video_id", "")
            
            w_comp = float(eng.get("watch_completion_rate", 0.0))
            rep = int(eng.get("replay_count", 0))
            liked = bool(eng.get("is_liked", False))
            saved = bool(eng.get("is_saved", False))
            shared = bool(eng.get("is_shared", False))
            commented = bool(eng.get("is_commented", False))
            is_final = bool(eng.get("is_final", False))

            e_score = 0.0
            if liked: e_score += 1.5
            if saved: e_score += 1.5
            if shared: e_score += 1.5
            if commented: e_score += 1.0

            s_key = f"{user_id}_{vid}"
            r_scores = prof["raw_scores"]

            if s_key in session_scores:
                s_delta = e_score - session_scores[s_key]
                session_scores[s_key] = e_score
            else:
                s_delta = e_score
                session_scores[s_key] = e_score

            raw_cat = v_meta.get("category", "") or v_meta.get("primary_category", "")
            cat = self.CATEGORY_CANONICAL_MAP.get(raw_cat, raw_cat)
            if not cat or cat in self.LEGACY_KEYS:
                cat = "Temple Darshan"

            if s_delta != 0.0:
                r_scores[cat] = max(0.0, r_scores.get(cat, 0.0) + s_delta)

            tot = sum(r_scores.values())
            ints = {}
            if tot > 0.05:
                for k, s in r_scores.items():
                    if s > 0.05:
                        ints[k] = round((s / tot) * 100.0, 1)

            s_ints = dict(sorted(ints.items(), key=lambda x: x[1], reverse=True))
            prof["raw_scores"] = r_scores
            prof["category_interests"] = s_ints
            prof["interests"] = s_ints
            prof["version"] += 1
            prof["last_event_id"] = ev.get("event_id")

        self.profiles[str(user_id)] = prof
        self._persist_profiles()
        return prof

    def _create_snapshot_nolock(self, user_id: str):
        """Saves periodic snapshot file."""
        if user_id in self.profiles:
            prof = self.profiles[user_id]
            snap_path = os.path.join(self.snapshots_dir, f"{user_id}_v{prof['version']}.json")
            with open(snap_path, "w", encoding="utf-8") as f:
                json.dump(prof, f, indent=4)

    def _persist_profiles(self):
        """Atomically persists all profiles to disk."""
        with open(self.profiles_path, "w", encoding="utf-8") as f:
            json.dump(self.profiles, f, indent=4)

    def _persist_events(self):
        """Atomically persists raw events to disk."""
        with open(self.events_path, "w", encoding="utf-8") as f:
            json.dump(self.events, f, indent=4)
