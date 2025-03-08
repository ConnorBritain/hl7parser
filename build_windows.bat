@echo off
echo HL7 Parser Windows Build Launcher
echo ===============================
echo.

cd /d "%~dp0"

:: Run the build process
cd packaging\windows\scripts
call build.bat

:: Return to original directory
cd /d "%~dp0"

echo.
echo Process complete. Press any key to close...
pause > nul