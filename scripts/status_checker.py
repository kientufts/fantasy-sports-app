#!/usr/bin/env python3
"""
Fantasy Sports App Status Checker and Manager

This script helps you check if the Fantasy Sports app is running
and provides options to start/stop it.
"""

import subprocess
import sys
import time
import requests
import os
import signal
from pathlib import Path

def check_port_in_use(port=5000):
    """Check if a port is in use"""
    try:
        if sys.platform.startswith('win'):
            result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
            return f':{port}' in result.stdout and 'LISTENING' in result.stdout
        else:
            result = subprocess.run(['lsof', '-i', f':{port}'], capture_output=True, text=True)
            return len(result.stdout.strip()) > 0
    except:
        return False

def check_app_responding(url='http://127.0.0.1:5000'):
    """Check if the app is responding to HTTP requests"""
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except:
        return False

def get_process_id(port=5000):
    """Get the process ID using the specified port"""
    try:
        if sys.platform.startswith('win'):
            result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
            lines = result.stdout.split('\n')
            for line in lines:
                if f':{port}' in line and 'LISTENING' in line:
                    parts = line.split()
                    if parts:
                        return int(parts[-1])
        else:
            result = subprocess.run(['lsof', '-ti', f':{port}'], capture_output=True, text=True)
            if result.stdout.strip():
                return int(result.stdout.strip().split('\n')[0])
    except:
        pass
    return None

def kill_process(pid):
    """Kill a process by PID"""
    try:
        if sys.platform.startswith('win'):
            subprocess.run(['taskkill', '/F', '/PID', str(pid)], check=True)
        else:
            os.kill(pid, signal.SIGTERM)
        return True
    except:
        return False

def start_app():
    """Start the Fantasy Sports app"""
    app_path = Path(__file__).parent / 'app.py'
    if not app_path.exists():
        print(f"❌ Error: app.py not found at {app_path}")
        return False
    
    try:
        if sys.platform.startswith('win'):
            subprocess.Popen([sys.executable, str(app_path)], 
                           creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            subprocess.Popen([sys.executable, str(app_path)])
        
        print("🚀 Starting Fantasy Sports app...")
        time.sleep(3)  # Give it time to start
        
        if check_app_responding():
            print("✅ App started successfully!")
            print("🌐 Access at: http://127.0.0.1:5000")
            return True
        else:
            print("⚠️  App may be starting... Please wait a moment and check again.")
            return False
    except Exception as e:
        print(f"❌ Error starting app: {e}")
        return False

def main():
    """Main status checker and manager"""
    print("🏆 Fantasy Sports App Status Checker")
    print("=" * 40)
    
    # Check current status
    port_in_use = check_port_in_use()
    app_responding = check_app_responding()
    pid = get_process_id()
    
    if port_in_use and app_responding:
        print("✅ Status: App is RUNNING and RESPONDING")
        print(f"🌐 URL: http://127.0.0.1:5000")
        if pid:
            print(f"🔧 Process ID: {pid}")
    elif port_in_use:
        print("⚠️  Status: Port 5000 is in use but app not responding")
        if pid:
            print(f"🔧 Process ID: {pid}")
    else:
        print("❌ Status: App is NOT RUNNING")
    
    print("\nOptions:")
    print("1. Check status again")
    print("2. Start the app")
    if pid:
        print("3. Stop the app")
    print("4. Open app in browser")
    print("5. Exit")
    
    try:
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            print("\n" + "="*40)
            main()
        elif choice == '2':
            if port_in_use:
                print("⚠️  App appears to already be running. Start anyway? (y/N): ", end="")
                confirm = input().strip().lower()
                if confirm != 'y':
                    return
            start_app()
        elif choice == '3' and pid:
            print(f"🛑 Stopping app (PID: {pid})...")
            if kill_process(pid):
                print("✅ App stopped successfully!")
            else:
                print("❌ Failed to stop app")
        elif choice == '4':
            import webbrowser
            url = "http://127.0.0.1:5000"
            print(f"🌐 Opening {url} in browser...")
            webbrowser.open(url)
        elif choice == '5':
            print("👋 Goodbye!")
        else:
            print("❌ Invalid choice")
    
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
