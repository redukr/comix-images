@echo off
echo ==========================================
echo   JOJ Comic Generator - Frontend
echo ==========================================
echo.
echo Checking Node.js installation...
node --version

echo.
echo Installing dependencies (if needed)...
cd frontend
npm install

echo.
echo Starting Next.js dev server...
echo Frontend will be available at: http://localhost:3000
echo.

npm run dev

pause
