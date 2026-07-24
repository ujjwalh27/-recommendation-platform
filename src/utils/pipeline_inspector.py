import os
import json
import shutil
from typing import Dict, Any, List

DEBUG_MODE = True

class PipelineInspector:
    """Automated Pipeline Inspector that dumps raw intermediate artifacts to debug_outputs/ 01-19 folders."""

    STAGE_DIRS = {
        1: "01_input_video",
        2: "02_sampled_frames",
        3: "03_whisper",
        4: "04_ocr",
        5: "05_yolo",
        6: "06_clip",
        7: "07_videomae",
        8: "08_audio_events",
        9: "09_vlm",
        10: "10_reasoning",
        11: "11_knowledge_graph",
        12: "12_metadata",
        13: "13_embeddings",
        14: "14_claims",
        15: "15_hypotheses",
        16: "16_conflict_resolution",
        17: "17_episode_reasoning",
        18: "18_semantic_memory",
        19: "19_final_report"
    }

    def __init__(self, base_dir: str = "debug_outputs"):
        self.base_dir = base_dir
        self.init_directories()

    def init_directories(self):
        os.makedirs(self.base_dir, exist_ok=True)
        for num, name in self.STAGE_DIRS.items():
            dir_path = os.path.join(self.base_dir, f"{num:02d}_{name.split('_', 1)[1]}")
            os.makedirs(dir_path, exist_ok=True)

    def dump_stage(self, stage_num: int, filename: str, data: Any):
        if not DEBUG_MODE:
            return
        
        folder_name = f"{stage_num:02d}_{self.STAGE_DIRS[stage_num].split('_', 1)[1]}"
        target_dir = os.path.join(self.base_dir, folder_name)
        os.makedirs(target_dir, exist_ok=True)
        
        target_path = os.path.join(target_dir, filename)

        try:
            if isinstance(data, (dict, list)):
                with open(target_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            elif isinstance(data, str):
                with open(target_path, "w", encoding="utf-8") as f:
                    f.write(data)
            elif hasattr(data, "dict"):
                with open(target_path, "w", encoding="utf-8") as f:
                    json.dump(data.dict(), f, indent=2, ensure_ascii=False, default=str)
            print(f"[DEBUG-INSPECTOR] Stage {stage_num:02d} ({folder_name}) artifact dumped -> {target_path}")
        except Exception as e:
            print(f"[DEBUG-INSPECTOR] Error dumping stage {stage_num}: {e}")

    def copy_frame_images(self, frame_paths: List[str]):
        if not DEBUG_MODE:
            return
        target_dir = os.path.join(self.base_dir, "02_sampled_frames")
        os.makedirs(target_dir, exist_ok=True)
        for idx, src in enumerate(frame_paths):
            if os.path.exists(src):
                dst = os.path.join(target_dir, f"keyframe_{idx:03d}_{os.path.basename(src)}")
                shutil.copy(src, dst)
