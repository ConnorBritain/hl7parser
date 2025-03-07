@echo off
echo Starting HL7 Parser...

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Set environment variables to help PyQt find its DLLs
set PYTHONPATH=%PYTHONPATH%;%~dp0..\..\venv\Lib\site-packages\PyQt6\Qt6\bin
set PATH=%PATH%;%~dp0..\..\venv\Lib\site-packages\PyQt6\Qt6\bin

:: Run the application - the window will auto-close when app exits
start /wait "" python src\main.py

:: Only show the pause if there was an error
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Application finished with error code %ERRORLEVEL% 
    echo Press any key to close this window...
    pause > nul
)