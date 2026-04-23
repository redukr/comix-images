@echo off
echo ==========================================
echo   JOJ Comic Generator - Setup
echo ==========================================
echo.

echo Step 1: Checking prerequisites...
echo.

echo Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found! Please install Python 3.10+
    exit /b 1
)

echo Checking Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js not found! Please install Node.js 18+
    exit /b 1
)

echo.
echo Step 2: Setting up Backend...
cd backend
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install Python dependencies
    exit /b 1
)
cd ..

echo.
echo Step 3: Setting up Frontend...
cd frontend
npm install
if errorlevel 1 (
    echo ERROR: Failed to install Node.js dependencies
    exit /b 1
)
cd ..

echo.
echo Step 4: Checking JOJ data...
if not exist "data\joj-ranks.json" (
    echo WARNING: JOJ ranks data not found!
    echo Please copy JOJ-GAME-NEW\database\shared-ranks.json to data\joj-ranks.json
)
if not exist "data\joj-cards.json" (
    echo WARNING: JOJ cards data not found!
    echo Please copy JOJ-GAME-NEW\database\shared-deck-template.json to data\joj-cards.json
)

echo.
echo ==========================================
echo   Setup Complete!
echo ==========================================
echo.
echo To start the application:
echo   1. Make sure LLM Studio is running on port 1234
echo   2. Make sure ComfyUI is running on port 8188
echo   3. Run: start-backend.bat
echo   4. Run: start-frontend.bat (in new terminal)
echo.
echo Then open: http://localhost:3000
echo.

pause
