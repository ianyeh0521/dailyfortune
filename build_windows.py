#!/usr/bin/env python3
"""
Windows Build Script for Daily Fortune App
Run this on Windows with Python installed
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"📦 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Error: {result.stderr}")
            return False
        print(f"✅ {description} completed")
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    print("🔮 Daily Fortune App - Windows Build Script")
    print("=" * 50)
    
    # Check if we're on Windows
    if os.name != 'nt':
        print("⚠️  This script should be run on Windows")
        print("   Copy the dailyfortune folder to Windows and run there")
        return
    
    # Check Python version
    if sys.version_info < (3, 6):
        print("❌ Python 3.6 or higher required")
        return
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Install PyInstaller
    if not run_command("pip install pyinstaller", "Installing PyInstaller"):
        print("❌ Failed to install PyInstaller")
        return
    
    # Create build directory
    build_dir = Path("build_output")
    if build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir()
    
    print("📁 Created build directory")
    
    # Build executable (GUI version)
    build_command = """pyinstaller --onefile --windowed --name "DailyFortune" --icon=fortune.ico main.py"""
    if not run_command(build_command, "Building GUI executable"):
        print("⚠️  Building without icon...")
        build_command = """pyinstaller --onefile --windowed --name "DailyFortune" main.py"""
        if not run_command(build_command, "Building GUI executable (no icon)"):
            return
    
    # Build console version for debugging
    console_command = """pyinstaller --onefile --name "DailyFortune-Console" test_data.py"""
    run_command(console_command, "Building console executable")
    
    # Copy files to build directory
    dist_dir = Path("dist")
    if dist_dir.exists():
        for file in dist_dir.glob("*.exe"):
            shutil.copy2(file, build_dir)
            print(f"📄 Copied {file.name}")
    
    # Copy fortune data
    shutil.copy2("fortunes.json", build_dir)
    print("📄 Copied fortunes.json")
    
    # Create README for distribution
    readme_content = '''# Daily Fortune App

## How to Use
1. Double-click "DailyFortune.exe" to start the app
2. Click "Get Today's Fortune" to receive your daily fortune
3. Come back tomorrow for a new fortune!

## Files Included
- DailyFortune.exe - Main application (GUI)
- DailyFortune-Console.exe - Console version for testing
- fortunes.json - Fortune database (you can edit this!)

## Customizing Fortunes
Edit "fortunes.json" to add your own fortunes:
- Add new entries with unique IDs
- Categories: "encouraging", "motivational", "general"

## Data Storage
Your fortune history is stored in:
C:\\Users\\[username]\\AppData\\Roaming\\.dailyfortune\\

Enjoy your daily dose of inspiration! 🔮
'''
    
    with open(build_dir / "README.txt", "w") as f:
        f.write(readme_content)
    
    print("📄 Created README.txt")
    
    print("\n🎉 Build completed successfully!")
    print(f"📁 Files are in: {build_dir.absolute()}")
    print("\n📦 Distribution files:")
    for file in build_dir.glob("*"):
        file_size = file.stat().st_size / (1024*1024)
        print(f"   {file.name} ({file_size:.1f} MB)")
    
    print("\n🚀 Ready for distribution!")
    print("   You can now share the build_output folder")

if __name__ == "__main__":
    main()