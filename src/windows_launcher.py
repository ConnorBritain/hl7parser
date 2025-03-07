#!/usr/bin/env python3
"""
Windows-specific launcher for HL7 Parser with no console window.
This file is used by PyInstaller to create a Windows executable
that doesn't show a command prompt window.
"""
import sys
import os
import traceback
from pathlib import Path

# Redirect stdout/stderr to files when running as an exe
# to avoid creating console windows but still capture errors
if getattr(sys, 'frozen', False):
    # Running as compiled exe
    app_dir = Path(os.path.dirname(sys.executable))
    log_dir = app_dir / "logs"
    
    # Create logs directory if it doesn't exist
    log_dir.mkdir(exist_ok=True)
    
    # Redirect stdout and stderr to log files
    sys.stdout = open(log_dir / "stdout.log", "w")
    sys.stderr = open(log_dir / "stderr.log", "w")

try:
    from PyQt6.QtWidgets import QApplication, QMessageBox
    from gui.main_window import MainWindow

    def main():
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())

    if __name__ == "__main__":
        main()
        
except Exception as e:
    # If we're running as frozen app and error occurs,
    # show error message box instead of crashing silently
    if getattr(sys, 'frozen', False):
        error_message = f"Error starting HL7 Parser:\n\n{str(e)}\n\n{traceback.format_exc()}"
        try:
            # If we can import Qt, use it for error dialog
            from PyQt6.QtWidgets import QApplication, QMessageBox
            app = QApplication(sys.argv)
            QMessageBox.critical(None, "HL7 Parser Error", error_message)
        except:
            # If Qt failed to import, we can't show GUI error dialog,
            # so at least write to the error log
            if hasattr(sys, 'stderr'):
                sys.stderr.write(error_message)
        sys.exit(1)
    else:
        # If running from source, just raise the exception normally
        raise