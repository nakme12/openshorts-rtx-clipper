#!/usr/bin/env python3
"""
===============================================================================
Module: patch_engine.py
Description: Translates high-level declarative clipping rules from 
             config/clipping_rules.json into operational environment variables 
             and runtime parameters consumed by the OpenShorts engine.
===============================================================================
"""

import argparse
import json
import os
import sys
from typing import Any, Dict, List

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_RULES_PATH = os.path.join(BASE_DIR, "config", "clipping_rules.json")
ENGINE_DIR = os.path.join(BASE_DIR, "engine")
ENGINE_ENV = os.path.join(ENGINE_DIR, ".env")
ROOT_ENV = os.path.join(BASE_DIR, ".env")


def load_rules(rules_path: str = DEFAULT_RULES_PATH) -> Dict[str, Any]:
    """
    Loads and validates the JSON clipping rules configuration.

    Args:
        rules_path (str): Absolute or relative path to clipping_rules.json.

    Returns:
        Dict[str, Any]: Parsed configuration dictionary.

    Raises:
        FileNotFoundError: If the specified rules file does not exist.
        ValueError: If JSON formatting or required sections are missing.
    """
    if not os.path.isfile(rules_path):
        raise FileNotFoundError(f"Configuration file not found: {rules_path}")

    with open(rules_path, "r", encoding="utf-8") as file_handle:
        data = json.load(file_handle)

    required_keys = ["duration_rules", "subtitles", "publishing_schedule"]
    missing = [k for k in required_keys if k not in data]
    if missing:
        raise ValueError(f"Invalid rules schema. Missing required sections: {missing}")

    return data


def build_env_injections(rules: Dict[str, Any]) -> List[str]:
    """
    Constructs clean, well-commented environment variable definitions
    derived from the user's clipping rules.
    """
    min_dur = rules["duration_rules"].get("min_seconds", 15)
    max_dur = rules["duration_rules"].get("max_seconds", 45)
    max_lines = rules["subtitles"].get("max_lines", 1)
    words_batch = rules["subtitles"].get("words_per_batch", 3)
    animation = rules["subtitles"].get("animation", "bounce")
    primary_color = rules["subtitles"].get("primary_color", "#FFFFFF")
    highlight_color = rules["subtitles"].get("highlight_color", "#FFD700")
    clips_per_day = rules["publishing_schedule"].get("clips_per_day", 3)

    return [
        "\n# ------------------------------------------------------------------------------",
        "# Auto-Injected from config/clipping_rules.json by scripts/patch_engine.py",
        "# ------------------------------------------------------------------------------",
        f"MIN_CLIP_DURATION={min_dur}",
        f"MAX_CLIP_DURATION={max_dur}",
        f"CLIP_TARGET_MIN={clips_per_day}",
        f"CLIP_TARGET_MAX={clips_per_day + 2}",
        f"SUBTITLE_MAX_LINES={max_lines}",
        f"SUBTITLE_WORDS_PER_BATCH={words_batch}",
        f"SUBTITLE_ANIMATION={animation}",
        f"SUBTITLE_PRIMARY_COLOR={primary_color}",
        f"SUBTITLE_HIGHLIGHT_COLOR={highlight_color}",
        "DUAL_ASPECT_RATIOS=16:9,9:16",
        "# ------------------------------------------------------------------------------\n"
    ]


def apply_patch(rules_path: str = DEFAULT_RULES_PATH, dry_run: bool = False) -> bool:
    """
    Applies configuration rules to both the root .env and engine/.env files.

    Args:
        rules_path (str): Path to clipping_rules.json.
        dry_run (bool): If True, previews changes without writing to disk.

    Returns:
        bool: True if patching succeeded, False otherwise.
    """
    try:
        rules = load_rules(rules_path)
    except Exception as exc:
        print(f"[ERROR] Failed to load rules: {exc}")
        return False

    injections = build_env_injections(rules)
    managed_prefixes = (
        "MIN_CLIP_DURATION",
        "MAX_CLIP_DURATION",
        "CLIP_TARGET_MIN",
        "CLIP_TARGET_MAX",
        "SUBTITLE_MAX_LINES",
        "SUBTITLE_WORDS_PER_BATCH",
        "SUBTITLE_ANIMATION",
        "SUBTITLE_PRIMARY_COLOR",
        "SUBTITLE_HIGHLIGHT_COLOR",
        "DUAL_ASPECT_RATIOS"
    )

    target_env_files = [ROOT_ENV]
    if os.path.isdir(ENGINE_DIR):
        target_env_files.append(ENGINE_ENV)

    print("[INFO] Initiating Engine Configuration Patch...")

    for env_path in target_env_files:
        if not os.path.exists(env_path):
            # If .env does not exist, initialize from .env.example
            example_path = os.path.join(BASE_DIR, ".env.example")
            if os.path.exists(example_path):
                with open(example_path, "r", encoding="utf-8") as src:
                    initial_content = src.read()
            else:
                initial_content = ""
        else:
            with open(env_path, "r", encoding="utf-8") as src:
                initial_content = src.read()

        # Remove existing managed keys to prevent duplicate entries
        cleaned_lines = [
            line for line in initial_content.splitlines()
            if not line.strip().startswith(managed_prefixes)
            and not line.strip().startswith("# Auto-Injected from config")
        ]

        updated_content = "\n".join(cleaned_lines) + "\n" + "\n".join(injections)

        if dry_run:
            print(f"[DRY-RUN] Previewing modifications for: {env_path}")
            print("\n".join(injections))
        else:
            with open(env_path, "w", encoding="utf-8") as dst:
                dst.write(updated_content)
            print(f"[SUCCESS] Patched configuration written to: {env_path}")

    print("[SUCCESS] All clipping constraints successfully synchronized with engine!")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Synchronize clipping_rules.json with OpenShorts runtime configuration."
    )
    parser.add_argument(
        "-c", "--config",
        type=str,
        default=DEFAULT_RULES_PATH,
        help="Custom path to clipping_rules.json"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate the patch without modifying .env files on disk."
    )

    args = parser.parse_args()
    success = apply_patch(rules_path=args.config, dry_run=args.dry_run)
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
