@echo off
chcp 65001 >nul
cls
echo Daily Fortune App Builder
echo ========================

python --version
if %ERRORLEVEL% neq 0 (
    echo Python not found. Please install Python first.
    pause
    exit /b 1
)

echo Python found!
echo Installing PyInstaller...
pip install pyinstaller

echo Building application...
pyinstaller --onefile --windowed --name DailyFortune main.py

if exist dist\DailyFortune.exe (
    echo Success! DailyFortune.exe created in dist folder
    copy dist\DailyFortune.exe .
    echo DailyFortune.exe copied to current folder
) else (
    echo Build failed
)

pause