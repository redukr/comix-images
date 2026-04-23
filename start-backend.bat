@echo off
echo ==========================================
echo   JOJ Comic Generator - Backend
echo ==========================================
echo.
echo Checking Python installation...
python --version

echo.
echo Installing dependencies (if needed)...
cd backend
pip install -r requirements.txt

echo.
echo Starting FastAPI server...
echo API will be available at: http://localhost:8000
echo Documentation: http://localhost:8000/docs
echo.

python main.py

pause
