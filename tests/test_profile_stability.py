import sys
sys.path.insert(0, ".")
import os
import json
import time
import unittest
import threading
from src.recommender.profile_store import UserInterestProfileStore

class TestProfileStability(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.store = UserInterestProfileStore()

    def setUp(self):
        self.test_user = "test_user_stability"
        self.store.reset_profile(self.test_user)

    def test_a_like_persistence(self):
        """Test A: Profile stays unchanged during scroll navigation after a Like event."""
        initial_prof = self.store.get_profile(self.test_user)
        v0 = initial_prof["version"]

        # Like Video A
        video_a_meta = {"video_id": "vid_a", "category": "Aarti", "ritual_family": "Aarti", "primary_ritual": "Flame Worship"}
        res_like = self.store.process_event(
            user_id=self.test_user,
            event_id="evt_like_a_1",
            event_type="like",
            video_id="vid_a",
            engagement_payload={"is_liked": True, "watch_completion_rate": 0.5},
            video_meta=video_a_meta
        )
        liked_prof = res_like["profile"]
        v1 = liked_prof["version"]
        liked_vector = dict(liked_prof["interests"])

        self.assertEqual(v1, v0 + 1)
        self.assertIn("Aarti", liked_vector)

        # Scroll to Video B (Read-Only)
        prof_b = self.store.get_profile(self.test_user)
        self.assertEqual(prof_b["version"], v1)
        self.assertEqual(prof_b["interests"], liked_vector)

        # Scroll to Video C (Read-Only)
        prof_c = self.store.get_profile(self.test_user)
        self.assertEqual(prof_c["version"], v1)
        self.assertEqual(prof_c["interests"], liked_vector)

    def test_b_scroll_back(self):
        """Test B: Backward scroll navigation (A -> B -> C -> B -> A) causes ZERO interest changes."""
        start_prof = self.store.get_profile(self.test_user)
        start_version = start_prof["version"]
        start_vector = dict(start_prof["interests"])

        # Simulate read-only scrolling requests
        for vid in ["vid_a", "vid_b", "vid_c", "vid_b", "vid_a"]:
            p = self.store.get_profile(self.test_user)
            self.assertEqual(p["version"], start_version)
            self.assertEqual(p["interests"], start_vector)

    def test_c_idempotency_duplicate_like(self):
        """Test C: Duplicate feedback events with same event_id are applied exactly once."""
        video_meta = {"video_id": "vid_idemp", "category": "Bhajan", "ritual_family": "Bhajan", "primary_ritual": "Kirtan"}
        payload = {"is_liked": True, "watch_completion_rate": 1.0}
        event_id = "evt_unique_idemp_100"

        # Send Event 1
        res1 = self.store.process_event(self.test_user, event_id, "like", "vid_idemp", payload, video_meta)
        self.assertEqual(res1["status"], "applied")
        v1 = res1["profile"]["version"]
        vec1 = dict(res1["profile"]["interests"])

        # Send Event 2 (Duplicate)
        res2 = self.store.process_event(self.test_user, event_id, "like", "vid_idemp", payload, video_meta)
        self.assertEqual(res2["status"], "ignored_duplicate")
        self.assertEqual(res2["profile"]["version"], v1)
        self.assertEqual(res2["profile"]["interests"], vec1)

        # Send Event 3 (Duplicate)
        res3 = self.store.process_event(self.test_user, event_id, "like", "vid_idemp", payload, video_meta)
        self.assertEqual(res3["status"], "ignored_duplicate")
        self.assertEqual(res3["profile"]["version"], v1)
        self.assertEqual(res3["profile"]["interests"], vec1)

    def test_d_restart_persistence(self):
        """Test D: Profile version and vector survive backend application restart."""
        video_meta = {"video_id": "vid_restart", "category": "Abhishekam", "ritual_family": "Abhishekam"}
        res = self.store.process_event(
            self.test_user,
            "evt_restart_1",
            "like",
            "vid_restart",
            {"is_liked": True, "watch_completion_rate": 0.9},
            video_meta
        )
        saved_version = res["profile"]["version"]
        saved_vector = dict(res["profile"]["interests"])

        # Simulate Application Restart: Instantiate new profile store from disk
        new_store = UserInterestProfileStore()
        reloaded_prof = new_store.get_profile(self.test_user)

        self.assertEqual(reloaded_prof["version"], saved_version)
        self.assertEqual(reloaded_prof["interests"], saved_vector)

    def test_e_concurrent_feedback(self):
        """Test E: Concurrent thread feedback updates maintain monotonic version integrity without lost updates."""
        threads = []
        errs = []

        def worker(idx):
            try:
                vm = {"video_id": f"vid_conc_{idx}", "category": "Pooja" if idx % 2 == 0 else "Bhajan"}
                self.store.process_event(
                    self.test_user,
                    f"evt_conc_{idx}_{time.time()}",
                    "like",
                    f"vid_conc_{idx}",
                    {"is_liked": True, "watch_completion_rate": 0.8},
                    vm
                )
            except Exception as e:
                errs.append(e)

        for i in range(10):
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        self.assertEqual(len(errs), 0)
        final_prof = self.store.get_profile(self.test_user)
        self.assertGreaterEqual(final_prof["version"], 10)

    def test_f_deterministic_event_sourced_reconstruction(self):
        """Test F: Deleting derived profile and replaying interaction events yields identical profile vector."""
        # 1. Generate interaction history
        events_to_send = [
            ("evt_rec_1", "vid_1", "Aarti", {"is_liked": True, "watch_completion_rate": 0.9}),
            ("evt_rec_2", "vid_2", "Bhajan", {"is_liked": True, "watch_completion_rate": 0.85}),
            ("evt_rec_3", "vid_3", "Abhishekam", {"is_saved": True, "watch_completion_rate": 0.95}),
        ]

        for eid, vid, cat, eng in events_to_send:
            vm = {"video_id": vid, "category": cat, "ritual_family": cat}
            self.store.process_event(self.test_user, eid, "feedback", vid, eng, vm)

        persisted_prof = self.store.get_profile(self.test_user)
        persisted_vector = dict(persisted_prof["interests"])

        # 2. Rebuild profile from raw event log 10 times to verify 100% determinism
        for _ in range(10):
            reconstructed_prof = self.store.rebuild_profile_from_events(self.test_user)
            self.assertEqual(reconstructed_prof["interests"], persisted_vector)

if __name__ == "__main__":
    unittest.main()
