# AI Agent Runbook: Execution & Maintenance

> **For AI Agents & Developers**: This runbook provides clear, deterministic instructions to run, verify, and maintain the OpenShorts RTX Clipper pipeline.

---

## 1. Environment Verification

Before launching the pipeline, run the following verification checks:

```bash
# 1. Check NVIDIA Driver & CUDA
nvidia-smi --query-gpu=name,memory.total,memory.free --format=csv

# 2. Check Docker & Compose
docker compose version

# 3. Verify .env file exists and has GEMINI_API_KEY set
grep -E "GEMINI_API_KEY|GEMINI_MODEL" .env
```

---

## 2. Standard Execution Sequence

### Step 1: Start Background Services
```bash
docker compose up -d
```
Verify all containers report healthy:
```bash
docker compose ps
# Expected: openshorts-backend (Port 5175) and openshorts-renderer running
```

### Step 2: Download Source Video
```bash
python scripts/download_stream.py "<YOUTUBE_OR_TWITCH_URL>"
# File will be saved to ./uploads/<title>.mp4
```

### Step 3: Trigger Clipping Job
* Open the web interface at `http://localhost:5175` OR POST to the backend API:
* Ensure constraints match `config/clipping_rules.json`:
  * Duration: `min=15`, `max=45`
  * Captions: `max_lines=1`, `style=bounce`
  * Formats: 16:9 (for X) + 9:16 (for Shorts/Reels/TikTok)

### Step 4: Preview Publishing Schedule
```bash
python scripts/scheduler.py
```
This prints the 3 daily publication slots spaced by at least 2 hours.

---

## 3. Troubleshooting & Error Recovery

### A. CUDA Out of Memory (OOM)
* **Symptom**: `RuntimeError: CUDA out of memory` in `docker logs openshorts-backend`.
* **Fix**:
  1. Ensure local Ollama is NOT running on the GPU: `docker stop openshorts-ollama`.
  2. Verify `.env` has `GEMINI_MODEL=gemini-2.5-flash` so moment selection is offloaded to cloud API.
  3. If still tight, lower Whisper precision in `.env`:
     ```env
     WHISPER_MODEL=medium
     WHISPER_COMPUTE=int8
     ```

### B. Docker GPU Pass-Through Fails
* **Symptom**: `could not select device driver "" with capabilities: [[gpu, video]]`.
* **Fix**: Ensure NVIDIA Container Toolkit is installed:
  ```bash
  sudo apt-get install -y nvidia-container-toolkit
  sudo systemctl restart docker
  ```
  On Windows: Ensure Docker Desktop Settings -> Resources -> WSL Integration is enabled for Ubuntu.

### C. Captions Text Wrapping to Multiple Lines
* **Fix**: In `config/clipping_rules.json`, set `words_per_batch` to `2` or `3` to guarantee only 1 line appears on screen at any time.
