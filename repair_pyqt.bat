@echo off
echo Repairing PyQt6 installation...

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Show current Python and pip versions
python --version
pip --version

:: Uninstall and reinstall PyQt6
pip uninstall -y PyQt6 PyQt6-Qt6 PyQt6-sip
pip install PyQt6==6.5.0

echo.
echo Repair complete! Run the application with:
echo run_windows.bat

pause