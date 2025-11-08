@echo off
REM Setup script for RTX Hackathon 2025 project (Windows)

echo ==================================
echo RTX Hackathon 2025 - Setup Script
echo ==================================
echo.

REM Check Python version
echo Checking Python version...
python --version

REM Create virtual environment
echo.
echo Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt

REM Check for CUDA
echo.
echo Checking for CUDA availability...
python -c "import torch; print(f'CUDA Available: {torch.cuda.is_available()}')"

echo.
echo ==================================
echo Setup Complete!
echo ==================================
echo.
echo To get started:
echo   1. Activate the virtual environment: venv\Scripts\activate.bat
echo   2. Run the main application: python src\main.py
echo   3. Try the examples: python examples\gpu_benchmark.py
echo.

pause
