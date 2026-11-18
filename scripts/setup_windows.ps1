# ==============================================================================
# OpenShorts RTX Setup Script for Windows (PowerShell)
# ==============================================================================

Write-Host "🚀 Starting OpenShorts RTX 3060 Setup on Windows..." -ForegroundColor Cyan

# 1. Check NVIDIA Driver
try {
    $gpu = nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
    Write-Host "✅ GPU Detected: $gpu" -ForegroundColor Green
} catch {
    Write-Host "❌ nvidia-smi not detected! Please ensure NVIDIA drivers are installed." -ForegroundColor Red
}

# 2. Check Docker Desktop
try {
    docker version | Out-Null
    Write-Host "✅ Docker Desktop is running." -ForegroundColor Green
} catch {
    Write-Host "❌ Docker Desktop is not running or not in PATH! Please start Docker Desktop." -ForegroundColor Red
}

# 3. Create folders
Write-Host "📁 Creating storage folders..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path output, uploads, .cache, models | Out-Null

# 4. Copy .env
if (-not (Test-Path .env)) {
    Copy-Item .env.example .env
    Write-Host "📝 Created .env from .env.example" -ForegroundColor Yellow
    Write-Host "⚠️ Remember to put your GEMINI_API_KEY in .env file!" -ForegroundColor Magenta
}

Write-Host "`n🎉 Ready! Run: docker compose up -d" -ForegroundColor Green
Write-Host "🌐 Dashboard will be at: http://localhost:5175" -ForegroundColor Cyan
