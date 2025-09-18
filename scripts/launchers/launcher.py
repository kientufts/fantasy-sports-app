#!/usr/bin/env python3
"""
Cross-platform launcher for Fantasy Sports App
Works on Windows, macOS, and Linux
"""

import sys
import subprocess
import os
import time
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
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "../../requirements.txt"])
            return True
        except subprocess.CalledProcessError:
            print("Error: Failed to install dependencies.")
            print("Please run: pip install -r requirements.txt")
            return False


def run_console_app():
    """Launch the console version"""
    print("Starting console app...")
    try:
        subprocess.run([sys.executable, "../../main.py"])
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
        subprocess.run([sys.executable, "../../src/web/app.py"])
    except KeyboardInterrupt:
        print("\nWeb server stopped by user.")
    except Exception as e:
        print(f"Error running web app: {e}")


def run_web_app_with_restart():
    """Launch the web version with auto-restart capability"""
    print("Starting web app with auto-restart...")
    print("Open http://localhost:5000 in your browser")
    print("Press Ctrl+C twice quickly to stop completely")
    print()
    
    consecutive_interrupts = 0
    restart_count = 0
    
    while True:
        try:
            print(f"Starting app... (restart #{restart_count})")
            process = subprocess.Popen([sys.executable, "../../src/web/app.py"], 
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.STDOUT,
                                     universal_newlines=True)
            
            # Reset interrupt counter on successful start
            consecutive_interrupts = 0
            
            # Monitor the process
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())
            
            # Process ended, check return code
            return_code = process.poll()
            if return_code == 0:
                print("App exited normally.")
                break
            else:
                print(f"App crashed with return code {return_code}")
                restart_count += 1
                print(f"Restarting in 3 seconds... (restart #{restart_count})")
                time.sleep(3)
                
        except KeyboardInterrupt:
            consecutive_interrupts += 1
            print(f"\nInterrupt received ({consecutive_interrupts}/2)")
            
            if consecutive_interrupts >= 2:
                print("Stopping app completely...")
                try:
                    process.terminate()
                    process.wait(timeout=5)
                except:
                    try:
                        process.kill()
                    except:
                        pass
                break
            else:
                print("Press Ctrl+C again quickly to stop completely, or wait to restart...")
                try:
                    process.terminate()
                    process.wait(timeout=5)
                except:
                    try:
                        process.kill()
                    except:
                        pass
                
                # Wait a bit, then restart
                time.sleep(2)
                restart_count += 1
                
        except Exception as e:
            print(f"Error running web app: {e}")
            restart_count += 1
            print(f"Restarting in 5 seconds... (restart #{restart_count})")
            time.sleep(5)


def main():
    """Main launcher function"""
    print("Fantasy Sports App Launcher")
    print("==========================")
    print(f"Python version: {sys.version}")
    print(f"Platform: {sys.platform}")
    
    # Platform-specific instructions
    if sys.platform.startswith('win'):
        print("Platform: Windows - Batch files available for quick start")
    elif sys.platform == 'darwin':
        print("Platform: macOS - Use Terminal to run this script")
    else:
        print("Platform: Linux - Use terminal to run this script")
    
    print()

    # Check Python version
    if not check_python_version():
        input("Press Enter to exit...")
        return

    # Check if we're in the right directory
    if not Path("../../main.py").exists() or not Path("../../src/web/app.py").exists():
        print("Error: Please run this script from the scripts/launchers directory")
        print("Make sure main.py and src/web/app.py exist in the project root")
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
        print("3) Run Web App with Auto-Restart (Recommended)")
        print("4) Exit")
        print()

        try:
            choice = input("Enter your choice (1-4): ").strip()
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

        if choice == "1":
            run_console_app()
        elif choice == "2":
            run_web_app()
        elif choice == "3":
            run_web_app_with_restart()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
