#!/usr/bin/env python3
import os
import sys
import shutil
import subprocess
import logging
from pathlib import Path
from datetime import datetime

# Setup logging
log_dir = Path(__file__).parent.parent.parent / "logs"
log_dir.mkdir(exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_path = log_dir / f"pyinstaller_{timestamp}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_path),
        logging.StreamHandler()
    ]
)

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent.absolute()
RESOURCES_DIR = PROJECT_ROOT / "resources"
DIST_DIR = PROJECT_ROOT / "dist"
BUILD_DIR = PROJECT_ROOT / "build"

# Application information
APP_NAME = "HL7Parser"
APP_VERSION = "1.0.0"
APP_ICON = str(RESOURCES_DIR / "app_icon.ico")

def clean_previous_builds():
    """Remove previous build artifacts"""
    logging.info("Cleaning previous build artifacts...")
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    
    # Remove any spec files
    for spec_file in PROJECT_ROOT.glob("*.spec"):
        spec_file.unlink()
    
    logging.info("Previous build artifacts cleaned.")

def check_dependencies():
    """Check for required dependencies"""
    logging.info("Checking for required dependencies...")
    try:
        import PyQt6
        logging.info(f"PyQt6 version: {PyQt6.__version__}")
    except ImportError:
        logging.error("PyQt6 not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "PyQt6"])
        
    try:
        import hl7apy
        logging.info(f"hl7apy version: {hl7apy.__version__}")
    except ImportError:
        logging.error("hl7apy not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "hl7apy==1.3.4"])

def create_pyinstaller_spec():
    """Create a PyInstaller spec file"""
    logging.info("Creating PyInstaller spec file...")
    
    # Use app.py as entry point (standalone application)
    app_py_path = PROJECT_ROOT / "app.py"
    if not app_py_path.exists():
        logging.error(f"app.py not found at {app_py_path}. Cannot continue.")
        sys.exit(1)
    
    logging.info(f"Using app.py as entry point: {app_py_path}")
    
    # Create the spec contents
    spec_content = f"""# -*- mode: python ; coding: utf-8 -*-

import sys
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

# Add data files from hl7apy
datas = collect_data_files('hl7apy')

# Add example files
datas += [
    ('{str(PROJECT_ROOT / "examples")}', 'examples'),
]

# Add our application resources
datas += [
    ('{str(RESOURCES_DIR)}', 'resources'),
]

a = Analysis(
    ['{str(app_py_path)}'],  # Use app.py as the entry point
    pathex=['{str(PROJECT_ROOT)}'],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'PyQt6.sip',
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{APP_NAME}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to False to hide the console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='{APP_ICON}',
    version='{str(PROJECT_ROOT / "packaging" / "windows" / "config" / "windows_version_info.txt")}',
)
"""
    
    # Write the spec file
    spec_path = PROJECT_ROOT / f"{APP_NAME}.spec"
    with open(spec_path, 'w') as f:
        f.write(spec_content)
        
    logging.info(f"PyInstaller spec file created at {spec_path}")
    return spec_path

def run_pyinstaller(spec_path):
    """Run PyInstaller to build the executable"""
    logging.info("Running PyInstaller...")
    
    # Run PyInstaller with detailed output
    try:
        # First, ensure PyInstaller is up to date
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "pyinstaller"],
            check=True,
            capture_output=True,
            text=True
        )
        
        # Run PyInstaller
        result = subprocess.run(
            ["pyinstaller", "--clean", "--noconfirm", "--log-level", "DEBUG", str(spec_path)],
            cwd=str(PROJECT_ROOT),
            check=True,
            capture_output=True,
            text=True
        )
        
        # Log the output
        logging.info("PyInstaller stdout:")
        for line in result.stdout.splitlines():
            logging.info(line)
        
        logging.info("PyInstaller stderr:")
        for line in result.stderr.splitlines():
            logging.warning(line)
        
        logging.info("PyInstaller completed successfully!")
    except subprocess.CalledProcessError as e:
        logging.error(f"PyInstaller failed with return code {e.returncode}")
        logging.error("PyInstaller stdout:")
        for line in e.stdout.splitlines():
            logging.error(line)
        
        logging.error("PyInstaller stderr:")
        for line in e.stderr.splitlines():
            logging.error(line)
        
        sys.exit(1)

def verify_build():
    """Verify the build was successful"""
    logging.info("Verifying build...")
    
    # Check if executable exists
    exe_path = DIST_DIR / APP_NAME / f"{APP_NAME}.exe"
    if not exe_path.exists():
        logging.error(f"Executable not found at {exe_path}")
        sys.exit(1)
    
    logging.info(f"Executable found at {exe_path}")
    
    # Check if resources are included
    resources_dir = DIST_DIR / APP_NAME / "resources"
    if not resources_dir.exists() or not list(resources_dir.glob("*")):
        logging.warning(f"Resources directory is empty or missing: {resources_dir}")
    else:
        logging.info(f"Resources directory found with {len(list(resources_dir.glob('*')))} files")
    
    # Check examples
    examples_dir = DIST_DIR / APP_NAME / "examples"
    if not examples_dir.exists() or not list(examples_dir.glob("*")):
        logging.warning(f"Examples directory is empty or missing: {examples_dir}")
    else:
        logging.info(f"Examples directory found with {len(list(examples_dir.glob('*')))} files")
    
    logging.info("Build verification completed")

def main():
    """Main build process"""
    logging.info(f"Building {APP_NAME} v{APP_VERSION}...")
    logging.info(f"Project root: {PROJECT_ROOT}")
    
    # Ensure resources directory exists
    if not RESOURCES_DIR.exists():
        RESOURCES_DIR.mkdir(parents=True)
        logging.info(f"Created resources directory: {RESOURCES_DIR}")
    
    # Check dependencies
    check_dependencies()
    
    # Clean previous builds
    clean_previous_builds()
    
    # Create the spec file
    spec_path = create_pyinstaller_spec()
    
    # Run PyInstaller
    run_pyinstaller(spec_path)
    
    # Verify the build
    verify_build()
    
    logging.info(f"Build completed! Executable is in {DIST_DIR / APP_NAME}")
    logging.info("Now you can run the Inno Setup script to create the installer.")
    logging.info(f"Build log saved to: {log_path}")

if __name__ == "__main__":
    main()