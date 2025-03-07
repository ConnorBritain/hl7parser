@echo on
echo Starting HL7 Parser in DEBUG mode...

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Run the application directly in the console
python src\main.py

:: Always pause at the end
echo.
echo Application exited with code %ERRORLEVEL%
echo Press any key to close this window...
pause > nul