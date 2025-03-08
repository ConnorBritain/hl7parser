#!/usr/bin/env python3
import os
import platform
import subprocess
import sys
from pathlib import Path

def main():
    """Run the appropriate installation script based on the operating system."""
    system = platform.system().lower()
    
    # Get the project root directory (parent of bin/)
    project_root = Path(__file__).parent.parent.absolute()
    scripts_dir = project_root / "scripts"
    
    if system == 'windows':
        script_path = scripts_dir / "windows" / "install.bat"
        subprocess.call([str(script_path)])
    elif system == 'darwin':  # macOS
        script_path = scripts_dir / "macos" / "install.sh"
        # Make the script executable
        os.chmod(script_path, 0o755)
        subprocess.call([str(script_path)])
    elif system == 'linux':
        script_path = scripts_dir / "linux" / "install.sh"
        # Make the script executable
        os.chmod(script_path, 0o755)
        subprocess.call([str(script_path)])
    else:
        print(f"Unsupported operating system: {platform.system()}")
        print("Please run the installation script manually from the scripts directory.")
        sys.exit(1)

if __name__ == "__main__":
    main()