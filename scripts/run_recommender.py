import sys
import os
import json

# Ensure the project root is in the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.recommender.service import RecommenderService
from src.users.personas import PERSONAS

def run_demo():
    print("=" * 70)
    print("Daiv Clips Recommendation Engine CLI Demo")
    print("=" * 70)
    
    # Initialize service
    print("Initializing Recommender Service...")
    service = RecommenderService()
    print("Service initialized successfully!")
    print()

    # Pick a few personas to demo
    demo_personas = ["Automobile Enthusiast", "Gamer", "Traveler"]
    
    for persona in demo_personas:
        print("-" * 70)
        print(f"PERSONA: {persona}")
        print("-" * 70)
        
        # Resolve to a mock user belonging to this persona
        user = service.find_user_by_id_or_persona(persona)
        user_id = user["user_id"]
        username = user["username"]
        
        # Get interest profile
        profile = service.interest_profiles.get(user_id)
        interests = profile.get("interests") if profile else {}
        non_zero_interests = {k: v for k, v in interests.items() if v > 0}
        
        print(f"Resolved User: {username} ({user_id})")
        print(f"Interest Profile: {non_zero_interests}")
        print()
        
        # Generate recommendations
        recommendations = service.get_recommendations(user_id, limit=5)
        
        print("TOP 5 RECOMMENDATIONS:")
        for rank, rec in enumerate(recommendations, start=1):
            print(f"\n{rank}. {rec['title'][:60]}...")
            print(f"   [Video ID]:   {rec['video_id']}")
            print(f"   [Category]:   {rec['category']}")
            print(f"   [Final Score]: {rec['score']:.4f}")
            print(f"   [Sources]:     {', '.join(rec['retrieval_sources'])}")
            print(f"   [Breakdown]:   Interest: {rec['score_breakdown']['interest']:.3f}, "
                  f"Similarity: {rec['score_breakdown']['similarity']:.3f}, "
                  f"Popularity: {rec['score_breakdown']['popularity']:.3f}, "
                  f"Exploration: {rec['score_breakdown']['exploration']:.3f}")
            print(f"   [Explanation]: \"{rec['explanation']}\"")
        print()
        
    print("=" * 70)
    print("CLI Recommendation Demo Completed")
    print("=" * 70)

if __name__ == "__main__":
    run_demo()
