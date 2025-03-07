@echo off
echo Installing HL7 Parser...

:: Create and activate virtual environment
python -m venv venv
call venv\Scripts\activate.bat

:: Install dependencies
pip install -r requirements.txt

echo.
echo Installation complete! Run the application with:
echo run_windows.bat