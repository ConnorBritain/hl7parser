@echo off
echo Starting HL7 Parser (Tkinter Version)...

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Run the Tkinter version (no Qt dependency)
python src\main_tk.py

:: Pause to keep the window open if the app closes unexpectedly
echo.
echo Application finished with exit code %ERRORLEVEL% 
echo Press any key to close this window...
pause > nul