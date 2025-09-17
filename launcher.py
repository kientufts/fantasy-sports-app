#!/usr/bin/env python3
"""
Cross-platform launcher for Fantasy Sports App
Works on Windows, macOS, and Linux
"""

import sys
import subprocess
import os
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.8 or higher"""
    if sys.version_info < (3, 8):
        print(f"Error: Python {sys.version_info.major}.{sys.version_info.minor} detected.")
        print("This app requires Python 3.8 or higher.")
        print("Please upgrade Python and try again.")
        return False
    return True


def install_requirements():
    """Install required packages if not already installed"""
    try:
        import flask
        return True
    except ImportError:
        print("Installing required dependencies...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            return True
        except subprocess.CalledProcessError:
            print("Error: Failed to install dependencies.")
            print("Please run: pip install -r requirements.txt")
            return False


def run_console_app():
    """Launch the console version"""
    print("Starting console app...")
    try:
        subprocess.run([sys.executable, "main.py"])
    except KeyboardInterrupt:
        print("\nApp stopped by user.")
    except Exception as e:
        print(f"Error running console app: {e}")


def run_web_app():
    """Launch the web version"""
    print("Starting web app...")
    print("Open http://localhost:5000 in your browser")
    print("Press Ctrl+C to stop the server")
    try:
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\nWeb server stopped by user.")
    except Exception as e:
        print(f"Error running web app: {e}")


def main():
    """Main launcher function"""
    print("Fantasy Sports App Launcher")
    print("==========================")
    print(f"Python version: {sys.version}")
    print(f"Platform: {sys.platform}")
    print()

    # Check Python version
    if not check_python_version():
        input("Press Enter to exit...")
        return

    # Check if we're in the right directory
    if not Path("main.py").exists() or not Path("app.py").exists():
        print("Error: Please run this script from the fantasy app directory")
        print("Make sure main.py and app.py are in the current directory")
        input("Press Enter to exit...")
        return

    # Install requirements if needed
    if not install_requirements():
        input("Press Enter to exit...")
        return

    # Show menu
    while True:
        print()
        print("Choose an option:")
        print("1) Run Console App")
        print("2) Run Web App")
        print("3) Exit")
        print()

        try:
            choice = input("Enter your choice (1-3): ").strip()
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

        if choice == "1":
            run_console_app()
        elif choice == "2":
            run_web_app()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
