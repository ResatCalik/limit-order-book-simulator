& .\.venv\Scripts\python.exe -m pytest

if ($LASTEXITCODE -ne 0) {
    Write-Host "Tests failed. main.py will not run."
    exit $LASTEXITCODE
}

Write-Host "Tests passed. Running main.py..."
& .\.venv\Scripts\python.exe -m src.main

# .\run_checks.ps1 