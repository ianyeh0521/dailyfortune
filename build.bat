@echo off
echo 🔮 Daily Fortune App - Windows Build
echo =====================================

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ Python not found. Please install Python 3.6+ first.
    pause
    exit /b 1
)

echo ✅ Python found

REM Install PyInstaller
echo 📦 Installing PyInstaller...
pip install pyinstaller
if %ERRORLEVEL% neq 0 (
    echo ❌ Failed to install PyInstaller
    pause
    exit /b 1
)

REM Create build directory
if exist build_output rmdir /s /q build_output
mkdir build_output

REM Build GUI version
echo 🔨 Building GUI application...
pyinstaller --onefile --windowed --name "DailyFortune" main.py
if %ERRORLEVEL% neq 0 (
    echo ❌ Build failed
    pause
    exit /b 1
)

REM Build console version
echo 🔨 Building console version...
pyinstaller --onefile --name "DailyFortune-Console" test_data.py

REM Copy files
echo 📄 Copying files...
copy dist\DailyFortune.exe build_output\
copy dist\DailyFortune-Console.exe build_output\
copy fortunes.json build_output\

REM Create README
echo 📄 Creating README...
echo # Daily Fortune App > build_output\README.txt
echo. >> build_output\README.txt
echo Double-click DailyFortune.exe to start the app! >> build_output\README.txt
echo Edit fortunes.json to customize your fortunes. >> build_output\README.txt

echo.
echo 🎉 Build completed successfully!
echo 📁 Files are in: build_output\
echo.
dir build_output
echo.
echo 🚀 Ready for distribution!
pause