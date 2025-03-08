#!/usr/bin/env python3
"""
HL7 Parser - Main entry point
This script serves as a single, convenient entry point for the HL7 Parser application.
It detects the platform and runs the appropriate platform-specific script.
"""
import os
import sys
import platform
import subprocess
from pathlib import Path

def main():
    """Run the appropriate script based on the operating system."""
    print("HL7 Parser")
    print("==========")
    
    # Get the base directory
    base_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    bin_dir = base_dir / "bin"
    
    # Check if run with arguments
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        
        if cmd == "install":
            print("Installing HL7 Parser...")
            run_script(bin_dir / "install.py")
            return
            
        elif cmd == "build":
            system = platform.system().lower()
            if system == 'windows':
                print("Building Windows installer...")
                windows_build_dir = base_dir / "packaging" / "windows" / "scripts"
                script_path = windows_build_dir / "build.bat"
                subprocess.call([script_path], cwd=str(windows_build_dir))
            else:
                print(f"Building is not yet supported on {platform.system()}")
            return
            
        elif cmd == "help" or cmd == "--help" or cmd == "-h":
            show_help()
            return
    
    # Default: run the application
    print("Starting HL7 Parser application...")
    run_script(bin_dir / "run.py")

def run_script(script_path):
    """Run a Python script."""
    if not script_path.exists():
        print(f"Error: Script not found at {script_path}")
        return False
        
    return subprocess.call([sys.executable, str(script_path)]) == 0

def show_help():
    """Show help information."""
    print("""
Usage: python hl7parser.py [command]

Commands:
  (no command) Run the HL7 Parser application
  install      Install dependencies
  build        Build installer package (Windows only)
  help         Show this help message

For more information, see docs/README.md and docs/BUILD.md
""")

if __name__ == "__main__":
    main()