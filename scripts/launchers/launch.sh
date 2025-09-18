#!/bin/bash
# Launch script for macOS/Linux

echo "Fantasy Sports App Launcher"
echo "=========================="

# Check if Python 3 is available
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null && python --version 2>&1 | grep -q "Python 3"; then
    PYTHON_CMD="python"
else
    echo "Error: Python 3 is not installed or not found in PATH"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

echo "Using Python command: $PYTHON_CMD"

# Check if requirements are installed
if ! $PYTHON_CMD -c "import flask" 2>/dev/null; then
    echo "Installing dependencies..."
    $PYTHON_CMD -m pip install -r requirements.txt
fi

echo ""
echo "Choose an option:"
echo "1) Run Console App"
echo "2) Run Web App"
echo "3) Exit"
echo ""

read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo "Starting console app..."
        $PYTHON_CMD main.py
        ;;
    2)
        echo "Starting web app..."
        echo "Open http://localhost:5000 in your browser"
        $PYTHON_CMD app.py
        ;;
    3)
        echo "Goodbye!"
        exit 0
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac
