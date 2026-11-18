#!/usr/bin/env python3
"""
OpenShorts Engine Rule Injector & Config Patcher
Translates config/clipping_rules.json directly into engine/.env and core parameters:
- 15s to 45s min/max duration
- Single-line bouncy subtitles (3 words per batch)
- 16:9 (X/Twitter & FB Page) + 9:16 (Shorts/Reels) dual export presets
- Target 3 clips per job
"""

import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RULES_PATH = os.path.join(BASE_DIR, "config", "clipping_rules.json")
ENGINE_DIR = os.path.join(BASE_DIR, "engine")
ENGINE_ENV = os.path.join(ENGINE_DIR, ".env")
ROOT_ENV = os.path.join(BASE_DIR, ".env")

def load_rules():
    if not os.path.exists(RULES_PATH):
        print(f"❌ Rules not found at {RULES_PATH}")
        sys.exit(1)
    with open(RULES_PATH, "r") as f:
        return json.load(f)

def patch():
    rules = load_rules()
    print("🔧 Injecting Custom Rules from config/clipping_rules.json into Engine...")

    min_dur = rules["duration_rules"]["min_seconds"]
    max_dur = rules["duration_rules"]["max_seconds"]
    max_lines = rules["subtitles"]["max_lines"]
    words_batch = rules["subtitles"]["words_per_batch"]
    clips_per_day = rules["publishing_schedule"]["clips_per_day"]

    injections = [
        f"\n# === Auto-Injected from config/clipping_rules.json ===",
        f"MIN_CLIP_DURATION={min_dur}",
        f"MAX_CLIP_DURATION={max_dur}",
        f"CLIP_TARGET_MIN={clips_per_day}",
        f"CLIP_TARGET_MAX={clips_per_day + 2}",
        f"SUBTITLE_MAX_LINES={max_lines}",
        f"SUBTITLE_WORDS_PER_BATCH={words_batch}",
        f"SUBTITLE_ANIMATION={rules['subtitles']['animation']}",
        f"DUAL_ASPECT_RATIOS=16:9,9:16",
        f"PRIMARY_COLOR={rules['subtitles']['primary_color']}",
        f"HIGHLIGHT_COLOR={rules['subtitles']['highlight_color']}",
        f"# =====================================================\n"
    ]

    target_envs = [ROOT_ENV]
    if os.path.exists(ENGINE_DIR):
        target_envs.append(ENGINE_ENV)

    for env_file in target_envs:
        if os.path.exists(env_file):
            with open(env_file, "r") as f:
                content = f.read()
            # Strip old injections
            lines = [l for l in content.splitlines() if not l.startswith(("MIN_CLIP_DURATION", "MAX_CLIP_DURATION", "CLIP_TARGET_MIN", "CLIP_TARGET_MAX", "SUBTITLE_MAX_LINES", "SUBTITLE_WORDS_PER_BATCH", "DUAL_ASPECT_RATIOS"))]
            new_content = "\n".join(lines) + "\n" + "\n".join(injections)
            with open(env_file, "w") as f:
                f.write(new_content)
            print(f"✅ Injected rules into {env_file}")

    print("🎉 All custom rules successfully patched into the engine!")

if __name__ == "__main__":
    patch()
