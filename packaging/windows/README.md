# Windows Packaging Guide

This directory contains scripts and configuration files to build a standalone Windows executable and installer for the HL7 Parser application.

## Directory Organization

- **`/config/`**: Configuration files
  - `installer.iss`: Inno Setup script for creating the installer
  - `version_info.py`: Generates Windows version information
  - `windows_version_info.txt`: Generated version resource for Windows executable

- **`/scripts/`**: Build scripts
  - `build.bat`: Master build script that orchestrates the entire process
  - `build_installer.bat`: Script for building the installer with Inno Setup
  - `build_exe.py`: Python script for building the executable with PyInstaller
  - `test_build.bat`: Script for testing the built executable

## Prerequisites

1. **Python Environment**:
   - Python 3.8 or higher
   - Required packages: install with `pip install -r requirements.txt`

2. **Inno Setup**:
   - Download and install Inno Setup from: https://jrsoftware.org/isdl.php
   - Make sure the Inno Setup compiler (`iscc.exe`) is in your PATH

## Building the Application

### One-Step Build Process (Recommended)

Run the master build script from the project root directory:

```bash
cd packaging/windows/scripts
build.bat
```

This will:
1. Build the executable with PyInstaller using app.py
2. Create the installer with Inno Setup
3. Test the executable to ensure it works
4. Open the folder containing the installer when complete

### Step-by-Step Build Process

If you need more control over the build process:

1. Build the executable:
   ```
   cd packaging/windows/scripts
   python build_exe.py
   ```

2. Create the installer:
   ```
   build_installer.bat
   ```

3. Test the build:
   ```
   test_build.bat
   ```

## Build Output and Logs

- Executable: `dist/HL7Parser/HL7Parser.exe`
- Installer: `dist/installer/HL7Parser_Setup.exe`
- Logs: All build logs are saved in the `logs/` directory

## Customizing the Build

### Application Icon

- Replace the icon file at `resources/app_icon.ico` with your own icon
- Make sure the icon is in ICO format and has multiple sizes (16x16, 32x32, 48x48, 256x256)

### Version Information

- Update the version information in:
  - `config/version_info.py` (VERSION_INFO dictionary)
  - `config/installer.iss` (#define MyAppVersion)
  - `scripts/build_exe.py` (APP_VERSION variable)

### Publisher Information

- Update the publisher information in `config/installer.iss`

## Troubleshooting

All build scripts create detailed logs to help diagnose issues:

- `logs/master_build_*.log`: Main build log
- `logs/build_*.log`: Installer build log
- `logs/pyinstaller_*.log`: PyInstaller detailed log
- `logs/test_*.log`: Build test log

The key improvements in the current build system:

1. **Enhanced logging**: Comprehensive logging at all stages of the build
2. **Standalone application**: Uses app.py as the single-file entry point
3. **Automated testing**: Verifies the built executable works correctly
4. **Improved error handling**: Better error detection and reporting