# HL7 Parser

A cross-platform, privacy-focused HL7 message parser with GUI for viewing message structure.

## Features

- Parse HL7 messages into hierarchical structures
- View segments, fields, components, and subcomponents
- No data persistence - all processing happens in memory
- Cross-platform support (Windows, macOS, Linux)
- Simple export options with privacy warnings

## Installation

### Prerequisites

- Python 3.8+
- PyQt6

### Setup

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

```bash
# Run the application
python src/main.py
```

## License

MIT
