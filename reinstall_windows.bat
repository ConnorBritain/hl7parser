@echo off
echo Reinstalling HL7 Parser from scratch...

:: Check if venv exists and remove it
if exist venv (
    echo Removing existing virtual environment...
    rmdir /s /q venv
)

:: Create and activate virtual environment
echo Creating new virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

:: Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

:: Install dependencies with specific versions known to work with Python 3.13
echo Installing dependencies...
pip install PyQt6==6.5.3 PyQt6-Qt6==6.5.3 PyQt6-sip==13.6.0
pip install hl7apy==1.3.4 pytest==7.3.1

echo.
echo Installation complete! Run the application with:
echo run_windows.bat

pause