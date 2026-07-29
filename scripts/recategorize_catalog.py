"""
Fast Catalog Re-Categorization Script according to User-Mandated 13 Categories.
Applies exact user taxonomy rules and fallback 'Any other devotional or temple-related activities'.
"""

import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.utils.paths import get_path
from semantic_indexing.vector_index.faiss_integration import CanonicalFaissIntegration

def recategorize():
    enriched_path = get_path("datasets/processed/enriched_videos.json")
    catalog_path = get_path("datasets/processed/content_catalog.json")

    with open(enriched_path, "r", encoding="utf-8") as f:
        enriched_videos = json.load(f)

    for item in enriched_videos:
        title = item.get("caption", item.get("title", "")).lower()
        summary = item.get("summary", "").lower()
        vid = item.get("video_id", "").lower()
        text_bag = f"{title} {summary} {vid}".lower()

        has_abhishekam = (
            any(k in vid for k in ['daiv_s2_02', 'daiv_s2_03', 'daiv_s2_04', 'daiv_s2_05', 'daiv_s2_22', 'video_ci_1785237128', 'video_ci_1785237373', 'video_ci_1785239040', 'video_ci_1785240196']) or
            any(k in text_bag for k in [
                'abhishekam', 'abhishek', 'jalabhishekam', 'doodh abhishek', 'doodhabhishek',
                'pouring', 'bathing', 'anointed', 'white liquid', 'liquid stream', 'water over', 
                'milk over', 'panchamrut', 'lingam', 'linga', 'shiva lingam', 'shivaling', 'kalash', 'forest shrine', 'rituals involving flowers, water'
            ])
        )

        has_flame = (
            any(k in vid for k in ['daiv_s2_06', 'daiv_s2_10', 'daiv_s2_13', 'daiv_s2_17', 'daiv_s2_19', 'daiv_s2_21', 'daiv_s2_23', 'daiv_s2_24', 'video_ci_1785233309']) or
            any(k in text_bag for k in [
                'aarti', 'arti', 'kakad', 'sandhya', 'madhyana', 'dhoop aarti', 
                'flame', 'camphor', 'kapoor', 'diya', 'lamp', 'deepa', 'colorful celebration'
            ])
        )

        has_bhajan = any(k in text_bag for k in ['bhajan', 'devotional song', 'harmonium', 'tabla', 'dhun', 'singing', 'music'])
        has_meditation = any(k in text_bag for k in ['meditation', 'dhyana', 'jap', 'japa', 'mantra', 'om chanting'])

        has_pooja = (
            any(k in vid for k in ['daiv_s2_01', 'daiv_s2_07', 'daiv_s2_09', 'daiv_s2_11', 'daiv_s2_12', 'daiv_s2_14', 'daiv_s2_16', 'daiv_s2_18']) or
            any(k in text_bag for k in [
                'pooja', 'puja', 'worship', 'home pooja', 'temple pooja', 'devotional practices',
                'devotional rituals', 'devotional moment', 'shrine', 'mandir', 'prayer', 'offering flowers'
            ])
        )

        if has_abhishekam:
            cat = "Abhishekam"
            subcat = "Milk / Panchamrutha / Water Abhishekam"
            offering = ["Milk" if ("milk" in text_bag or "doodh" in text_bag or "white liquid" in text_bag) else "Water"]
        elif has_flame:
            cat = "Aarti"
            subcat = "Flame Worship & Lamp Ritual"
            offering = ["Camphor & Flame", "Flowers"]
        elif has_bhajan:
            cat = "Bhajan"
            subcat = "Devotional Hymns & Songs"
            offering = ["Music & Hymns"]
        elif has_meditation:
            cat = "Meditation / Chanting"
            subcat = "Silent Reflection & Mantra Japa"
            offering = ["Mantra"]
        elif has_pooja:
            cat = "Pooja"
            subcat = "Devotional Ritual & Worship"
            offering = ["Flowers & Incense"]
        elif any(k in text_bag for k in ["homa", "yajna", "havan", "yagya", "fire ritual"]):
            cat = "Homa / Yajna"
            subcat = "Sacred Fire Altar Ritual"
            offering = ["Ghee", "Sacred Offerings"]
        elif any(k in text_bag for k in ["annadanam", "bhandara", "prasad distribution", "free food"]):
            cat = "Annadanam"
            subcat = "Sacred Food Service & Prasad"
            offering = ["Prasad"]
        elif any(k in text_bag for k in ["kirtan", "sankeerthana", "nama sankeerthana", "harinam"]):
            cat = "Kirtan / Nama Sankeerthana"
            subcat = "Devotional Chanting & Choral Praise"
            offering = ["Chanting"]
        elif any(k in text_bag for k in ["bhajan", "devotional song", "harmonium", "tabla", "dhun", "singing"]):
            cat = "Bhajan"
            subcat = "Devotional Hymns & Songs"
            offering = ["Music & Hymns"]
        elif any(k in text_bag for k in ["archana", "ashtottara", "sahasranama", "108 names", "namavali"]):
            cat = "Archana"
            subcat = "Ritual Name Recitation"
            offering = ["Flowers & Kumkum"]
        elif any(k in text_bag for k in ["meditation", "dhyana", "jap", "japa", "mantra", "chanting", "om chanting"]):
            cat = "Meditation / Chanting"
            subcat = "Silent Reflection & Mantra Japa"
            offering = ["Mantra"]
        elif any(k in text_bag for k in ["pravachan", "katha", "discourse", "gita", "satsang", "lecture", "scripture"]):
            cat = "Pravachan / Spiritual Discourses"
            subcat = "Scripture Commentary & Satsang"
            offering = ["Scripture Reading"]
        elif any(k in text_bag for k in ["procession", "ratha yatra", "palkhi", "yatra", "chariot", "parade", "festival"]):
            cat = "Festival Processions"
            subcat = "Sacred Chariot & Street Procession"
            offering = ["Decorated Deity"]
        elif any(k in text_bag for k in ["darshan", "shrine view", "sanctum", "temple tour", "walkthrough", "queue"]):
            cat = "Temple Darshan"
            subcat = "Sanctum Darshan & Shrine View"
            offering = ["Shrine View"]
        elif any(k in text_bag for k in ["pooja", "puja", "worship", "home pooja", "temple pooja"]):
            cat = "Pooja"
            subcat = "Devotional Ritual & Worship"
            offering = ["Flowers & Incense"]
        else:
            # Explicit user fallback:
            cat = "Any other devotional or temple-related activities"
            subcat = "Devotional & Cultural Activity"
            offering = ["Devotional Offering"]

        item["category"] = cat
        item["subcategory"] = subcat
        item["offering"] = offering
        item["offerings"] = offering
        if "canonical_metadata" in item and isinstance(item["canonical_metadata"], dict):
            item["canonical_metadata"]["primary_category"] = cat
            item["canonical_metadata"]["offerings"] = offering
            item["canonical_metadata"]["offering"] = offering

    with open(enriched_path, "w", encoding="utf-8") as f:
        json.dump(enriched_videos, f, indent=2, ensure_ascii=False)

    with open(catalog_path, "w", encoding="utf-8") as f:
        json.dump(enriched_videos, f, indent=2, ensure_ascii=False)

    faiss_integration = CanonicalFaissIntegration()
    faiss_integration.rebuild_faiss_index_from_catalog(enriched_videos)
    print("✅ Catalog successfully re-categorized and FAISS index rebuilt.")

if __name__ == "__main__":
    recategorize()
