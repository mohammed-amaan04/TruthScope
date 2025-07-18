@echo off
echo ========================================
echo Veritas Chrome Extension Setup
echo ========================================
echo.

echo STEP 1: Creating extension icons...
if not exist "icons" mkdir icons
echo Icons folder created (you can add custom icons later)
echo.

echo STEP 2: Make sure your Veritas backend is running:
echo    cd /path/to/veritas
echo    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
echo.

echo STEP 3: Install the extension:
echo    1. Open Chrome and go to: chrome://extensions/
echo    2. Enable "Developer mode" (toggle in top right)
echo    3. Click "Load unpacked" and select this folder:
echo       %~dp0
echo    4. The extension should now appear in your Chrome toolbar!
echo.

echo STEP 4: Test the extension:
echo    1. Go to any website
echo    2. Highlight some text
echo    3. Right-click and select "Fact-check with Veritas"
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.

echo Optional: Open create-icons.html to generate custom icons
echo.

echo Press any key to open Chrome extensions page...
pause >nul

start chrome://extensions/
