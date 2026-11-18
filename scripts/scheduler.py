#!/usr/bin/env python3
"""
Clips Auto-Scheduler & Rule Enforcer
Enforces:
1. Video Duration: 15s - 45s min/max.
2. Formats: 16:9 for X/Twitter, 9:16 for Shorts/Reels/TikTok.
3. Subtitles: Always 1-line max on screen.
4. Schedule: 2-3 clips per day, with at least 2 hours gap between posts.
"""

import json
import os
import sys
from datetime import datetime, timedelta

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "clipping_rules.json")

def load_rules():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def validate_clip_duration(duration_sec, rules):
    min_sec = rules["duration_rules"]["min_seconds"]
    max_sec = rules["duration_rules"]["max_seconds"]
    if duration_sec < min_sec:
        return False, f"Clip is too short ({duration_sec}s < {min_sec}s)"
    if duration_sec > max_sec:
        return False, f"Clip is too long ({duration_sec}s > {max_sec}s)"
    return True, f"Clip valid ({duration_sec}s)"

def generate_schedule(num_clips=3, start_time=None):
    rules = load_rules()
    gap_hours = rules["publishing_schedule"]["min_gap_hours"]
    
    if start_time is None:
        start_time = datetime.now()
        # Round up to next full hour
        start_time = start_time.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    
    schedule = []
    current_slot = start_time
    
    for i in range(1, num_clips + 1):
        schedule.append({
            "slot_number": i,
            "scheduled_time": current_slot.strftime("%Y-%m-%d %H:%M:%S"),
            "destinations": {
                "x_twitter": {"aspect_ratio": "16:9", "format": "Landscape"},
                "youtube_shorts": {"aspect_ratio": "9:16", "format": "Vertical"},
                "instagram_reels": {"aspect_ratio": "9:16", "format": "Vertical"},
                "tiktok": {"aspect_ratio": "9:16", "format": "Vertical"}
            },
            "caption_rule": "1 line max (bouncing active word)",
            "min_gap_from_previous_hours": gap_hours if i > 1 else 0
        })
        current_slot += timedelta(hours=gap_hours)
        
    return schedule

def print_summary():
    rules = load_rules()
    print("=" * 60)
    print("🎬 CLIP AUTOMATION RULES")
    print("=" * 60)
    print(f"⏱️  Duration: Min {rules['duration_rules']['min_seconds']}s | Max {rules['duration_rules']['max_seconds']}s")
    print("📐 Aspect Ratios:")
    print("   • X (Twitter)  : 16:9 Landscape")
    print("   • Shorts/Reels : 9:16 Vertical")
    print(f"💬 Captions: Single line only ({rules['subtitles']['words_per_batch']} words batch, {rules['subtitles']['animation']} style)")
    print(f"📅 Daily Output: {rules['publishing_schedule']['clips_per_day']} clips/day (Min {rules['publishing_schedule']['min_gap_hours']} hours gap)")
    print("=" * 60)
    
    schedule = generate_schedule(rules['publishing_schedule']['clips_per_day'])
    print("\n📅 Generated Sample Posting Schedule for Today:")
    for item in schedule:
        print(f"  Slot #{item['slot_number']}: {item['scheduled_time']} | Gap: {item['min_gap_from_previous_hours']}h")
    print("=" * 60)

if __name__ == "__main__":
    print_summary()
