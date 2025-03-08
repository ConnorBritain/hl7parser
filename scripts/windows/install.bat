@echo off
pushd %~dp0..\..
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
pip install -r requirements.txt

echo.
echo Installation complete! Run the parser with:
echo run.py

pause
popd