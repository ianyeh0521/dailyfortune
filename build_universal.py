#!/usr/bin/env python3
"""
Universal Build Script for Daily Fortune App
Detects platform and builds appropriate executable
"""

import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path

class UniversalBuilder:
    def __init__(self):
        self.system = platform.system().lower()
        self.build_dir = Path("dist_release")
        self.app_name = "DailyFortune"
        
    def run_command(self, command, description):
        """Run a command and handle errors"""
        print(f"📦 {description}...")
        try:
            if isinstance(command, list):
                result = subprocess.run(command, capture_output=True, text=True)
            else:
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                
            if result.returncode != 0:
                print(f"❌ Error: {result.stderr}")
                return False
            print(f"✅ {description} completed")
            return True
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False

    def check_requirements(self):
        """Check if all requirements are met"""
        print("🔍 Checking requirements...")
        
        # Check Python version
        if sys.version_info < (3, 6):
            print("❌ Python 3.6 or higher required")
            return False
        print(f"✅ Python {sys.version.split()[0]} detected")
        
        # Check if fortunes.json exists
        if not Path("fortunes.json").exists():
            print("❌ fortunes.json not found")
            return False
        print("✅ Fortune database found")
        
        # Install PyInstaller if needed
        try:
            import PyInstaller
            print("✅ PyInstaller already installed")
        except ImportError:
            print("📦 Installing PyInstaller...")
            if not self.run_command([sys.executable, "-m", "pip", "install", "pyinstaller"], "Installing PyInstaller"):
                return False
        
        return True

    def clean_build(self):
        """Clean previous build artifacts"""
        print("🧹 Cleaning previous builds...")
        
        cleanup_dirs = ["build", "dist", "__pycache__", "*.spec"]
        for pattern in cleanup_dirs:
            if pattern.startswith("*"):
                # Handle glob patterns
                for path in Path(".").glob(pattern):
                    if path.is_file():
                        path.unlink()
                        print(f"   Removed {path}")
            else:
                path = Path(pattern)
                if path.exists():
                    if path.is_dir():
                        shutil.rmtree(path)
                    else:
                        path.unlink()
                    print(f"   Removed {path}")

        # Create fresh release directory
        if self.build_dir.exists():
            shutil.rmtree(self.build_dir)
        self.build_dir.mkdir()
        print(f"✅ Created {self.build_dir}")

    def build_windows(self):
        """Build Windows executable"""
        print("🖥️  Building for Windows...")
        
        # Build command with all necessary options
        build_cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--windowed",
            "--name", self.app_name,
            "--add-data", "fortunes.json;.",  # Windows uses semicolon
            "--distpath", str(self.build_dir),
            "main.py"
        ]
        
        # Try to add icon if it exists
        if Path("fortune.ico").exists():
            build_cmd.extend(["--icon", "fortune.ico"])
        
        if not self.run_command(build_cmd, "Building Windows executable"):
            return False
            
        return True

    def build_macos(self):
        """Build macOS executable"""  
        print("🍎 Building for macOS...")
        
        # Build command for macOS
        build_cmd = [
            sys.executable, "-m", "PyInstaller", 
            "--onefile",
            "--windowed",
            "--name", self.app_name,
            "--add-data", "fortunes.json:.",  # macOS/Linux uses colon
            "--distpath", str(self.build_dir),
            "main.py"
        ]
        
        if not self.run_command(build_cmd, "Building macOS executable"):
            return False
            
        # Make executable
        exe_path = self.build_dir / self.app_name
        if exe_path.exists():
            exe_path.chmod(0o755)
            print("✅ Made executable")
            
        return True

    def build_linux(self):
        """Build Linux executable"""
        print("🐧 Building for Linux...")
        
        # Build command for Linux  
        build_cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile", 
            "--windowed",
            "--name", self.app_name,
            "--add-data", "fortunes.json:.",
            "--distpath", str(self.build_dir),
            "main.py"
        ]
        
        if not self.run_command(build_cmd, "Building Linux executable"):
            return False
            
        # Make executable
        exe_path = self.build_dir / self.app_name
        if exe_path.exists():
            exe_path.chmod(0o755)
            print("✅ Made executable")
            
        return True

    def create_readme(self):
        """Create platform-specific README"""
        if self.system == "windows":
            exe_name = f"{self.app_name}.exe"
            data_location = r"C:\Users\[username]\.dailyfortune"
        else:
            exe_name = self.app_name
            data_location = "~/.dailyfortune"

        readme_content = f"""# Daily Fortune App

## How to Use
1. Double-click "{exe_name}" to start the app
2. Click "Get Today's Fortune" to receive your daily fortune  
3. Come back tomorrow for a new fortune!

## Features
- ✨ One unique fortune per day
- 📊 Track your daily streak
- 🔒 Completely offline - no internet required
- 💾 Remembers your fortune history
- 🎯 Over 1000 inspiring messages

## System Requirements
- {platform.system()} {platform.release()}+
- No installation required - just run the executable!

## Data Storage
Your fortune history is stored in: {data_location}

## Customizing Fortunes
The app includes over 1000 fortunes, but you can add more by editing
the fortune database after running the app for the first time.

## Troubleshooting
If the app doesn't start:
- Make sure your system allows running downloaded applications
- On macOS: Right-click → Open → Open (to bypass security warning)
- On Windows: Click "More info" → "Run anyway" if SmartScreen appears

---
Enjoy your daily dose of inspiration! 🔮

Built with ❤️ using Python and PyInstaller
"""

        readme_path = self.build_dir / "README.txt"
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(readme_content)
        
        print("✅ Created README.txt")

    def show_results(self):
        """Show build results"""
        print("\n" + "="*50)
        print("🎉 BUILD COMPLETED SUCCESSFULLY!")
        print("="*50)
        
        print(f"\n📁 Distribution files in: {self.build_dir.absolute()}")
        print("\n📦 Contents:")
        
        total_size = 0
        for file in self.build_dir.iterdir():
            if file.is_file():
                size_mb = file.stat().st_size / (1024*1024)
                total_size += size_mb
                print(f"   📄 {file.name} ({size_mb:.1f} MB)")
        
        print(f"\n💽 Total size: {total_size:.1f} MB")
        print(f"\n🚀 Ready for distribution!")
        print(f"   Users can run this on any {platform.system()} system")
        
        if self.system == "darwin":
            print("\n📝 macOS Note:")
            print("   Users may need to right-click → Open first time")
        elif self.system == "windows":  
            print("\n📝 Windows Note:")
            print("   Users may see SmartScreen warning - click 'Run anyway'")

    def build(self):
        """Main build process"""
        print(f"🔮 Daily Fortune App - Universal Builder")
        print(f"Platform: {platform.system()} {platform.release()}")
        print("="*50)
        
        # Check requirements
        if not self.check_requirements():
            print("❌ Requirements not met")
            return False
            
        # Clean previous builds
        self.clean_build()
        
        # Build for current platform
        success = False
        if self.system == "windows":
            success = self.build_windows()
        elif self.system == "darwin":
            success = self.build_macos() 
        elif self.system == "linux":
            success = self.build_linux()
        else:
            print(f"❌ Unsupported platform: {self.system}")
            return False
            
        if not success:
            print("❌ Build failed")
            return False
            
        # Create documentation
        self.create_readme()
        
        # Show results
        self.show_results()
        
        return True

def main():
    builder = UniversalBuilder()
    success = builder.build()
    
    if not success:
        sys.exit(1)
        
    print("\n🎊 Build process completed!")
    print("Share the dist_release folder with your users!")

if __name__ == "__main__":
    main()