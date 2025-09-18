#!/usr/bin/env python3
"""
Fantasy Sports App - Quick Launcher
Universal cross-platform starter for Windows, macOS, and Linux
"""

import sys
import subprocess
import os
from pathlib import Path

def main():
    """Main launcher function"""
    print("Fantasy Sports App - Universal Launcher")
    print("======================================")
    
    # Check if we're in the right directory
    if not Path("main.py").exists():
        print("❌ Error: Please run this script from the fantasy app root directory")
        print("Make sure main.py exists in the current directory")
        input("Press Enter to exit...")
        return
    
    # Call the main launcher
    launcher_path = Path("scripts/launchers/launcher.py")
    if launcher_path.exists():
        print("🚀 Starting full launcher...")
        print()
        try:
            # Change to the launcher directory and run it
            original_cwd = os.getcwd()
            os.chdir("scripts/launchers")
            subprocess.run([sys.executable, "launcher.py"])
            os.chdir(original_cwd)
        except Exception as e:
            print(f"❌ Error running launcher: {e}")
            input("Press Enter to exit...")
    else:
        print("❌ Error: Main launcher not found at scripts/launchers/launcher.py")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()