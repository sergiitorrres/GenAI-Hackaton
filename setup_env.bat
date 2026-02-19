@echo off
setlocal

echo ========================================
echo Checking for Python...
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not found in PATH!
    echo Please install Python 3.12 or ensure it is in your PATH.
    pause
    exit /b 1
)
python --version

echo ========================================
echo Creating virtual environment (.venv)...
if not exist ".venv" (
    python -m venv .venv
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

echo ========================================
echo Upgrading pip and installing requirements...
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
if exist "requirements.txt" (
    pip install -r requirements.txt
    echo.
    echo Dependencies installed successfully.
) else (
    echo requirements.txt not found!
    pause
    exit /b 1
)

echo ========================================
echo Setup complete!
echo.
echo To run your app, use:
echo .venv\Scripts\python app\main.py
echo.
pause
