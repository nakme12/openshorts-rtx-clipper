# Exact Content Sources & Upload Destinations Guide

This guide details the exact verified channels and tools to download source gameplay from, and the precise file formats and destinations for publishing.

---

## 1. WHERE TO DOWNLOAD (Verified High-Retention Sources)

### A. Gaming & Open-World (GTA 6 / GTA 5)
* **Official Releases**: [Rockstar Games YouTube](https://www.youtube.com/@RockstarGames) (Official 4K trailers, announcements).
* **Physics, Stunts & Fails**:
  * *ENXGMA* — Hidden physics, easter eggs, NPC ragdoll mechanics.
  * *Badman Killa* & *Radical Gaming* — Crazy car stunts, map glitches.
* **Search Query to Find Fresh Content**:
  `"GTA 5 funny NPC moments 2026"` | `"GTA 6 trailer breakdown 4K"`

### B. Competitive Action (PUBG / BGMI / Shooters)
* **BGMI / Indian Streamers**:
  * *Jonathan Gaming*, *ScoutOP*, *Mortal*, *Mavi*.
  * Search: `"BGMI funny random squad voice chat"` | `"BGMI 1v4 clutch last zone"`.
* **Global PUBG Pros**:
  * *TGLTN*, *chocoTaco* (high-IQ squad wipes and sniper trickshots).

### C. Big Streamers & Reaction Kings
* **IShowSpeed**: [IShowSpeed YouTube Live Streams](https://www.youtube.com/@IShowSpeed) (Travel streams, funny crashes).
* **Kai Cenat**: [Kai Cenat Live](https://www.youtube.com/@KaiCenatLive) (Celebrity stream reactions).

### D. Download Methods
1. **Automated Terminal Script**:
   ```bash
   python scripts/download_stream.py "<YOUTUBE_OR_TWITCH_URL>"
   ```
   *(Saves automatically into `./uploads/<title>.mp4`)*
2. **Web Downloaders**:
   * [cobalt.tools](https://cobalt.tools) (Clean, zero ads, direct 1080p).
   * [snapyt.app](https://snapyt.app).

---

## 2. WHERE TO UPLOAD (Outputs & Platform Destinations)

When OpenShorts finishes processing, rendered videos appear in `./output/`:

### Local Folder Routing:
* 📁 **`./output/x_twitter/`**: Contains **16:9 Landscape (1920x1080)** clips.
* 📁 **`./output/vertical_shorts/`**: Contains **9:16 Vertical (1080x1920)** clips with 1-line bouncing subtitles.

### Online Platform Destination Matrix:

| Platform | Format Required | Target Account Profile | Monetization Mechanism |
| :--- | :--- | :--- | :--- |
| **X (Twitter)** | `16:9 Landscape` | Gaming Brand (e.g. `@ApexClutchGaming`) | X Creator Ad-Revenue (Impressions/Replies) |
| **YouTube Shorts** | `9:16 Vertical` | Gaming Shorts Channel | Shorts Fund / AdSense + Bio links |
| **Instagram Reels**| `9:16 Vertical` | Theme Page | Affiliate Bio Links + Mobile Game Sponsorships |
| **TikTok** | `9:16 Vertical` | TikTok Creator Profile | TikTok Creator Rewards Program + Clipper Bounties |

---

## 3. Recommended Transfer Workflow (PC to Mobile 1-Tap)

1. OpenShorts exports to `./output/`.
2. Move files to **Google Drive** or a private **Telegram Saved Messages** chat.
3. Open on your phone, save to camera roll.
4. Open the official mobile apps and tap **"Post"** in accordance with the 2-hour schedule in [`scripts/scheduler.py`](../scripts/scheduler.py).
