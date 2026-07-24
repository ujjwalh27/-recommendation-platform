import os
import sys
import json
import shutil

# Add project root to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def clear_cache_and_history():
    print("=========================================================================")
    print("           CLEARING CONTENT INTELLIGENCE CACHE & SEEDING HISTORY          ")
    print("=========================================================================")

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    # 1. Reset content intelligence JSON database
    db_file = os.path.join(base_dir, "datasets", "processed", "content_intelligence_db.json")
    with open(db_file, "w", encoding="utf-8") as f:
        json.dump([], f)
    print(f"✓ Reset Content Intelligence DB: {db_file}")

    # 2. Reset feedback repository
    feedback_file = os.path.join(base_dir, "datasets", "processed", "feedback_repository.json")
    with open(feedback_file, "w", encoding="utf-8") as f:
        json.dump([], f)
    print(f"✓ Reset Feedback Repository: {feedback_file}")

    # 3. Clear debug_outputs directory
    debug_dir = os.path.join(base_dir, "debug_outputs")
    if os.path.exists(debug_dir):
        for item in os.listdir(debug_dir):
            item_path = os.path.join(debug_dir, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            elif os.path.isfile(item_path):
                os.remove(item_path)
        print(f"✓ Cleared Debug Outputs: {debug_dir}")

    # 4. Clear knowledge graphs directory
    kg_dir = os.path.join(base_dir, "datasets", "processed", "knowledge_graphs")
    if os.path.exists(kg_dir):
        for item in os.listdir(kg_dir):
            item_path = os.path.join(kg_dir, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
        print(f"✓ Cleared Knowledge Graphs: {kg_dir}")

    print("=========================================================================")
    print("ALL CACHE & CATALOG SEEDING HISTORY CLEARED! READY FOR MANUAL VALIDATION.")
    print("=========================================================================")

if __name__ == "__main__":
    clear_cache_and_history()
