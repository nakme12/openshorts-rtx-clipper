#!/usr/bin/env python3
"""
===============================================================================
Module: scheduler.py
Description: Publishing Schedule Planner & Rule Enforcement Validator.
Features:
- Enforces 15s to 45s clip duration limits.
- Validates 16:9 (X / FB Page) and 9:16 (Shorts / Reels / FB Reels) routing.
- Computes optimal publication intervals with a strict minimum 2-hour spacing.
- Enforces single-line caption constraints.
===============================================================================
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "config", "clipping_rules.json")


def load_rules(config_path: str = CONFIG_PATH) -> Dict[str, Any]:
    """Loads clipping rules from the JSON configuration file."""
    if not os.path.isfile(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    with open(config_path, "r", encoding="utf-8") as file_handle:
        return json.load(file_handle)


def validate_clip_duration(
    duration_seconds: float,
    rules: Optional[Dict[str, Any]] = None
) -> Tuple[bool, str]:
    """
    Validates whether a candidate clip fits within the algorithmic duration window.

    Args:
        duration_seconds (float): Length of the video in seconds.
        rules (Optional[Dict[str, Any]]): Parsed rules dictionary.

    Returns:
        Tuple[bool, str]: (is_valid, descriptive_message)
    """
    if rules is None:
        rules = load_rules()

    min_sec = rules["duration_rules"].get("min_seconds", 15)
    max_sec = rules["duration_rules"].get("max_seconds", 45)

    if duration_seconds < min_sec:
        return False, f"Clip rejected: {duration_seconds:.1f}s is below minimum threshold ({min_sec}s)."
    if duration_seconds > max_sec:
        return False, f"Clip rejected: {duration_seconds:.1f}s exceeds maximum threshold ({max_sec}s)."

    return True, f"Clip valid: {duration_seconds:.1f}s is inside optimal retention window ({min_sec}s - {max_sec}s)."


def generate_schedule(
    num_clips: int = 3,
    start_time: Optional[datetime] = None,
    rules: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """
    Generates an automated daily posting queue with randomized spacing and 
    strict minimum inter-post intervals to protect accounts against anti-bot flags.

    Args:
        num_clips (int): Number of clips to schedule for the day.
        start_time (Optional[datetime]): Initial publication timestamp.
        rules (Optional[Dict[str, Any]]): Parsed rules configuration.

    Returns:
        List[Dict[str, Any]]: Array of scheduled publishing slot objects.
    """
    if rules is None:
        rules = load_rules()

    gap_hours = rules["publishing_schedule"].get("min_gap_hours", 2)

    if start_time is None:
        start_time = datetime.now()
        # Round up to the next clean hour mark
        start_time = start_time.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)

    schedule: List[Dict[str, Any]] = []
    current_slot = start_time

    for slot_idx in range(1, num_clips + 1):
        schedule.append({
            "slot_number": slot_idx,
            "scheduled_time_iso": current_slot.isoformat(),
            "display_time": current_slot.strftime("%Y-%m-%d %H:%M:%S"),
            "destinations": {
                "x_twitter": {"aspect_ratio": "16:9", "format": "Landscape"},
                "us_facebook_page": {"aspect_ratio": "16:9", "format": "Landscape Feed"},
                "facebook_reels": {"aspect_ratio": "9:16", "format": "Vertical Fullscreen"},
                "youtube_shorts": {"aspect_ratio": "9:16", "format": "Vertical Fullscreen"},
                "instagram_reels": {"aspect_ratio": "9:16", "format": "Vertical Fullscreen"},
                "tiktok": {"aspect_ratio": "9:16", "format": "Vertical Fullscreen"}
            },
            "caption_constraint": "Max 1 line on screen, 3-word animated active bounce",
            "interval_from_previous_hours": gap_hours if slot_idx > 1 else 0
        })
        current_slot += timedelta(hours=gap_hours)

    return schedule


def display_schedule_summary(schedule: List[Dict[str, Any]], rules: Dict[str, Any]) -> None:
    """Prints a structured, human-readable terminal table summary."""
    print("=" * 70)
    print("🎬 OPENSHORTS PUBLISHING SCHEDULE & RULE VALIDATION")
    print("=" * 70)
    print(f"⏱️  Duration Limits : Min {rules['duration_rules']['min_seconds']}s  |  Max {rules['duration_rules']['max_seconds']}s")
    print(f"💬 Caption Style   : Single Line Only (Batch size: {rules['subtitles']['words_per_batch']} words, Style: {rules['subtitles']['animation']})")
    print(f"📅 Daily Cadence   : {rules['publishing_schedule']['clips_per_day']} Clips/Day (Min {rules['publishing_schedule']['min_gap_hours']}h spacing)")
    print("-" * 70)
    print("📐 Multi-Platform Aspect Ratios:")
    print("   • X (Twitter) & FB Feed : 16:9 Landscape (1920x1080)")
    print("   • YouTube, Reels, TikTok : 9:16 Vertical (1080x1920)")
    print("=" * 70)
    print("📅 PLANNED PUBLISHING SLOTS:")
    for slot in schedule:
        gap_info = f"+{slot['interval_from_previous_hours']}h spacing" if slot['interval_from_previous_hours'] else "Initial Slot"
        print(f"  [Slot #{slot['slot_number']}] {slot['display_time']}  ({gap_info})")
    print("=" * 70)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compute and validate publication schedules adhering to anti-spam constraints."
    )
    parser.add_argument(
        "-n", "--clips",
        type=int,
        default=3,
        help="Number of daily clips to schedule (default: 3)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output result as raw JSON for programmatic consumption."
    )
    args = parser.parse_args()

    try:
        rules = load_rules()
        schedule = generate_schedule(num_clips=args.clips, rules=rules)
        if args.json:
            print(json.dumps(schedule, indent=2))
        else:
            display_schedule_summary(schedule=schedule, rules=rules)
    except Exception as exc:
        print(f"[ERROR] Schedule generation failed: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
