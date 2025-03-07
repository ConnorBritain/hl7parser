@echo off
echo Repairing PyQt6 installation...

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Show current Python and pip versions
python --version
pip --version

:: Upgrade pip first
pip install --upgrade pip

:: Clean uninstall PyQt6 components
pip uninstall -y PyQt6 PyQt6-Qt6 PyQt6-sip

:: Install specific binary wheels that are known to work with Python 3.13
pip install PyQt6==6.5.3 PyQt6-Qt6==6.5.3 PyQt6-sip==13.6.0

echo.
echo Repair complete! Run the application with:
echo run_windows.bat

pause