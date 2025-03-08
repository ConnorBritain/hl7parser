# HL7 Parser

A cross-platform, privacy-focused HL7 message parser with GUI for viewing message structure.

## Features

- Parse HL7 messages into hierarchical structures
- View segments, fields, components, and subcomponents
- No data persistence - all processing happens in memory
- Cross-platform support (Windows, macOS, Linux)
- Simple export options with privacy warnings

## Installation

### Windows Installer

Download the latest installer from the releases page and run it to install HL7 Parser with all required dependencies.

### Quick Start (All Platforms)

```bash
# Clone repository
git clone https://github.com/ConnorBritain/hl7parser.git
cd hl7parser

# Install dependencies and run
python hl7parser.py install
python hl7parser.py
```

### Platform-Specific Scripts

The application includes platform-specific scripts for installation and running:

#### Windows
```
bin\install.py  # Install dependencies
bin\run.py      # Run the application
```

#### macOS/Linux
```
chmod +x bin/install.py bin/run.py
./bin/install.py  # Install dependencies
./bin/run.py      # Run the application
```

## Project Structure

- `/app.py` - Standalone application file (single-file version)
- `/bin/` - Platform-specific install/run scripts
- `/docs/` - Documentation
- `/examples/` - Sample HL7 messages
- `/packaging/` - Packaging scripts for different platforms
  - `/windows/` - Windows packaging
    - `/config/` - Configuration files
    - `/scripts/` - Build scripts
- `/resources/` - Application resources (icons, etc.)
- `/src/` - Source code
  - `/gui/` - UI components
  - `/parser/` - HL7 parsing logic
- `/tests/` - Test files

## Building the Windows Installer

To create a standalone Windows executable with installer:

```bash
# Option 1: Using the unified script
python hl7parser.py build

# Option 2: Using the batch file directly
cd packaging/windows/scripts
build.bat
```

The installer will be created in the `dist/installer` directory. For detailed build instructions, see [docs/BUILD.md](docs/BUILD.md).

## Examples

Sample HL7 messages are provided in the `examples` directory.

## Privacy Warning

This tool may be used to process messages containing Protected Health Information (PHI). 
Always handle such data in compliance with HIPAA regulations and your organization's policies.
HL7 Parser does not transmit any data over networks.

## License

MIT
