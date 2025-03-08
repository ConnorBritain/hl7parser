# HL7 Parser - Build and Installation Guide

This document explains how to build, package, and install the HL7 Parser application.

## Prerequisites

### For Development and Running from Source
- Python 3.8 or newer
- Required Python packages: PyQt6, hl7apy, pytest
- Git (for version control)

### For Building Windows Installer
- Python 3.8 or newer
- PyInstaller (installed automatically if missing)
- Inno Setup 6.0 or newer (https://jrsoftware.org/isdl.php)
- Windows OS (or Wine on Linux/macOS for Inno Setup)

## Running the Application from Source

1. Clone the repository:
   ```
   git clone <repository-url>
   cd hl7parser
   ```

2. Install dependencies:
   ```
   python install.py
   ```

3. Run the application:
   ```
   python run.py
   ```

The `install.py` script will set up a virtual environment and install all required dependencies. The `run.py` script will launch the appropriate platform-specific script to run the application.

## Building the Windows Installer

The packaging system has been designed to generate a standalone Windows executable and installer that bundles all dependencies.

### Option 1: One-step Build Process (Recommended)

Run the master build script:

```
cd packaging/windows
build.bat
```

This script will:
1. Build the executable with PyInstaller
2. Create the installer with Inno Setup
3. Test the executable to verify it works
4. Open the folder containing the installer when done

### Option 2: Step-by-step Build Process

If you need more control over the build process:

1. Build the executable:
   ```
   cd packaging/windows
   python build_exe.py
   ```

2. Create the installer:
   ```
   iscc installer.iss
   ```

3. Test the build:
   ```
   test_build.bat
   ```

### Key Changes in the Build Process

The current build process has been optimized to:

1. **Use the standalone app.py file** - This single-file version of the application avoids module import issues that can occur with PyInstaller packaging.

2. **Enhanced logging and diagnostics** - All build scripts now create detailed logs to help diagnose issues.

3. **Testing automation** - The test_build.bat script verifies that the built executable runs correctly.

4. **Better error handling** - The build scripts check for missing dependencies and properly report errors.

## Customizing the Build

- Version information: Update the version number in:
  - `packaging/windows/build_exe.py` (APP_VERSION variable)
  - `packaging/windows/installer.iss` (#define MyAppVersion)
  - `packaging/windows/version_info.py` (VERSION_INFO dictionary)

- Application icon: Replace `resources/app_icon.ico` with your own ICO file

## Troubleshooting the Build

All build scripts create detailed logs in the `logs/` directory to help diagnose issues:

- `logs/master_build_*.log`: Main build log
- `logs/build_*.log`: Installer build log
- `logs/pyinstaller_*.log`: PyInstaller detailed log
- `logs/test_*.log`: Build test log

Common issues and solutions:

1. **Missing dependencies**: 
   - Ensure all required Python packages are installed with `pip install -r requirements.txt`
   - The build scripts should automatically install missing dependencies

2. **PyInstaller issues**:
   - Check the PyInstaller log for errors
   - Try running PyInstaller with `--debug` flag for more information
   - Check if the standalone app.py is being found and used

3. **Inno Setup issues**:
   - Ensure Inno Setup is installed and in your PATH
   - Check if the executable was properly created in `dist/HL7Parser/`

4. **Application crashes after build**:
   - Check the application logs in `dist/HL7Parser/logs/`
   - Test with console enabled in PyInstaller to see error messages
   - The standalone app.py includes additional error handling and logging

## Deployment

The final installer will be in the `dist/installer/` directory named `HL7Parser_Setup.exe`. This installer can be distributed to end users.

When installed, the application will:
- Create a desktop shortcut (if selected during installation)
- Create start menu entries
- Associate with .hl7 files (double-clicking a .hl7 file will open it in the application)
- Provide an uninstaller through Control Panel