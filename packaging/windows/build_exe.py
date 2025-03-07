#!/usr/bin/env python3
import os
import sys
import shutil
import subprocess
from pathlib import Path

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
    print("Cleaning previous build artifacts...")
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    
    # Remove any spec files
    for spec_file in PROJECT_ROOT.glob("*.spec"):
        spec_file.unlink()
    
    print("Previous build artifacts cleaned.")

def create_pyinstaller_spec():
    """Create a PyInstaller spec file"""
    print("Creating PyInstaller spec file...")
    
    # Create the spec contents
    spec_content = f"""# -*- mode: python ; coding: utf-8 -*-

import sys
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

# Add data files from hl7apy
datas = collect_data_files('hl7apy')

# Add our application resources
datas += [
    ('{str(RESOURCES_DIR)}', 'resources'),
]

a = Analysis(
    ['{str(PROJECT_ROOT / "src" / "windows_launcher.py")}'],
    pathex=['{str(PROJECT_ROOT)}'],
    binaries=[],
    datas=datas,
    hiddenimports=['PyQt6.sip'],
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
    version='{str(PROJECT_ROOT / "packaging" / "windows" / "windows_version_info.txt")}',
)
"""
    
    # Write the spec file
    spec_path = PROJECT_ROOT / f"{APP_NAME}.spec"
    with open(spec_path, 'w') as f:
        f.write(spec_content)
        
    print(f"PyInstaller spec file created at {spec_path}")
    return spec_path

def run_pyinstaller(spec_path):
    """Run PyInstaller to build the executable"""
    print("Running PyInstaller...")
    
    # Run PyInstaller
    result = subprocess.run(
        ["pyinstaller", "--clean", "--noconfirm", str(spec_path)],
        cwd=str(PROJECT_ROOT),
        check=True,
    )
    
    if result.returncode == 0:
        print("PyInstaller completed successfully!")
    else:
        print("PyInstaller failed!")
        sys.exit(1)

def main():
    """Main build process"""
    print(f"Building {APP_NAME} v{APP_VERSION}...")
    
    # Ensure resources directory exists
    if not RESOURCES_DIR.exists():
        RESOURCES_DIR.mkdir(parents=True)
    
    # Clean previous builds
    clean_previous_builds()
    
    # Create the spec file
    spec_path = create_pyinstaller_spec()
    
    # Run PyInstaller
    run_pyinstaller(spec_path)
    
    print(f"Build completed! Executable is in {DIST_DIR}")
    print("Now you can run the Inno Setup script to create the installer.")

if __name__ == "__main__":
    main()