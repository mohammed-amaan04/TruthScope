@echo off
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║  🌐 VERITAS FRONTEND - React Interface                      ║
echo ║                                                              ║
echo ║  Starting the React development server...                   ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed!
    echo.
    echo 💡 Please install Node.js from: https://nodejs.org/
    echo    Download the LTS version and install it.
    echo.
    pause
    exit /b 1
)

echo ✅ Node.js found!

REM Check if dependencies are installed
if not exist "node_modules" (
    echo 📦 Installing dependencies...
    npm install
    if %errorlevel% neq 0 (
        echo ❌ Failed to install dependencies!
        pause
        exit /b 1
    )
)

echo 🚀 Starting React development server...
echo 📍 Frontend will be available at: http://localhost:3000
echo 🔗 Make sure the backend is running at: http://localhost:8000
echo ⏹️  Press Ctrl+C to stop the server
echo.

npm run dev

pause
