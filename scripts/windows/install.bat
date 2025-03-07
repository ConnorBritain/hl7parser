@echo off
echo Installing HL7 Parser...

:: Create and activate virtual environment
python -m venv venv
call venv\Scripts\activate.bat

:: Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

:: Install dependencies with binary-only packages to avoid compilation issues
echo Installing dependencies...
pip install --only-binary=:all: PyQt6
pip install hl7apy==1.3.4 pytest==7.3.1

echo.
echo Installation complete! Run the parser with:
echo scripts\windows\run.bat

pause