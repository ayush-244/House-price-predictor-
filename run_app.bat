@echo off
echo ===================================================
echo   House Price Prediction Platform - Startup Script
echo ===================================================

echo.
echo [1/3] Checking for trained model...
if not exist "ml\models\best_model.joblib" (
    echo Model not found! Training model using master pipeline...
    python build_pipeline.py
) else (
    echo Model found.
)

echo.
echo [2/3] Starting Backend (Port 8000)...
start "Backend API" cmd /k "cd backend && uvicorn app.main:app --reload --port 8000"

echo.
echo [3/3] Starting Frontend (Port 3000)...
start "Frontend UI" cmd /k "cd frontend && npm run dev"

echo.
echo ===================================================
echo   All services started!
echo   Frontend: http://localhost:3000
echo   Backend:  http://localhost:8000
echo ===================================================
echo.
pause
