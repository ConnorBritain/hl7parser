@echo off
echo Starting HL7 Parser...

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Run the application with verbose error output
python -v src\main.py

:: Pause to keep the window open regardless of exit code
echo.
echo Application finished with exit code %ERRORLEVEL% 
echo Press any key to close this window...
pause > nul