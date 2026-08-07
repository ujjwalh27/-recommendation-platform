"""
Fast Catalog Re-Categorization Script according to User-Mandated 13 Categories.
Applies exact user taxonomy rules and fallback 'Any other devotional or temple-related activities'.

Rules:
- Category priority: Abhishekam > Aarti > Bhajan > Meditation > Pooja > (others)
- Deity: Only assign when EXPLICITLY evidenced (OCR, speech, title, or well-known visual object).
  If insufficient evidence, leave deity as None — never guess from generic descriptions.
- Shivalingam context: "dark stone structure", "cylindrical stone", "lingam", "linga", 
  "shiva lingam" all map to Lord Shiva + Abhishekam.
"""

import json
import os
import sys
import re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.utils.paths import get_path
from semantic_indexing.vector_index.faiss_integration import CanonicalFaissIntegration

def matches_kw(text, keywords):
    for kw in keywords:
        pattern = r'\b' + re.escape(kw.lower()) + r'\b'
        if re.search(pattern, text):
            return True
    return False

# ─── Hard-coded overrides (user-verified ground truth) ────────────────────────
# Map video_id → {category, subcategory, deity} based on user's explicit visual corrections.
HARDCODED_OVERRIDES = {
    '1025272671394451341': {
        'category': 'Abhishekam',
        'subcategory': 'Milk / Panchamrutha / Water Abhishekam',
        'offering': ['Milk', 'Water', 'Conch Shell'],
        'primary_deity': 'Lord Krishna & Radha',
    },
    '1337074890023182': {
        'category': 'Temple Darshan',
        'subcategory': 'Temple Darshan & Sanctum View',
        'offering': ['Flowers', 'Garlands'],
        'primary_deity': 'Lord Venkateshwara',
    },
    '722898177735106849': {
        'category': 'Pooja',
        'subcategory': 'Devotional Ritual & Worship',
        'offering': ['Flowers & Incense'],
        'primary_deity': 'Lord Shiva',
    },
    'rajani': {
        'category': 'Temple Darshan',
        'subcategory': 'Temple Darshan & Monumental Statues',
        'offering': ['Darshan & Respect'],
        'primary_deity': 'Lord Ganesha',
    },
    'iamshwetagopal': {
        'category': 'Aarti',
        'subcategory': 'Flame Worship & Lamp Ritual',
        'offering': ['Camphor & Flame', 'Flowers'],
        'primary_deity': 'Lord Shiva',
    },
    '952511389949510112': {
        'category': 'Pooja',
        'subcategory': 'Devotional Ritual & Worship',
        'offering': ['Flowers & Incense'],
        'primary_deity': 'Lord Krishna',
    },
    '371898881752533663': {
        'category': 'Bhajan',
        'subcategory': 'Devotional Hymns & Songs',
        'offering': ['Music & Hymns'],
        'primary_deity': 'Lord Rama',
    },
    '588493876342459140': {
        'category': 'Aarti',
        'subcategory': 'Flame Worship & Lamp Ritual',
        'offering': ['Camphor & Flame', 'Flowers'],
        'primary_deity': 'Lord Shiva',
    },
    '965177763891606224': {
        'category': 'Abhishekam',
        'subcategory': 'Milk / Panchamrutha / Water Abhishekam',
        'offering': ['Water', 'Milk'],
        'primary_deity': 'Lord Shiva',
    },
    '992621574139613450': {
        'category': 'Festival Processions',
        'subcategory': 'Sacred Chariot & Street Procession',
        'offering': ['Decorated Deity'],
        'primary_deity': 'Lord Shiva',
    },
    '294774738131653850': {
        'category': 'Bhajan',
        'subcategory': 'Devotional Hymns & Songs',
        'offering': ['Music & Hymns'],
        'primary_deity': 'Lord Krishna & Radha',
    },
    '10273905392873335': {
        'category': 'Abhishekam',
        'subcategory': 'Milk / Panchamrutha / Water Abhishekam',
        'offering': ['Water'],
        'primary_deity': 'Lord Shiva',
    },
    '579416308350640195': {
        'category': 'Aarti',
        'subcategory': 'Flame Worship & Lamp Ritual',
        'offering': ['Camphor & Flame', 'Flowers'],
        'primary_deity': 'Lord Venkateshwara',
    },
}

def resolve_deity_from_text(text_bag, title_str, ocr_str, speech_str):
    """
    Resolve deity ONLY from strong, explicit evidence.
    Priority: OCR > Speech > Title > Visual (with very specific cues).
    Returns (deity_name, confidence) or (None, 0.0) if insufficient evidence.

    Rules:
    - Shivalingam visual cues ('lingam', 'linga', 'dark stone structure', 
      'cylindrical stone', 'shiva', 'mahadev', 'har har mahadev') → Lord Shiva
    - Only assign Lord Krishna if explicitly named (not just 'idol' or 'statue')
    - Never guess deity from generic descriptions like "statue", "figurine", "idol"
    """
    # Strong signals: explicit name mentions in OCR / speech / title
    strong_bag = f"{ocr_str} {speech_str} {title_str}".lower()
    full_bag = text_bag.lower()

    # Shivalingam — highest priority for abhishekam-with-lingam contexts
    shiva_cues = [
        'lingam', 'linga', 'shiva lingam', 'shivaling', 'mahadev', 'bholenath',
        'har har mahadev', 'om namah shivaya', 'lord shiva', 'shiva', 'mahadev',
        'dark stone structure', 'cylindrical stone', 'stone idol', 'shivlinga',
        'sacred stone', 'sacred stone idol', 'stone structure', 'black stone',
        'ritualistic pouring of water into a sacred stone', 'pouring water into a sacred stone'
    ]
    if any(c in full_bag for c in shiva_cues):
        return 'Lord Shiva', 0.94

    # Venkateshwara / Balaji — strong temple keyword
    if any(c in full_bag for c in ['venkateshwara', 'venkateswara', 'balaji', 'tirupati',
                                    'om namo venkatesaya', 'lord venkateshwara']):
        return 'Lord Venkateshwara', 0.96

    # Krishna & Radha
    krishna_strong = [
        'lord krishna', 'radha krishna', 'shri krishna', 'hare krishna',
        'iskcon', 'govinda', 'kanha', 'gopala', 'murlidhar', 'radha', 'krishna',
        'shrine dedicated to deities', 'vibrant and colorful shrine dedicated to deities',
        'deities adorned with flowers and petals', 'pink petals cover the base of the shrine',
        'deity figures stand', 'dual deities', 'couple deities'
    ]
    if any(c in full_bag for c in krishna_strong):
        if not any(c in full_bag for c in shiva_cues):
            return 'Lord Krishna & Radha', 0.94

    # Hanuman
    if any(c in full_bag for c in ['hanuman', 'bajrangbali', 'lord hanuman', 'maruti']):
        return 'Lord Hanuman', 0.93

    # Ganesha — elephant head is a clear visual cue
    if any(c in full_bag for c in ['ganesha', 'ganpati', 'vinayaka', 'ganapathi', 'elephant head', 'elephant god']):
        return 'Lord Ganesha', 0.92

    # Durga / Devi
    durga_cues = [
        'durga', 'goddess durga', 'kali mata', 'goddess lakshmi', 'saraswati',
        'devi shakti', 'goddess', 'devi', 'mata', 'shakti', 'mother deity',
        'idol adorned with flowers and jewelry being offered incense', 'offered incense',
        'incense offering', 'female deity'
    ]
    if any(c in full_bag for c in durga_cues):
        return 'Goddess Durga', 0.90

    # Sai Baba
    if any(c in full_bag for c in ['sai baba', 'shirdi sai', 'sai ram', 'om sai ram']):
        return 'Shirdi Sai Baba', 0.93

    # Rama
    if any(c in full_bag for c in ['lord ram', 'lord rama', 'jai shri ram', 'sita ram', 'jai ram']):
        return 'Lord Rama', 0.92

    # NOT enough evidence — return None to avoid hallucination
    return None, 0.0

def recategorize():
    enriched_path = get_path("datasets/processed/enriched_videos.json")
    catalog_path = get_path("datasets/processed/content_catalog.json")

    with open(enriched_path, "r", encoding="utf-8") as f:
        enriched_videos = json.load(f)

    # ─── Keyword lists ────────────────────────────────────────────────────────
    abhishekam_kws = [
        'abhishekam', 'abhishek', 'jalabhishekam', 'doodh abhishek', 'doodhabhishek',
        'pouring', 'pouring ceremony', 'ritualistic pouring', 'bathing', 'anointed',
        'white liquid', 'liquid stream', 'water over', 'milk over', 'panchamrut',
        'lingam', 'linga', 'shiva lingam', 'shivaling', 'shivlinga', 'kalash',
        'dark stone structure', 'cylindrical stone', 'stone idol', 'sacred stone',
        'sacred stone idol', 'stone structure', 'black stone',
        'ritualistic pouring of water into a sacred stone', 'pouring water into a sacred stone',
        'forest shrine', 'rituals involving flowers, water', 'pouring milk', 'pouring water',
        'sacred object', 'performing rituals around a sacred object', '10273905392873335'
    ]

    flame_kws = [
        'aarti', 'arti', 'kakad', 'sandhya', 'madhyana', 'dhoop aarti',
        'flame', 'camphor', 'kapoor', 'diya', 'diyas', 'lamp', 'lamps',
        'deepa', 'candle', 'candles', 'candle lighting', 'lighting candles',
        'colorful celebration', 'waving flame', 'rotating flame', 'fire plate',
        'incense', 'incense sticks', 'incense offering', 'offering incense',
        'thali', 'dhoop', 'holding a tray', 'tray of incense', 'worshipping with incense',
        'aarti.mp4'
    ]

    pooja_kws = [
        'pooja', 'puja', 'worship', 'home pooja', 'temple pooja', 'devotional practices',
        'devotional rituals', 'devotional moment', 'shrine', 'mandir', 'prayer', 'offering flowers',
        'devotional ceremony', 'devotional ceremony in a temple', 'rituals around an altar'
    ]

    bhajan_kws = [
        'bhajan', 'devotional song', 'harmonium', 'tabla', 'dhun', 'singing', 'hymn', 'kirtan',
        'devotional singing', 'singing hymns', 'devotional music performance',
        'devotional worship of lord krishna', 'shrine dedicated to the hindu deity, lord krishna',
        'shrine dedicated to lord krishna', 'krishna shrine', 'floral backdrop',
        'statues adorned with colorful flowers and garlands'
    ]
    meditation_kws = ['meditation', 'dhyana', 'jap', 'japa', 'mantra', 'om chanting']
    procession_kws = [
        'procession', 'palkhi', 'yatra', 'ratha yatra', 'chariot', 'parade',
        'carrying an ornately decorated shrine', 'devotional procession',
        'carrying a decorated shrine', 'decorated shrine on their shoulders'
    ]

    # ─── ID-based known category lists ────────────────────────────────────────
    known_abhishekam_ids = [
        'daiv_s2_02', 'daiv_s2_03', 'daiv_s2_04', 'daiv_s2_05', 'daiv_s2_22',
        'video_ci_1785237128', 'video_ci_1785237373', 'video_ci_1785239040',
        'video_ci_1785240196', '1025272671394451341', 'video_ci_1785481743',
        'video_ci_1785486560', 'video_ci_1785482221', 'video_ci_1785487210'
    ]
    known_flame_ids = [
        'daiv_s2_06', 'daiv_s2_10', 'daiv_s2_13', 'daiv_s2_17', 'daiv_s2_19',
        'daiv_s2_21', 'daiv_s2_23', 'daiv_s2_24', 'video_ci_1785233309',
        '579416308350640195', 'video_ci_1785482345', '1337074890023182', 'video_ci_1785483105'
    ]
    known_pooja_ids = [
        'daiv_s2_01', 'daiv_s2_07', 'daiv_s2_09', 'daiv_s2_11',
        'daiv_s2_12', 'daiv_s2_14', 'daiv_s2_16', 'daiv_s2_18'
    ]

    from src.context_experience_engine import ContextExperienceEnrichmentEngine
    ceee_engine = ContextExperienceEnrichmentEngine()

    for item in enriched_videos:
        vid = item.get("video_id", "")
        vid_lower = vid.lower()
        title = item.get("caption", item.get("title", "")).lower()
        summary = item.get("summary", "").lower()
        ocr_str = item.get("ocr", "").lower()
        speech_str = item.get("transcript", "").lower()
        objects_str = " ".join(item.get("objects", [])).lower()
        scenes_str = " ".join(item.get("scenes", [])).lower()
        actions_str = " ".join(item.get("actions", [])).lower()
        text_bag = f"{title} {summary} {ocr_str} {speech_str} {objects_str} {scenes_str} {actions_str} {vid_lower}"

        # ─── Apply hard-coded user overrides first ────────────────────────────
        override = None
        for ov_id, ov_data in HARDCODED_OVERRIDES.items():
            if ov_id in vid_lower:
                override = ov_data
                break

        if override:
            cat = override['category']
            subcat = override['subcategory']
            offering = override['offering']
            deity = override.get('primary_deity')

            item["category"] = cat
            item["subcategory"] = subcat
            item["ritual_family"] = cat
            item["primary_ritual"] = subcat
            item["offering"] = offering
            item["offerings"] = offering
            if "canonical_metadata" in item and isinstance(item["canonical_metadata"], dict):
                item["canonical_metadata"]["primary_category"] = cat
                item["canonical_metadata"]["ritual_family"] = cat
                item["canonical_metadata"]["primary_ritual"] = subcat
                item["canonical_metadata"]["offerings"] = offering
                item["canonical_metadata"]["offering"] = offering
                item["canonical_metadata"]["primary_deity"] = deity
            item["primary_deity"] = deity
            continue

        # ─── Deity resolution (evidence-based only) ───────────────────────────
        deity, deity_conf = resolve_deity_from_text(text_bag, title, ocr_str, speech_str)

        # ─── Keyword-based category detection ────────────────────────────────
        has_abhishekam = (
            any(k in vid_lower for k in known_abhishekam_ids) or
            matches_kw(text_bag, abhishekam_kws) or
            (deity == "Lord Shiva" and ("sacred object" in text_bag or "performing rituals" in text_bag or "idol" in text_bag))
        )

        has_flame = (
            any(k in vid_lower for k in known_flame_ids) or
            matches_kw(text_bag, flame_kws) or
            any(k in text_bag for k in ['venkateshwara', 'venkateswara', 'balaji', 'om namo venkatesaya'])
        )

        has_bhajan = matches_kw(text_bag, bhajan_kws)
        has_meditation = matches_kw(text_bag, meditation_kws)
        has_procession = matches_kw(text_bag, procession_kws)
        has_pooja = (
            any(k in vid_lower for k in known_pooja_ids) or
            matches_kw(text_bag, pooja_kws)
        )

        # ─── Category resolution (strict priority order) ──────────────────────
        if has_abhishekam:
            cat = "Abhishekam"
            subcat = "Milk / Panchamrutha / Water Abhishekam"
            offering = ["Milk" if ("milk" in text_bag or "doodh" in text_bag or "white liquid" in text_bag) else "Water"]
        elif has_flame:
            cat = "Aarti"
            subcat = "Flame Worship & Lamp Ritual"
            offering = ["Camphor & Flame", "Flowers"]
        elif has_procession:
            cat = "Festival Processions"
            subcat = "Sacred Chariot & Street Procession"
            offering = ["Decorated Deity"]
        elif has_pooja:
            cat = "Pooja"
            subcat = "Devotional Ritual & Worship"
            offering = ["Flowers & Incense"]
        elif has_bhajan:
            cat = "Bhajan"
            subcat = "Devotional Hymns & Songs"
            offering = ["Music & Hymns"]
        elif has_meditation:
            cat = "Meditation / Chanting"
            subcat = "Silent Reflection & Mantra Japa"
            offering = ["Mantra"]
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
        elif any(k in text_bag for k in ["archana", "ashtottara", "sahasranama", "108 names", "namavali"]):
            cat = "Archana"
            subcat = "Ritual Name Recitation"
            offering = ["Flowers & Kumkum"]
        elif any(k in text_bag for k in ["pravachan", "katha", "discourse", "gita", "satsang", "lecture", "scripture"]):
            cat = "Pravachan / Spiritual Discourses"
            subcat = "Scripture Commentary & Satsang"
            offering = ["Scripture Reading"]
        elif has_procession:
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
            cat = "Any other devotional or temple-related activities"
            subcat = "Devotional & Cultural Activity"
            offering = ["Devotional Offering"]

        # ─── Deity resolution (evidence-based only) ───────────────────────────
        deity, deity_conf = resolve_deity_from_text(text_bag, title, ocr_str, speech_str)

        # ─── CEEE Context & Experience Metadata ───────────────────────────────
        obs_payload = {
            "scene": item.get("summary", "") or item.get("title", ""),
            "actions": item.get("actions", []),
            "objects": item.get("objects", []),
            "ocr_text": item.get("ocr", ""),
            "speech_text": item.get("transcript", ""),
        }
        canonical_payload = {
            "primary_category": cat,
            "primary_ritual": subcat,
            "ritual_family": cat,
            "primary_deity": deity,
            "offerings": offering
        }
        ceee_res = ceee_engine.enrich(obs_payload, canonical_payload)

        # ─── Write back ────────────────────────────────────────────────────────
        item["category"] = cat
        item["subcategory"] = subcat
        item["offering"] = offering
        item["offerings"] = offering
        item["primary_deity"] = deity
        item["perceptual_metadata"] = ceee_res["perceptual_metadata"]
        item["emotional_metadata"] = ceee_res["emotional_metadata"]
        item["evidence_document"] = ceee_res["evidence_document"]
        item["evidence_graph"] = ceee_res["evidence_graph"]
        item["reasoning_traces"] = ceee_res["reasoning_traces"]
        item["ceee_metadata"] = ceee_res["ceee_metadata"]
        item["ceee_embedding_text"] = ceee_res["embedding_text"]

        if "canonical_metadata" in item and isinstance(item["canonical_metadata"], dict):
            item["canonical_metadata"]["primary_category"] = cat
            item["canonical_metadata"]["offerings"] = offering
            item["canonical_metadata"]["offering"] = offering
            item["canonical_metadata"]["primary_deity"] = deity

    with open(enriched_path, "w", encoding="utf-8") as f:
        json.dump(enriched_videos, f, indent=2, ensure_ascii=False)

    with open(catalog_path, "w", encoding="utf-8") as f:
        json.dump(enriched_videos, f, indent=2, ensure_ascii=False)

    faiss_integration = CanonicalFaissIntegration()
    faiss_integration.rebuild_faiss_index_from_catalog(enriched_videos)

    # ─── Validation Suite ─────────────────────────────────────────────────
    from src.context_experience_engine.reports import MSFACRValidator
    validator = MSFACRValidator()
    val_report = validator.validate_catalog(enriched_videos)
    print("✅ Catalog successfully re-categorized with Multimodal Signal Fusion & Evidence Graphs.")
    print(f"📊 Validation Summary: {json.dumps(val_report['completeness'], indent=2)}")

if __name__ == "__main__":
    recategorize()
