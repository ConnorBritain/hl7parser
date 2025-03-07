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

:: Install binary-only packages to avoid compilation issues
pip install --only-binary=:all: PyQt6

echo.
echo Repair complete! Run the application with:
echo scripts\windows\run.bat

pause