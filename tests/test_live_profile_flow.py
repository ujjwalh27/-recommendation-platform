import sys
sys.path.insert(0, ".")
import os
import json
import time
import unittest
from fastapi.testclient import TestClient
from backend.app import app, service

class TestLiveProfileFlow(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.test_user = "user_debug_flow"

    def setUp(self):
        # Reset profile for clean baseline
        self.client.post(f"/profile/{self.test_user}/reset")

    def test_live_feed_and_feedback_flow(self):
        """Tests live API end-to-end flow: LIKE -> GET /feed x4 -> Scroll navigation -> Idempotency."""
        # 1. Baseline profile inspect (Cold-start persona baseline)
        r0 = self.client.get(f"/profile/{self.test_user}/inspect")
        self.assertEqual(r0.status_code, 200)
        p0 = r0.json()
        v0 = p0["version"]
        self.assertIn("Aarti", p0["interests"])

        # 2. Like Video A
        video_id_a = "daiv_s2_42_aarti"
        event_id = f"evt_{self.test_user}_{video_id_a}_true_false"
        feedback_payload = {
            "user_id": self.test_user,
            "video_id": video_id_a,
            "event_id": event_id,
            "watch_completion_rate": 0.5,
            "is_liked": True,
            "is_saved": False,
            "video_meta": {"category": "Aarti", "ritual_family": "Aarti"}
        }
        r_like = self.client.post("/feedback", json=feedback_payload)
        self.assertEqual(r_like.status_code, 200)
        p_like = r_like.json()
        v1 = p_like["version"]
        self.assertEqual(v1, v0 + 1)
        self.assertIn("Aarti", p_like["interests"])
        like_interests = p_like["interests"]

        # 3. Request /feed 4 consecutive times (Simulate scrolling / fetching next pages)
        for i in range(4):
            rf = self.client.get(f"/feed?user_id={self.test_user}&limit=100")
            self.assertEqual(rf.status_code, 200)
            
            # Inspect profile after every single feed call
            rp = self.client.get(f"/profile/{self.test_user}/inspect")
            p_curr = rp.json()
            self.assertEqual(p_curr["version"], v1, f"Profile version mutated during feed call #{i+1}!")
            self.assertEqual(p_curr["interests"], like_interests, f"Profile vector changed during feed call #{i+1}!")

        # 4. Simulate Navigation A -> B -> C -> B -> A (Read-only calls)
        for nav_target in ["video_A", "video_B", "video_C", "video_B", "video_A"]:
            rf = self.client.get(f"/feed?user_id={self.test_user}&limit=100")
            self.assertEqual(rf.status_code, 200)
            rp = self.client.get(f"/profile/{self.test_user}/inspect")
            p_nav = rp.json()
            self.assertEqual(p_nav["version"], v1, f"Profile version mutated during navigation to {nav_target}!")
            self.assertEqual(p_nav["interests"], like_interests, f"Profile interests mutated during navigation to {nav_target}!")

        # 5. Send DUPLICATE LIKE with same event_id
        r_dup = self.client.post("/feedback", json=feedback_payload)
        self.assertEqual(r_dup.status_code, 200)
        p_dup = r_dup.json()
        # Version must NOT increase and interests must match
        self.assertEqual(p_dup["version"], v1)
        self.assertEqual(p_dup["interests"], like_interests)

        # 6. Final Inspection
        r_final = self.client.get(f"/profile/{self.test_user}/inspect")
        p_final = r_final.json()
        self.assertEqual(p_final["version"], v1)
        self.assertEqual(p_final["interests"], like_interests)

if __name__ == "__main__":
    unittest.main()
