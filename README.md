# HL7 Parser

A cross-platform, privacy-focused HL7 message parser with GUI for viewing message structure.

## Features

- Parse HL7 messages into hierarchical structures
- View segments, fields, components, and subcomponents
- No data persistence - all processing happens in memory
- Cross-platform support (Windows, macOS, Linux)
- Simple export options with privacy warnings

## Installation

### Windows

1. Double-click `scripts/windows/install.bat`
2. After installation completes, run `scripts/windows/run.bat` to start the application

If you encounter any issues, try running `scripts/windows/repair.bat` to fix the installation.

### macOS

1. Open Terminal
2. Navigate to the HL7 Parser directory
3. Run: `chmod +x scripts/macos/install.sh scripts/macos/run.sh`
4. Run: `./scripts/macos/install.sh`
5. After installation completes, run: `./scripts/macos/run.sh`

### Linux

1. Open Terminal
2. Navigate to the HL7 Parser directory
3. Run: `chmod +x scripts/linux/install.sh scripts/linux/run.sh`
4. Run: `./scripts/linux/install.sh`
5. After installation completes, run: `./scripts/linux/run.sh`

### Manual Setup

```bash
# Clone repository
git clone https://github.com/yourusername/hl7parser.git
cd hl7parser

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

If you installed using the scripts:
- Windows: Double-click `scripts/windows/run.bat`
- macOS: Run `./scripts/macos/run.sh` in Terminal
- Linux: Run `./scripts/linux/run.sh` in Terminal

If you performed a manual setup:
```bash
# Activate virtual environment if needed
# Run the application
python src/main.py
```

## Examples

Sample HL7 messages are provided in the `examples` directory.

## Privacy Warning

This tool may be used to process messages containing Protected Health Information (PHI). 
Always handle such data in compliance with HIPAA regulations and your organization's policies.
HL7 Parser does not transmit any data over networks.

## License

MIT
