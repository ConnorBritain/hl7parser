# Windows Packaging Guide

This directory contains scripts to build a standalone Windows executable and installer for the HL7 Parser application.

## Prerequisites

1. **Python Environment**:
   - Python 3.6 or higher
   - Required packages: install with `pip install -r requirements.txt`

2. **Inno Setup**:
   - Download and install Inno Setup from: https://jrsoftware.org/isdl.php
   - Make sure the Inno Setup compiler (`iscc.exe`) is in your PATH

## Building the Application

### Step 1: Build the Executable

Run the following command from the project root directory:

```bash
python packaging/windows/build_exe.py
```

This will:
- Clean any previous build artifacts
- Create a PyInstaller spec file
- Run PyInstaller to build the executable
- Package all dependencies into a standalone application

The executable will be created in the `dist/HL7Parser` directory.

### Step 2: Create the Installer

After building the executable, compile the Inno Setup script to create the installer:

```bash
iscc packaging/windows/installer.iss
```

This will create an installer EXE file in the `dist/installer` directory.

## Customizing the Build

### Application Icon

- Replace the icon file at `resources/app_icon.ico` with your own icon
- Make sure the icon is in ICO format and has multiple sizes (16x16, 32x32, 48x48, 256x256)

### Version Information

- Update the version information in both:
  - `packaging/windows/build_exe.py` (APP_VERSION variable)
  - `packaging/windows/installer.iss` (#define MyAppVersion)

### Publisher Information

- Update the publisher information in `packaging/windows/installer.iss`

## Fixing Potential Issues

### Missing DLLs

If the application fails to start due to missing DLLs, you may need to modify the PyInstaller spec file to include additional dependencies.

### Antivirus False Positives

Some antivirus software may flag PyInstaller-created executables as suspicious. This is a known issue with PyInstaller. Options to address this:

1. Submit the application to antivirus vendors for whitelisting
2. Use a code signing certificate to sign the executable
3. Use an alternative packaging solution (e.g., cx_Freeze or py2exe)

### File Associations

The installer sets up file associations for .hl7 files. If you need to change these or add more associations, modify the [Registry] section in the installer.iss file.