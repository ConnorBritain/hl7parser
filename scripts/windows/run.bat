@echo off
echo Starting HL7 Parser...

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Set environment variables to help PyQt find its DLLs
set PYTHONPATH=%PYTHONPATH%;%~dp0..\..\venv\Lib\site-packages\PyQt6\Qt6\bin
set PATH=%PATH%;%~dp0..\..\venv\Lib\site-packages\PyQt6\Qt6\bin

:: Run the application
python src\main.py

:: Pause to keep the window open if the app closes unexpectedly
echo.
echo Application finished with exit code %ERRORLEVEL% 
echo Press any key to close this window...
pause > nul