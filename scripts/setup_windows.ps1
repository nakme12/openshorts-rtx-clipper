<#
.SYNOPSIS
One-Click Fully Automated OpenShorts Setup for Windows (Asus TUF / RTX 3060)
#>

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "🚀 Starting OpenShorts RTX 3060 One-Click Setup..." -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Check NVIDIA Driver
try {
    $gpu = nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
    Write-Host "✅ NVIDIA GPU Detected: $gpu" -ForegroundColor Green
} catch {
    Write-Host "❌ nvidia-smi not detected! Please ensure NVIDIA drivers are installed." -ForegroundColor Red
    exit 1
}

# 2. Check Docker Desktop
try {
    docker version | Out-Null
    Write-Host "✅ Docker Desktop is running." -ForegroundColor Green
} catch {
    Write-Host "❌ Docker Desktop is not running! Please start Docker Desktop with WSL2 backend." -ForegroundColor Red
    exit 1
}

# 3. Check / Clone Core OpenShorts Engine
if (-not (Test-Path "engine")) {
    Write-Host "📦 Cloning Core OpenShorts Engine from mutonby/openshorts..." -ForegroundColor Yellow
    git clone https://github.com/mutonby/openshorts.git engine
} else {
    Write-Host "✅ Core Engine already present in ./engine" -ForegroundColor Green
}

# 4. Create Working Directories
Write-Host "📁 Setting up storage folders..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path output, uploads, .cache, models, engine/output, engine/uploads, engine/.cache, engine/models | Out-Null

# 5. Apply RTX 3060 Optimized Configuration to Engine
Write-Host "⚙️ Applying RTX 3060 (6GB VRAM) Gemini Flash Config..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Copy-Item .env.example .env
}
Copy-Item .env engine/.env -Force
Copy-Item docker-compose.override.yml engine/docker-compose.override.yml -Force

# Run Rule Injector
if (Test-Path "scripts/patch_engine.py") {
    python scripts/patch_engine.py
}

# 6. Apply Remotion Fix
if (Test-Path "engine/render-service") {
    Write-Host "🔧 Applying Remotion renderer package lock fix..." -ForegroundColor Yellow
    Push-Location "engine/render-service"
    try {
        docker run --rm -v "${PWD}:/w" -w /w node:18-bookworm-slim npm install --package-lock-only --save-exact @remotion/bundler@4.0.541 @remotion/renderer@4.0.541 remotion@4.0.541
    } catch {
        Write-Host "⚠️ Docker npm install notice: will proceed with standard build." -ForegroundColor Gray
    }
    Pop-Location
}

Write-Host "`n==========================================================" -ForegroundColor Green
Write-Host "🎉 ONE-CLICK SETUP COMPLETE!" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
Write-Host "👉 1. Make sure your GEMINI_API_KEY is pasted in .env" -ForegroundColor Yellow
Write-Host "👉 2. Run the engine with: cd engine; docker compose up -d" -ForegroundColor Cyan
Write-Host "👉 3. Open Web UI: http://localhost:5175" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Green
