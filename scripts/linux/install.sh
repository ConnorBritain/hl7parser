#!/bin/bash
cd "$(dirname "$0")/../.." || exit 1
echo "Installing HL7 Parser..."

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies from requirements.txt
echo "Installing dependencies..."
pip install -r requirements.txt

echo -e "\nInstallation complete! Run the parser with:"
echo "./run.py"