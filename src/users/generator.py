import json
import random
from typing import List, Dict, Any
import numpy as np
import pandas as pd
from src.utils.paths import get_path
from src.users.personas import PERSONAS, get_persona_preferred_categories

# Engagement weights for interest profile builder
ENGAGEMENT_WEIGHTS = {
    "completed": 10,
    "replay": 8,
    "like": 7,
    "save": 9,
    "share": 10,
    "comment": 8,
    "skip": -8
}

MOCK_USERNAMES = [
    "alex_dreamer", "car_guy_99", "pixel_coder", "foodie_chef", "dog_whisperer",
    "wanderlust_soul", "gaming_ninja", "auto_speed", "tech_reviewer", "baker_delight",
    "paw_friend", "globe_trotter", "keyboard_warrior", "gear_head", "code_coffee",
    "gourmet_gal", "cat_lady_meow", "nomad_journey", "retro_gamer", "speed_demon",
    "silicon_valley", "sweet_tooth", "wildlife_click", "passport_stamps", "console_boss",
    "piston_cup", "hacker_spirit", "tasty_bites", "furry_tails", "summit_chaser"
]


class MockDataGenerator:
    """Generates mock users, watch histories, and interest profiles based on personas."""

    def __init__(self, num_users: int = 60):
        self.num_users = num_users
        self.videos_path = get_path("datasets/processed/enriched_videos.json")
        self.users_path = get_path("datasets/processed/users.json")
        self.watch_history_path = get_path("datasets/processed/watch_history.json")
        self.interest_profiles_path = get_path("datasets/processed/interest_profiles.json")
        
        # Load videos
        with open(self.videos_path, "r", encoding="utf-8") as f:
            self.videos = json.load(f)

        # Index videos by category for quick sampling
        self.videos_by_category: Dict[str, List[Dict[str, Any]]] = {}
        for video in self.videos:
            cat = video.get("category", "Entertainment")
            self.videos_by_category.setdefault(cat, []).append(video)

        self.categories = list(self.videos_by_category.keys())

    def generate(self) -> None:
        """Runs the generation pipeline."""
        print(f"Generating mock data for {self.num_users} users...")
        random.seed(42)  # For reproducibility

        users = []
        watch_history = []
        interest_profiles = {}

        persona_names = list(PERSONAS.keys())

        for i in range(self.num_users):
            user_id = f"user_{i + 1}"
            
            # Select username
            if i < len(MOCK_USERNAMES):
                username = MOCK_USERNAMES[i]
            else:
                username = f"user_persona_{i + 1}"

            # Assign a persona in a round-robin / balanced way
            persona = persona_names[i % len(persona_names)]
            preferred_cats = get_persona_preferred_categories(persona)

            # 1. Store User Info
            users.append({
                "user_id": user_id,
                "username": username,
                "persona": persona,
                "preferred_categories": preferred_cats
            })

            # 2. Simulate Watch History
            # Generate between 20 and 50 watch events per user
            num_events = random.randint(25, 50)
            user_events = []
            
            for _ in range(num_events):
                # 80% preferred category, 20% random exploration
                if random.random() < 0.8 and preferred_cats:
                    category = random.choice(preferred_cats)
                else:
                    category = random.choice(self.categories)

                # Fetch videos in this category
                cat_videos = self.videos_by_category.get(category, self.videos)
                if not cat_videos:
                    cat_videos = self.videos
                video = random.choice(cat_videos)

                # Simulate engagement signals
                is_preferred = category in preferred_cats
                
                # Preferred content gets higher completion rate
                if is_preferred:
                    watch_completion_rate = min(1.0, max(0.1, random.normalvariate(0.85, 0.15)))
                else:
                    watch_completion_rate = min(1.0, max(0.0, random.normalvariate(0.40, 0.30)))

                watch_completion_rate = round(watch_completion_rate, 2)
                watch_time_seconds = round(video["duration"] * watch_completion_rate, 2)

                # Replay simulation
                replay_count = 0
                if watch_completion_rate > 0.9:
                    replay_prob = 0.20 if is_preferred else 0.05
                    if random.random() < replay_prob:
                        replay_count = random.choice([1, 2])

                # Social interaction simulation
                is_liked = False
                is_saved = False
                is_shared = False
                commented = False

                if watch_completion_rate > 0.8:
                    is_liked = random.random() < (0.40 if is_preferred else 0.15)
                if watch_completion_rate > 0.9:
                    is_saved = random.random() < (0.25 if is_preferred else 0.05)
                if watch_completion_rate > 0.95:
                    is_shared = random.random() < (0.15 if is_preferred else 0.02)
                if is_liked:
                    commented = random.random() < 0.08

                # Engagement score calculation
                event_score = 0
                if watch_completion_rate >= 0.9:
                    event_score += ENGAGEMENT_WEIGHTS["completed"]
                elif watch_completion_rate < 0.2:
                    event_score += ENGAGEMENT_WEIGHTS["skip"]

                event_score += replay_count * ENGAGEMENT_WEIGHTS["replay"]
                if is_liked:
                    event_score += ENGAGEMENT_WEIGHTS["like"]
                if is_saved:
                    event_score += ENGAGEMENT_WEIGHTS["save"]
                if is_shared:
                    event_score += ENGAGEMENT_WEIGHTS["share"]
                if commented:
                    event_score += ENGAGEMENT_WEIGHTS["comment"]

                event = {
                    "user_id": user_id,
                    "video_id": video["video_id"],
                    "category": category,
                    "watch_completion_rate": watch_completion_rate,
                    "watch_time_seconds": watch_time_seconds,
                    "replay_count": replay_count,
                    "is_liked": is_liked,
                    "is_saved": is_saved,
                    "is_shared": is_shared,
                    "is_commented": commented,
                    "engagement_score": event_score
                }
                user_events.append(event)
                watch_history.append(event)

            # 3. Build Interest Profile
            # Aggregate engagement score per category
            df_events = pd.DataFrame(user_events)
            cat_scores = df_events.groupby("category")["engagement_score"].sum().to_dict()

            # Clean and keep non-negative scores
            cleaned_scores = {}
            for cat in self.categories:
                score = cat_scores.get(cat, 0.0)
                cleaned_scores[cat] = max(0.0, float(score))

            # Normalize to sum up to 100
            total_score = sum(cleaned_scores.values())
            normalized_profile = {}
            if total_score > 0:
                for cat, score in cleaned_scores.items():
                    normalized_profile[cat] = round((score / total_score) * 100, 2)
            else:
                # Fallback to uniform distribution if zero interaction score
                for cat in self.categories:
                    normalized_profile[cat] = round(100 / len(self.categories), 2)

            interest_profiles[user_id] = {
                "user_id": user_id,
                "persona": persona,
                "raw_scores": cleaned_scores,
                "interests": normalized_profile
            }

        # Save files
        with open(self.users_path, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4)
        print(f"Saved users to {self.users_path}")

        with open(self.watch_history_path, "w", encoding="utf-8") as f:
            json.dump(watch_history, f, indent=4)
        print(f"Saved watch history to {self.watch_history_path}")

        with open(self.interest_profiles_path, "w", encoding="utf-8") as f:
            json.dump(interest_profiles, f, indent=4)
        print(f"Saved interest profiles to {self.interest_profiles_path}")

        # Prints sample stats
        print("\nInterest Profile Sample (User 1 - Persona: {}):".format(users[0]["persona"]))
        print(json.dumps(interest_profiles["user_1"]["interests"], indent=2))
