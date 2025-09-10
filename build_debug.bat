@echo off
echo 🔮 Daily Fortune App - Build Diagnostics
echo ==========================================

echo.
echo 🔍 Checking Python installation...
python --version
if %ERRORLEVEL% neq 0 (
    echo.
    echo ❌ PROBLEM: Python not found!
    echo.
    echo 💡 SOLUTIONS:
    echo    1. Install Python from: https://python.org/downloads/
    echo    2. During installation, check "Add Python to PATH"
    echo    3. Or download Python from Microsoft Store
    echo.
    echo 📋 After installing Python, run this script again
    goto :error
)

echo.
echo 🔍 Checking pip installation...
pip --version
if %ERRORLEVEL% neq 0 (
    echo.
    echo ❌ PROBLEM: pip not found!
    echo.
    echo 💡 SOLUTION: Reinstall Python with pip included
    goto :error
)

echo.
echo 🔍 Checking current directory...
echo Current directory: %CD%
if not exist main.py (
    echo.
    echo ❌ PROBLEM: main.py not found!
    echo.
    echo 💡 SOLUTION: Make sure you're in the dailyfortune folder
    echo    Your dailyfortune folder should contain:
    echo    - main.py
    echo    - gui.py
    echo    - fortune_data.py
    echo    - fortunes.json
    goto :error
)

echo.
echo ✅ All checks passed! Starting build...
echo.

REM Continue with the actual build...
goto :build

:error
echo.
echo ❌ Build cannot continue due to errors above
echo.
echo 🔧 QUICK FIXES:
echo    1. Install Python: https://python.org/downloads/
echo    2. Make sure "Add to PATH" is checked during install
echo    3. Restart Command Prompt after Python install
echo    4. Navigate to the dailyfortune folder
echo    5. Run this script again
echo.
echo Press any key to exit...
pause >nul
exit /b 1

:build
echo 📦 Installing PyInstaller...
pip install pyinstaller
if %ERRORLEVEL% neq 0 (
    echo ❌ Failed to install PyInstaller
    echo 💡 Try: pip install --user pyinstaller
    goto :error
)

echo.
echo 🏗️ Creating build directory...
if exist build_output rmdir /s /q build_output
mkdir build_output

echo.
echo 🔨 Building GUI application...
pyinstaller --onefile --windowed --name "DailyFortune" main.py
if %ERRORLEVEL% neq 0 (
    echo ❌ Build failed!
    echo.
    echo 💡 Possible solutions:
    echo    1. Try: python -m PyInstaller --onefile --windowed main.py
    echo    2. Check if antivirus is blocking
    echo    3. Run as Administrator
    goto :error
)

echo.
echo 🔨 Building console version...
pyinstaller --onefile --name "DailyFortune-Console" test_data.py

echo.
echo 📄 Copying files...
copy dist\DailyFortune.exe build_output\ >nul
copy dist\DailyFortune-Console.exe build_output\ >nul 2>nul
copy fortunes.json build_output\ >nul

echo.
echo 📄 Creating README...
(
echo # Daily Fortune App
echo.
echo ## How to Use:
echo 1. Double-click DailyFortune.exe
echo 2. Click "Get Today's Fortune"
echo 3. Come back tomorrow for a new fortune!
echo.
echo ## Files:
echo - DailyFortune.exe = Main app
echo - fortunes.json = Edit to add your own fortunes
echo.
echo Enjoy your daily inspiration! 🔮
) > build_output\README.txt

echo.
echo 🎉 BUILD COMPLETED SUCCESSFULLY!
echo.
echo 📁 Your files are in: build_output\
echo.
dir build_output
echo.
echo 🚀 Ready to share! You can now:
echo    - Double-click DailyFortune.exe to test
echo    - Share the build_output folder
echo    - Zip it up for distribution
echo.
echo Press any key to exit...
pause >nul
exit /b 0