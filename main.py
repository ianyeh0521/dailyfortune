#!/usr/bin/env python3
"""
Daily Fortune App - Main Entry Point
Simple offline fortune application with daily limit
"""

import sys
import os
from gui import FortuneApp

def main():
    try:
        app = FortuneApp()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()