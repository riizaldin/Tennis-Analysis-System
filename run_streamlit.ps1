# Tennis Analysis Streamlit App - Quick Launcher
# Double-click this file to run the app

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "🎾 TENNIS ANALYSIS WEB APP" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (Test-Path ".venv\Scripts\Activate.ps1") {
    Write-Host "✅ Virtual environment found" -ForegroundColor Green
    Write-Host "🔄 Activating virtual environment..." -ForegroundColor Yellow
    & .\.venv\Scripts\Activate.ps1
} else {
    Write-Host "⚠️  Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please create virtual environment first:" -ForegroundColor Yellow
    Write-Host "  python -m venv .venv" -ForegroundColor White
    Write-Host "  .\.venv\Scripts\Activate.ps1" -ForegroundColor White
    Write-Host "  pip install -r requirements_streamlit.txt" -ForegroundColor White
    pause
    exit
}

Write-Host ""
Write-Host "🔍 Checking dependencies..." -ForegroundColor Yellow

# Check if streamlit is installed
$streamlitInstalled = python -c "import streamlit" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Streamlit not installed!" -ForegroundColor Red
    Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements_streamlit.txt
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Installation failed!" -ForegroundColor Red
        pause
        exit
    }
}

Write-Host "✅ All dependencies installed" -ForegroundColor Green
Write-Host ""

# Check model files
Write-Host "🔍 Checking model files..." -ForegroundColor Yellow

$courtModel = "training\Court-Keypoints\exps\skripsi_resnet50\model_best.pt"
$ballModel = "models\yolo8_best.pt"
$playerModel = "yolov8x.pt"

$missingModels = @()

if (!(Test-Path $courtModel)) {
    $missingModels += "Court Keypoints: $courtModel"
}

if (!(Test-Path $ballModel)) {
    $missingModels += "Ball Detection: $ballModel"
}

if (!(Test-Path $playerModel)) {
    $missingModels += "Player Detection: $playerModel"
}

if ($missingModels.Count -gt 0) {
    Write-Host "⚠️  Warning: Some models are missing:" -ForegroundColor Yellow
    foreach ($model in $missingModels) {
        Write-Host "  - $model" -ForegroundColor Red
    }
    Write-Host ""
    Write-Host "The app will still run, but you'll need to specify correct paths." -ForegroundColor Yellow
    Write-Host ""
} else {
    Write-Host "✅ All models found" -ForegroundColor Green
}

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "🚀 STARTING STREAMLIT APP..." -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "The app will open in your browser at: http://localhost:8501" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Run Streamlit
streamlit run streamlit_app.py

# If Streamlit exits
Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "App closed. Press any key to exit..." -ForegroundColor Yellow
pause
