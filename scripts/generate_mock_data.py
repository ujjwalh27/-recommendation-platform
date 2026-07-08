import sys
import os

# Ensure the project root is in the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.users.generator import MockDataGenerator

if __name__ == "__main__":
    print("=" * 60)
    print("Starting Mock User Data Generation")
    print("=" * 60)
    
    # Generate data for 60 users (10 users per persona)
    generator = MockDataGenerator(num_users=60)
    generator.generate()
    
    print()
    print("Mock Data Generation Pipeline Completed Successfully!")
    print("=" * 60)
