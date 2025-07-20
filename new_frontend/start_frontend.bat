@echo off
echo ========================================
echo Starting Truth Scope Frontend
echo ========================================
echo.

echo Checking if node_modules exists...
if not exist "node_modules" (
    echo Installing dependencies...
    npm install
    echo.
)

echo Starting development server...
echo Frontend will be available at: http://localhost:3001
echo.

npm run dev
