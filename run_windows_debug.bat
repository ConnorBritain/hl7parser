@echo on
echo Starting HL7 Parser in DEBUG mode...

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Set environment variables to help PyQt find its DLLs
set PYTHONPATH=%PYTHONPATH%;%~dp0venv\Lib\site-packages\PyQt6\Qt6\bin
set PATH=%PATH%;%~dp0venv\Lib\site-packages\PyQt6\Qt6\bin

:: Print environment path for debugging
echo PATH = %PATH%
echo PYTHONPATH = %PYTHONPATH%

:: Run the application directly in the console with verbose output
python -v src\main.py

:: Always pause at the end
echo.
echo Application exited with code %ERRORLEVEL%
echo Press any key to close this window...
pause > nul