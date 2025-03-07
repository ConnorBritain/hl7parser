@echo off
echo Starting HL7 Parser...

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Run the application
python src\main.py