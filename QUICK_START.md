# 🚀 Quick Start Guide - Daily Fortune App

## ❗ If build.bat doesn't work, try this:

### Step 1: Open Command Prompt
1. Press **Windows key + R**
2. Type: `cmd`
3. Press Enter

### Step 2: Navigate to your dailyfortune folder
```cmd
cd C:\path\to\your\dailyfortune
```
*Replace with your actual path*

### Step 3: Run the debug script
```cmd
build_debug.bat
```

This will tell you exactly what's wrong and how to fix it.

## 🔧 Common Problems & Solutions

### Problem 1: "Python is not recognized"
**Solution:** Install Python
1. Go to: https://python.org/downloads/
2. Download Python 3.12 (latest)
3. **IMPORTANT:** Check "Add Python to PATH" during install
4. Restart Command Prompt

### Problem 2: Script runs too fast to see
**Solution:** Use Command Prompt instead of double-clicking

### Problem 3: Permission denied
**Solution:** Run Command Prompt as Administrator
1. Right-click Command Prompt
2. Choose "Run as Administrator"

### Problem 4: Wrong folder
**Solution:** Make sure you're in the dailyfortune folder
- Should contain: main.py, gui.py, fortune_data.py, fortunes.json

## 🎯 Alternative: Manual Build

If scripts don't work, build manually:

```cmd
# 1. Install PyInstaller
pip install pyinstaller

# 2. Build the app
pyinstaller --onefile --windowed main.py

# 3. Find your .exe file in the dist/ folder
```

## ✅ Success Indicators

You'll know it worked when you see:
- `build_output` folder created
- `DailyFortune.exe` inside (15-25 MB)
- No error messages

## 🆘 Still Having Issues?

1. **Check Python version:** `python --version` (should be 3.6+)
2. **Check pip:** `pip --version`
3. **Try Microsoft Store Python** if regular Python doesn't work
4. **Run build_debug.bat** for detailed diagnostics

## 📞 What to Tell Me

If still stuck, tell me:
1. What error message you see
2. Output of: `python --version`
3. Output of: `pip --version`
4. Which Windows version you're using