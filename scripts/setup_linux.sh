#!/bin/bash
# ==============================================================================
# One-Click Fully Automated OpenShorts Setup for Linux / Ubuntu (WSL2)
# ==============================================================================

set -e

echo "=========================================================="
echo "🚀 Starting OpenShorts RTX 3060 One-Click Setup..."
echo "=========================================================="

# 1. Check NVIDIA GPU
if command -v nvidia-smi &> /dev/null; then
    echo "✅ NVIDIA GPU Detected:"
    nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
else
    echo "❌ nvidia-smi not detected! Please ensure NVIDIA drivers with CUDA are installed."
    exit 1
fi

# 2. Check Docker
if command -v docker &> /dev/null; then
    echo "✅ Docker detected."
else
    echo "❌ Docker not detected! Please install Docker Engine / Docker Desktop."
    exit 1
fi

# 3. Check / Clone Core OpenShorts Engine
if [ ! -d "engine" ]; then
    echo "📦 Cloning Core OpenShorts Engine from mutonby/openshorts..."
    git clone https://github.com/mutonby/openshorts.git engine
else
    echo "✅ Core Engine already present in ./engine"
fi

# 4. Create Working Directories
echo "📁 Setting up storage folders..."
mkdir -p output uploads .cache/huggingface models engine/output engine/uploads engine/.cache engine/models
chmod -R a+rwX output uploads .cache models engine/output engine/uploads engine/.cache engine/models

# 5. Apply RTX 3060 Optimized Configuration to Engine
echo "⚙️ Applying RTX 3060 (6GB VRAM) Gemini Flash Config..."
if [ ! -f .env ]; then
    cp .env.example .env
fi
cp .env engine/.env
cp docker-compose.override.yml engine/docker-compose.override.yml

# Run Rule Injector
if [ -f "scripts/patch_engine.py" ]; then
    python3 scripts/patch_engine.py
fi

# 6. Apply Remotion Fix
if [ -d "engine/render-service" ]; then
    echo "🔧 Applying Remotion renderer package lock fix..."
    cd engine/render-service
    docker run --rm -v "$(pwd):/w" -w /w node:18-bookworm-slim npm install --package-lock-only --save-exact @remotion/bundler@4.0.541 @remotion/renderer@4.0.541 remotion@4.0.541 || true
    cd ../..
fi

echo ""
echo "=========================================================="
echo "🎉 ONE-CLICK SETUP COMPLETE!"
echo "=========================================================="
echo "👉 1. Make sure your GEMINI_API_KEY is pasted in .env"
echo "👉 2. Run the engine with: cd engine && docker compose up -d"
echo "👉 3. Open Web UI: http://localhost:5175"
echo "=========================================================="
