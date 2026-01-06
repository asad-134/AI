# Multi-Agent Dashboard Installation Script
# Run this script to set up everything automatically

Write-Host "================================" -ForegroundColor Cyan
Write-Host "Multi-Agent Dashboard Setup" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Function to check if command exists
function Test-CommandExists {
    param($command)
    $null = Get-Command $command -ErrorAction SilentlyContinue
    return $?
}

# Step 1: Check Python
Write-Host "[1/6] Checking Python installation..." -ForegroundColor Yellow
if (Test-CommandExists python) {
    $pythonVersion = python --version
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "✗ Python not found!" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from: https://www.python.org/downloads/" -ForegroundColor Red
    exit 1
}

# Step 2: Check pip
Write-Host "[2/6] Checking pip..." -ForegroundColor Yellow
if (Test-CommandExists pip) {
    Write-Host "✓ pip found" -ForegroundColor Green
} else {
    Write-Host "✗ pip not found!" -ForegroundColor Red
    exit 1
}

# Step 3: Check Ollama
Write-Host "[3/6] Checking Ollama installation..." -ForegroundColor Yellow
if (Test-CommandExists ollama) {
    $ollamaVersion = ollama --version
    Write-Host "✓ Ollama found: $ollamaVersion" -ForegroundColor Green
    
    # Check if Mistral 7B is installed
    Write-Host "Checking for Mistral 7B model..." -ForegroundColor Yellow
    $models = ollama list
    if ($models -match "mistral") {
        Write-Host "✓ Mistral 7B already installed" -ForegroundColor Green
    } else {
        Write-Host "⚠ Mistral 7B not found. Installing..." -ForegroundColor Yellow
        Write-Host "This will download ~4.1GB. Please wait..." -ForegroundColor Cyan
        ollama pull mistral:7b
        Write-Host "✓ Mistral 7B installed" -ForegroundColor Green
    }
} else {
    Write-Host "✗ Ollama not found!" -ForegroundColor Red
    Write-Host "Please install Ollama from: https://ollama.ai/download" -ForegroundColor Yellow
    Write-Host "After installation, run this script again." -ForegroundColor Yellow
    exit 1
}

# Step 4: Install Python packages
Write-Host "[4/6] Installing Python dependencies..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor Cyan

pip install -r requirements.txt --quiet

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Python packages installed successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to install some packages" -ForegroundColor Red
    Write-Host "Try running: pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}

# Step 5: Verify installations
Write-Host "[5/6] Verifying installations..." -ForegroundColor Yellow

$verifyScript = @"
import streamlit
import pandas
import plotly
import ollama
print('SUCCESS')
"@

$result = python -c $verifyScript 2>&1
if ($result -match "SUCCESS") {
    Write-Host "✓ All packages verified" -ForegroundColor Green
} else {
    Write-Host "⚠ Some packages may have issues" -ForegroundColor Yellow
    Write-Host $result -ForegroundColor Gray
}

# Step 6: Check for dataset
Write-Host "[6/6] Checking for dataset..." -ForegroundColor Yellow
if (Test-Path "ifood_df.csv") {
    Write-Host "✓ Dataset found: ifood_df.csv" -ForegroundColor Green
} else {
    Write-Host "⚠ Dataset not found: ifood_df.csv" -ForegroundColor Yellow
    Write-Host "You'll need to upload your own CSV when running the app" -ForegroundColor Yellow
}

# Final summary
Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To start the dashboard, run:" -ForegroundColor Yellow
Write-Host "  streamlit run app.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "The dashboard will open at: http://localhost:8501" -ForegroundColor Yellow
Write-Host ""
Write-Host "Useful commands:" -ForegroundColor Yellow
Write-Host "  ollama list              - Show installed models" -ForegroundColor Gray
Write-Host "  ollama serve             - Start Ollama service" -ForegroundColor Gray
Write-Host "  streamlit run app.py     - Start dashboard" -ForegroundColor Gray
Write-Host ""

# Optional: Ask to start now
Write-Host "Would you like to start the dashboard now? (Y/N)" -ForegroundColor Cyan
$response = Read-Host

if ($response -eq 'Y' -or $response -eq 'y') {
    Write-Host ""
    Write-Host "Starting dashboard..." -ForegroundColor Green
    Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
    Write-Host ""
    
    # Check if Ollama is running
    $ollamaProcess = Get-Process -Name "ollama" -ErrorAction SilentlyContinue
    if (-not $ollamaProcess) {
        Write-Host "Starting Ollama service..." -ForegroundColor Yellow
        Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden
        Start-Sleep -Seconds 3
    }
    
    # Start Streamlit
    streamlit run app.py
} else {
    Write-Host ""
    Write-Host "Setup complete! Run 'streamlit run app.py' when ready." -ForegroundColor Green
    Write-Host ""
}
