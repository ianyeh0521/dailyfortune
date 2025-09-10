@echo off
chcp 65001 >nul
cls
echo Daily Fortune - Final Standalone Build
echo ======================================

echo Step 1: Installing PyInstaller...
pip install pyinstaller

echo.
echo Step 2: Building standalone executable...
pyinstaller DailyFortune.spec

echo.
echo Step 3: Creating distribution package...
if exist release rmdir /s /q release
mkdir release

if exist dist\DailyFortune.exe (
    copy dist\DailyFortune.exe release\
    
    echo # Daily Fortune App > release\README.txt
    echo. >> release\README.txt
    echo Double-click DailyFortune.exe to start! >> release\README.txt
    echo No installation required - runs immediately. >> release\README.txt
    echo. >> release\README.txt
    echo Features: >> release\README.txt
    echo - One fortune per day >> release\README.txt
    echo - Tracks your streak >> release\README.txt
    echo - Completely offline >> release\README.txt
    echo. >> release\README.txt
    echo Enjoy your daily inspiration! >> release\README.txt
    
    echo.
    echo == BUILD SUCCESSFUL ==
    echo.
    echo Distribution files:
    dir release
    echo.
    echo File sizes:
    for %%f in (release\*) do echo %%~nxf: %%~zf bytes
    echo.
    echo Ready for distribution!
    echo Users can now run DailyFortune.exe on any Windows machine.
    echo No Python or source files needed!
    
) else (
    echo == BUILD FAILED ==
    echo Check for error messages above
)

echo.
pause