# VetNet AI - Backend Startup with Virtual Environment
# Activates animal_env and runs the backend

Write-Host "Starting VetNet AI Backend..." -ForegroundColor Green

# Activate virtual environment
Write-Host "Activating animal_env..." -ForegroundColor Yellow
& ".\animal_env\Scripts\Activate.ps1"

# Set environment variables
$env:PYTHONPATH = "."
$env:PYTHONIOENCODING = "utf-8"

# Start the API server
Write-Host "Starting API on http://localhost:8002" -ForegroundColor Green
Write-Host ""
python simple_api.py
