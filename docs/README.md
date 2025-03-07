# HL7 Parser Documentation

## Overview

HL7 Parser is a cross-platform application for parsing and viewing HL7 messages. It provides a graphical interface to examine the structure of HL7 messages, helping users understand and work with healthcare data formats.

## Privacy Features

This application was designed with privacy in mind:

1. No persistence of PHI (Protected Health Information)
   - All message processing is done in-memory
   - No temporary files are created
   - No logs containing message data are written

2. User warnings
   - Clear warnings are displayed when exporting or copying data
   - Users are reminded to delete exported files when no longer needed

## Architecture

The application is built with a modular architecture:

- `src/parser/` - Contains the HL7 parsing logic using the hl7apy library
- `src/gui/` - Contains the PyQt6-based user interface
- `src/utils/` - Contains utility functions
- `tests/` - Contains unit tests
- `examples/` - Contains sample HL7 messages for testing

## Usage Guide

### Parsing HL7 Messages

1. **Paste Text**: Paste HL7 message text directly into the input area and click "Parse Message"
2. **Load File**: Click "Load File" to load a .hl7 file from disk

### Viewing Message Structure

- The parsed message structure is displayed as a hierarchical tree
- Expand/collapse nodes to see different levels of the HL7 message
- Element names are shown in the left column, values in the right column

### Exporting Data

- **Copy to Clipboard**: Copies the parsed message structure to clipboard
- **Export to File**: Exports the parsed message to a text file

## Development

### Running Tests

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Run tests
pytest tests/
```

### Adding Features

To extend the parser with additional features:

1. Parser enhancements should be added to `src/parser/`
2. UI enhancements should be added to `src/gui/`
3. Add tests for new functionality in `tests/`