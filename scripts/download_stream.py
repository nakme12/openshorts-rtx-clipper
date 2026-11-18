#!/usr/bin/env python3
"""
===============================================================================
Module: download_stream.py
Description: High-Performance Stream & Gameplay Downloader using yt-dlp.
Target Directory: Downloads 1080p60/4K video directly to ./uploads for clipping.
===============================================================================
"""

import argparse
import os
import shutil
import subprocess
import sys
from typing import Optional


def check_ytdlp_installed() -> bool:
    """Verifies that yt-dlp executable exists in the current system PATH."""
    return shutil.which("yt-dlp") is not None


def download_stream(
    url: str,
    output_dir: str = "./uploads",
    max_height: int = 1080
) -> Optional[str]:
    """
    Downloads full-resolution gameplay stream or video using yt-dlp.

    Args:
        url (str): Valid YouTube, Twitch, or Kick video URL.
        output_dir (str): Destination directory for the downloaded MP4.
        max_height (int): Maximum vertical resolution (default 1080p).

    Returns:
        Optional[str]: Path to the output directory if successful, None otherwise.
    """
    if not check_ytdlp_installed():
        print("[ERROR] 'yt-dlp' is not installed or not in PATH.")
        print("[HINT] Install it via: pip install -U yt-dlp")
        return None

    # Ensure output directory exists
    abs_output_dir = os.path.abspath(output_dir)
    os.makedirs(abs_output_dir, exist_ok=True)

    output_template = os.path.join(abs_output_dir, "%(title)s [%(id)s].%(ext)s")

    # Command optimized for fast muxing and maximum compatibility with FFmpeg/CUDA
    format_selector = (
        f"bestvideo[height<={max_height}][ext=mp4]+bestaudio[ext=m4a]/"
        f"bestvideo[height<={max_height}]+bestaudio/best[height<={max_height}]/best"
    )

    command = [
        "yt-dlp",
        "--format", format_selector,
        "--merge-output-format", "mp4",
        "--no-playlist",
        "--progress",
        "--output", output_template,
        url
    ]

    print("=" * 65)
    print(f"[INFO] Target URL   : {url}")
    print(f"[INFO] Destination  : {abs_output_dir}")
    print(f"[INFO] Max Quality  : {max_height}p")
    print("=" * 65)

    try:
        subprocess.run(command, check=True)
        print("=" * 65)
        print("[SUCCESS] Stream download completed successfully!")
        print(f"[SUCCESS] Ready in directory: {abs_output_dir}")
        print("=" * 65)
        return abs_output_dir
    except subprocess.CalledProcessError as exc:
        print(f"[ERROR] yt-dlp download failed with exit code {exc.returncode}")
        return None
    except Exception as exc:
        print(f"[ERROR] Unexpected error occurred during download: {exc}")
        return None


def main() -> None:
    """CLI Entry point with robust argument parsing."""
    parser = argparse.ArgumentParser(
        description="Download raw stream/gameplay footage for OpenShorts processing."
    )
    parser.add_argument(
        "url",
        type=str,
        help="YouTube or Twitch video/stream URL to download."
    )
    parser.add_argument(
        "-o", "--output-dir",
        type=str,
        default="./uploads",
        help="Custom destination directory (default: ./uploads)"
    )
    parser.add_argument(
        "-q", "--quality",
        type=int,
        default=1080,
        help="Maximum video vertical resolution (e.g., 720, 1080, 1440, 2160)"
    )

    args = parser.parse_args()
    result = download_stream(url=args.url, output_dir=args.output_dir, max_height=args.quality)

    if not result:
        sys.exit(1)


if __name__ == "__main__":
    main()
