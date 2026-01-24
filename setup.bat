@echo off
setlocal enabledelayedexpansion

echo ======================================================
echo    FakeLingoes - Automated Environment Setup
echo ======================================================

:: Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.10+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Creating virtual environment...
if not exist venv (
    python -m venv venv
    if !errorlevel! neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo Virtual environment created successfully.
) else (
    echo Virtual environment already exists. Skipping...
)

echo [2/4] Upgrading pip, setuptools, and wheel...
.\venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel

echo [3/4] Installing dependencies from requirements.txt...
if exist requirements.txt (
    .\venv\Scripts\pip install -r requirements.txt
    if !errorlevel! neq 0 (
        echo [ERROR] Failed to install dependencies.
        pause
        exit /b 1
    )
    echo Dependencies installed successfully.
) else (
    echo [WARNING] requirements.txt not found. Skipping dependency installation.
)

echo [4/4] Creating project structure markers...
.\venv\Scripts\python.exe -c "import os; paths=['src/__init__.py', 'src/fake_lingoes/__init__.py', 'src/fake_lingoes/ui/__init__.py', 'src/fake_lingoes/services/__init__.py', 'src/fake_lingoes/services/ocr/__init__.py', 'src/fake_lingoes/services/dictionary/__init__.py', 'src/fake_lingoes/services/audio/__init__.py', 'src/fake_lingoes/services/translation/__init__.py', 'src/fake_lingoes/utils/__init__.py']; [open(p, 'a').close() for p in paths if not os.path.exists(p)]"

echo ======================================================
echo    Setup completed successfully!
echo ======================================================
echo To start debugging, open the project in VS Code and press F5.
echo To build the EXE, run: .\venv\Scripts\pyinstaller FakeLingoes.spec
echo ======================================================

pause
