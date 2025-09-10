@echo off
chcp 65001 >nul
cls
echo Daily Fortune - Standalone Builder
echo ==================================

echo Installing PyInstaller...
pip install pyinstaller

echo Creating spec file...
pyi-makespec --onefile --windowed --name DailyFortune main.py

echo Building with all dependencies...
pyinstaller --onefile --windowed --add-data "fortunes.json;." --hidden-import tkinter --hidden-import tkinter.ttk --name DailyFortune main.py

if exist dist\DailyFortune.exe (
    echo Success! Creating distribution folder...
    if exist release rmdir /s /q release
    mkdir release
    copy dist\DailyFortune.exe release\
    copy fortunes.json release\
    echo.
    echo == Distribution Ready ==
    echo Files in release\ folder:
    dir release
    echo.
    echo Users can now run DailyFortune.exe directly!
) else (
    echo Build failed
)

pause