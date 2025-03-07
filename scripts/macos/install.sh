#!/bin/bash
echo "Installing HL7 Parser..."

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install PyQt6==6.5.3 hl7apy==1.3.4 pytest==7.3.1

echo -e "\nInstallation complete! Run the parser with:"
echo "scripts/macos/run.sh"