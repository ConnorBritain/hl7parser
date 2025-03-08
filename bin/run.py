#!/usr/bin/env python3
import os
import sys
from pathlib import Path

def main():
    """Redirect to the new startup/run.py location."""
    # Get the project root directory (parent of bin/)
    project_root = Path(__file__).parent.parent.absolute()
    startup_script = project_root / "startup" / "run.py"
    
    if not startup_script.exists():
        print(f"Error: Cannot find {startup_script}")
        print("Please make sure the startup/run.py script exists.")
        sys.exit(1)
        
    # Make the script executable
    os.chmod(startup_script, 0o755)
    
    # Execute the startup script
    if os.name == 'nt':  # Windows
        # Use Python to execute the script
        os.system(f'python "{str(startup_script)}"')
    else:  # macOS/Linux
        # Use the script directly
        os.system(f'"{str(startup_script)}"')

if __name__ == "__main__":
    main()