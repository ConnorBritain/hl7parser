#!/bin/bash
set -e

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

echo ""
echo "Installation complete! Run the application with:"
echo "./run_linux.sh"