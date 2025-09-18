#!/bin/bash

echo "Daily Fortune - macOS App Bundle Build Script"
echo "============================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 not found. Please install Python 3.6+ first."
    echo "Install from: https://python.org/downloads/"
    exit 1
fi

echo "Python 3 found: $(python3 --version)"

# Install PyInstaller
echo "Installing PyInstaller..."
python3 -m pip install pyinstaller

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build dist *.spec release_app

# Build the application as .app bundle
echo "Building macOS .app bundle..."
python3 -m PyInstaller \
    --onedir \
    --windowed \
    --add-data "fortunes.json:." \
    --name "DailyFortune" \
    main.py

# Create distribution folder
echo "Creating distribution package..."
mkdir release_app

if [ -d "dist/DailyFortune.app" ]; then
    cp -R dist/DailyFortune.app release_app/
    
    # Create README
    cat > release_app/README.txt << EOF
# Daily Fortune App for macOS (.app bundle)

## How to Use:
1. Drag DailyFortune.app to your Applications folder (optional)
2. Double-click DailyFortune.app to start
3. Click "Get Today's Fortune" 
4. Come back tomorrow for a new fortune!

## Features:
- One fortune per day
- Tracks your streak  
- Completely offline
- No installation required
- No console window (clean GUI experience)

## Installation:
- Simply drag DailyFortune.app to Applications folder
- Or run directly from any location

## Note:
If you get a security warning on first launch:
1. Right-click DailyFortune.app
2. Select "Open"
3. Click "Open" in the dialog

This .app bundle provides the cleanest user experience with no console windows.

Enjoy your daily inspiration!
EOF
    
    echo ""
    echo "BUILD SUCCESSFUL!"
    echo ""
    echo "Distribution files:"
    ls -la release_app/
    echo ""
    echo "App bundle size:"
    du -sh release_app/DailyFortune.app
    echo ""
    echo "Ready for distribution!"
    echo "Users can drag DailyFortune.app to Applications folder"
    echo "No console window will appear when launched"
    
else
    echo "BUILD FAILED"
    echo "Check error messages above"
fi