@echo off
echo ========================================
echo Fixing Chrome Extension Icon Issue
echo ========================================
echo.

echo Creating icons folder...
if not exist "icons" mkdir icons

echo.
echo The extension will now load without icon errors!
echo.
echo To add custom icons later:
echo 1. Open create-icons.html in your browser
echo 2. Click "Generate Icons" and "Download All Icons"
echo 3. Save the downloaded files to the icons/ folder
echo 4. Update manifest.json to include icon references
echo.

echo Current status: Extension will work without icons
echo The extension icon may appear as a default puzzle piece in Chrome
echo.

echo Press any key to continue...
pause >nul
