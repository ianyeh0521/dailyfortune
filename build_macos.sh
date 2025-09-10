#!/bin/bash

echo "🍎 Daily Fortune - macOS Build Script"
echo "===================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.6+ first."
    echo "💡 Install from: https://python.org/downloads/"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Install PyInstaller
echo "📦 Installing PyInstaller..."
python3 -m pip install pyinstaller

# Build the application
echo "🔨 Building macOS application..."
python3 -m PyInstaller --onefile --windowed --add-data "fortunes.json:." --name "DailyFortune" main.py

# Create distribution folder
echo "📁 Creating distribution package..."
rm -rf release
mkdir release

if [ -f "dist/DailyFortune" ]; then
    cp dist/DailyFortune release/
    
    # Make executable
    chmod +x release/DailyFortune
    
    # Create README
    cat > release/README.txt << EOF
# Daily Fortune App for macOS

## How to Use:
1. Double-click DailyFortune to start
2. Click "Get Today's Fortune" 
3. Come back tomorrow for a new fortune!

## Features:
- One fortune per day
- Tracks your streak  
- Completely offline
- No installation required

## Note:
If you get a security warning:
1. Right-click DailyFortune
2. Select "Open"
3. Click "Open" in the dialog

Enjoy your daily inspiration! 🔮
EOF
    
    echo ""
    echo "🎉 BUILD SUCCESSFUL!"
    echo ""
    echo "📁 Distribution files:"
    ls -la release/
    echo ""
    echo "🚀 Ready for distribution!"
    echo "Users can run DailyFortune on any macOS 10.14+ system"
    
else
    echo "❌ BUILD FAILED"
    echo "Check error messages above"
fi