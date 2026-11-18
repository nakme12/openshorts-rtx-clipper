#!/usr/bin/env python3
"""
Stream & Gameplay Downloader using yt-dlp
Downloads full resolution gameplay or clips directly into ./uploads folder
"""
import sys
import subprocess
import os

def download_video(url, output_dir="./uploads"):
    os.makedirs(output_dir, exist_ok=True)
    out_template = os.path.join(output_dir, "%(title)s.%(ext)s")
    
    cmd = [
        "yt-dlp",
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "--merge-output-format", "mp4",
        "-o", out_template,
        url
    ]
    
    print(f"📥 Downloading: {url}")
    try:
        subprocess.run(cmd, check=True)
        print("✅ Download finished! The video is saved in uploads/ folder.")
    except FileNotFoundError:
        print("❌ yt-dlp is not installed. Install via: pip install yt-dlp")
    except subprocess.CalledProcessError as e:
        print(f"❌ Download failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python download_stream.py <YouTube_URL>")
        sys.exit(1)
    download_video(sys.argv[1])
