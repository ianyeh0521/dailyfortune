#!/usr/bin/env python3
"""
Create README file for distribution
"""
import os
import sys

def create_readme(platform, exe_name):
    os.makedirs('dist', exist_ok=True)
    
    if platform == 'Windows':
        storage_path = r'C:\Users\[username]\.dailyfortune'
        notes = '- First run may show Windows security warning - click "Run anyway"'
    else:
        storage_path = '~/.dailyfortune'
        notes = '- First run may need right-click → "Open" to bypass security check'

    readme = f'''# Daily Fortune Cookie - {platform} Version

## How to Use
1. Double-click "{exe_name}" to start
2. Click "Get Today's Fortune" to receive your daily fortune
3. Come back tomorrow for a new fortune!

## System Requirements
- {platform} (recent version)
- No Python installation needed

## Notes
{notes}
- Your fortune history is stored in: {storage_path}

Enjoy your daily dose of inspiration! 🥠
'''

    with open('dist/README.txt', 'w', encoding='utf-8') as f:
        f.write(readme)
    print('README created successfully')

if __name__ == '__main__':
    platform = sys.argv[1] if len(sys.argv) > 1 else 'Unknown'
    exe_name = sys.argv[2] if len(sys.argv) > 2 else 'DailyFortuneCookie'
    create_readme(platform, exe_name)