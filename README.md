# OpenShorts RTX Clipper 🚀 (Asus TUF / RTX 3060 Optimized)

> **Zero API Cost AI Video Clipper:** Turn long gaming streams, podcasts, and gameplay videos into viral 9:16 Shorts, Reels, and TikToks with automated captions, smart face-tracking, and hook titles using your local NVIDIA GPU and Free Gemini Flash.

---

## ⚡ Architecture (Optimized for 6GB VRAM Laptops)

Traditional open-source video clippers require 16GB+ VRAM because they try to load heavy 7B-14B LLMs locally alongside Whisper and Computer Vision models.

This setup uses a **Hybrid High-Efficiency Architecture**:
1. **Moment Picking & Viral Scoring**: Powered by **Google Gemini Flash** (100% Free tier from Google AI Studio). Takes **0 GB GPU VRAM** and processes full transcripts in seconds.
2. **Audio Transcription**: Powered by **Faster-Whisper (`large-v3-turbo`)** running locally on CUDA FP16 (~1.8 GB VRAM).
3. **Smart Framing & Face Tracking**: Powered by **YOLOv8** to keep the gamer and gameplay centered in 9:16 format.
4. **Hardware Video Encoding**: Accelerated with NVIDIA **NVENC** via FFmpeg for fast rendering.

```
Long Video (.mp4)
       │
       ▼
 [ Faster-Whisper (CUDA) ] ──> Word-level Timestamps & Transcript
       │
       ▼
 [ Google Gemini Flash ] ────> Detects Top 5 Viral Moments & Hooks
       │
       ▼
 [ YOLOv8 Face Tracking ] ───> Smart 9:16 Crop & Reframe
       │
       ▼
 [ Remotion + FFmpeg NVENC ] ─> Burns Animated Subtitles & Exports
```

---

## 💻 Hardware Requirements

* **GPU**: NVIDIA GeForce RTX 3060 (6GB VRAM Laptop / 12GB Desktop), RTX 3070, RTX 4060, or higher.
* **OS**: Windows 11 with WSL2 & Docker Desktop, or Ubuntu 22.04+ LTS.
* **RAM**: 16 GB DDR4/DDR5 recommended.
* **Storage**: 15 GB free disk space for models & cache.

---

## 🚀 Quick Start Guide

### 1. Get Free Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/api-keys).
2. Sign in with your Google account.
3. Click **"Create API Key"** and copy your key.

---

### 2. Setup on Windows (Asus TUF A15 / Windows 11)

1. Make sure **Docker Desktop** is installed and running with WSL2 backend.
2. Clone this repository:
   ```powershell
   git clone https://github.com/nakme12/openshorts-rtx-clipper.git
   cd openshorts-rtx-clipper
   ```
3. Run the setup script:
   ```powershell
   .\scripts\setup_windows.ps1
   ```
4. Open `.env` and paste your `GEMINI_API_KEY`:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   GEMINI_MODEL=gemini-2.5-flash
   ```
5. Start the containers:
   ```powershell
   docker compose up -d
   ```
6. Open your browser at: **`http://localhost:5175`**

---

### 3. Setup on Linux / Ubuntu

1. Clone and configure:
   ```bash
   git clone https://github.com/nakme12/openshorts-rtx-clipper.git
   cd openshorts-rtx-clipper
   chmod +x scripts/setup_linux.sh
   ./scripts/setup_linux.sh
   ```
2. Insert your key into `.env`:
   ```bash
   nano .env
   ```
3. Launch:
   ```bash
   docker compose up -d
   ```
4. Open **`http://localhost:5175`**.

---

## 🎮 How to Process Videos

1. **Download Long Stream / Gameplay**:
   Use the included script to download in maximum quality:
   ```bash
   python scripts/download_stream.py "https://www.youtube.com/watch?v=VIDEO_ID"
   ```
2. Open the OpenShorts Web UI at `http://localhost:5175`.
3. Select your uploaded video or paste the direct link.
4. Set clip length (e.g. 30–60 seconds).
5. Click **"Generate Clips"**.
6. The engine will extract 5–10 vertical clips with word-by-word bouncing captions into the `./output` folder!

---

## 💰 Monetization Playbook

| Method | Potential | How it Works |
| :--- | :--- | :--- |
| **Clipper Bounties** | $500 – $2,500/mo | Upload to TikTok/Reels and link your clips to bounty platforms like Whop or Clip.cash ($0.50–$1.50 per 1k views). |
| **Affiliate Marketing** | $200 – $1,000/mo | Place gaming accessories, VPNs (NordVPN), or gear links in channel bio. |
| **Sponsorships** | $50 – $200/post | Gaming brands & indie game developers pay for dedicated promotions on 50k+ follower accounts. |

---

## ⚙️ Custom Pipeline & Posting Rules

All rules are pre-configured in [`config/clipping_rules.json`](./config/clipping_rules.json) and `.env`:

| Rule | Setting | Purpose |
| :--- | :--- | :--- |
| **Duration Limit** | `15s` Min – `45s` Max | Keeps retention high; eliminates boring fluff. |
| **Aspect Ratio for X** | `16:9` Landscape (1920x1080) | Perfect fit for Twitter/X timeline cards. |
| **Aspect Ratio for Shorts/Reels** | `9:16` Vertical (1080x1920) | Full screen vertical for TikTok, YouTube Shorts, Reels. |
| **Captions** | **Always 1 Line** | Max 1 line on screen, 3-word animated bouncy text. |
| **Daily Cadence** | `2 - 3` Clips per Day | Consistent algorithm push without tripping spam filters. |
| **Posting Gap** | **At least 2 Hours** | Spaces out posts across morning, evening, and night windows. |

### Run the Schedule Preview:
```bash
python scripts/scheduler.py
```

---

## 📱 Auto-Posting & Account Safety

Before enabling automated publishing, read the complete guide:
👉 **[Read the Auto-Posting & Anti-Ban Safety Guide](./docs/AUTO_POSTING_GUIDE.md)**

* **Avoid Shadowbans**: Learn why raw API scrapers get flagged and how to warm up new accounts.
* **The 7-Day Warmup**: How to safely transition from manual to scheduled posts.
* **Semi-Auto Draft Mode**: The 0% ban-risk method used by top clipping agencies.

---

## 📚 Documentation Index

Everything in this repository is modular, clean, and linked together:

| Document | Purpose |
| :--- | :--- |
| **[Architecture & Data Flow](./docs/ARCHITECTURE.md)** | Full system diagram, component linkages, and 6GB VRAM budget. |
| **[AI Agent & Dev Runbook](./docs/AGENT_RUNBOOK.md)** | Step-by-step commands, execution sequences, and error fixes for AI agents. |
| **[Auto-Posting & Safety Guide](./docs/AUTO_POSTING_GUIDE.md)** | Anti-ban rules, 7-day warmup, and the 1-tap mobile draft workflow. |
| **[Multi-Game Niche Playbook](./docs/NICHE_PLAYBOOK.md)** | Multi-game strategy (GTA + PUBG + Shooters), weekly schedule, and hooks. |
| **[Sources & Destinations](./docs/SOURCES_AND_DESTINATIONS.md)** | Exact verified channels to download from and upload platform matrix. |

---

## 🛠️ Project Structure

```
openshorts-rtx-clipper/
├── docker-compose.yml          # Core container definitions
├── docker-compose.override.yml # GPU device pass-through
├── .env.example                # 6GB VRAM optimized settings
├── scripts/
│   ├── setup_windows.ps1       # One-click Windows setup
│   ├── setup_linux.sh          # One-click Linux setup
│   └── download_stream.py      # yt-dlp downloader
└── templates/
    └── viral_hooks.json        # High-retention hooks & hashtags
```

---

## 📄 License & Credits
* Original OpenShorts Engine by [mutonby/openshorts](https://github.com/mutonby/openshorts).
* Faster-Whisper by SYSTRAN.
* YOLOv8 by Ultralytics.
