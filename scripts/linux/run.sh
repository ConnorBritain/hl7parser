#!/bin/bash
cd "$(dirname "$0")/../.." || exit 1
echo "Starting HL7 Parser..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Please run install.py first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Run the application
python src/main.py