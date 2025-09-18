#!/bin/bash
# Cross-platform startup script for Fantasy Sports App
# Works on macOS and Linux

echo "Fantasy Sports App - Quick Start"
echo "================================"

# Check if Python 3 is available
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null && python -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" 2>/dev/null; then
    PYTHON_CMD=python
else
    echo "Error: Python 3.8+ is required but not found"
    echo "Please install Python 3.8 or later"
    read -p "Press Enter to exit..."
    exit 1
fi

echo "Found Python: $PYTHON_CMD"

# Check if we're in the right directory
if [ ! -f "launcher.py" ]; then
    echo "Error: Please run this script from the fantasy app directory"
    echo "Make sure launcher.py is in the current directory"
    read -p "Press Enter to exit..."
    exit 1
fi

# Make sure we have execute permissions
chmod +x "$0"

echo "Starting launcher..."
$PYTHON_CMD launcher.py
