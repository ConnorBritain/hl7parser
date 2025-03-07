#!/usr/bin/env python3
import os
import platform
import subprocess
import sys

def main():
    """Run the appropriate script based on the operating system."""
    system = platform.system().lower()
    
    # Get the base directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    if system == 'windows':
        script_path = os.path.join(base_dir, 'scripts', 'windows', 'run.bat')
        subprocess.call([script_path])
    elif system == 'darwin':  # macOS
        script_path = os.path.join(base_dir, 'scripts', 'macos', 'run.sh')
        # Make the script executable
        os.chmod(script_path, 0o755)
        subprocess.call([script_path])
    elif system == 'linux':
        script_path = os.path.join(base_dir, 'scripts', 'linux', 'run.sh')
        # Make the script executable
        os.chmod(script_path, 0o755)
        subprocess.call([script_path])
    else:
        print(f"Unsupported operating system: {platform.system()}")
        print("Please run the script manually from the scripts directory.")
        sys.exit(1)

if __name__ == "__main__":
    main()