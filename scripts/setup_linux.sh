#!/bin/bash
# ==============================================================================
# OpenShorts RTX Setup Script for Linux / Ubuntu (WSL2)
# ==============================================================================

set -e

echo "🚀 Starting OpenShorts RTX 3060 Setup..."

# 1. Check NVIDIA GPU
if command -v nvidia-smi &> /dev/null; then
    echo "✅ NVIDIA Driver detected:"
    nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
else
    echo "❌ nvidia-smi not found! Please install NVIDIA drivers with CUDA support."
    exit 1
fi

# 2. Check Docker
if command -v docker &> /dev/null; then
    echo "✅ Docker detected."
else
    echo "❌ Docker not found! Please install Docker Engine / Docker Desktop."
    exit 1
fi

# 3. Create required directories
echo "📁 Creating working directories..."
mkdir -p output uploads .cache/huggingface models
chmod -R a+rwX output uploads .cache models

# 4. Check .env
if [ ! -f .env ]; then
    echo "📝 Creating .env from .env.example..."
    cp .env.example .env
    echo "⚠️ Please edit .env and insert your free GEMINI_API_KEY from https://aistudio.google.com/api-keys"
fi

echo "🎉 Setup complete! Run: docker compose up -d"
echo "🌐 Then open your browser at: http://localhost:5175"
