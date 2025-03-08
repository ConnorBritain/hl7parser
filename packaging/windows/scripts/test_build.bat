@echo off
setlocal enabledelayedexpansion

:: This script tests the built executable to ensure it works correctly

echo HL7 Parser Test Script
echo =====================

:: Set up log file
set LOG_DIR=..\..\..\logs
if not exist !LOG_DIR! mkdir !LOG_DIR!
set TIMESTAMP=%date:~10,4%%date:~4,2%%date:~7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set TIMESTAMP=!TIMESTAMP: =0!
set LOG_FILE=!LOG_DIR!\test_%TIMESTAMP%.log

echo Test started at %date% %time% > !LOG_FILE!
echo. >> !LOG_FILE!

:: Check if the executable exists
echo Checking for executable...
echo Checking for executable... >> !LOG_FILE!
set EXE_PATH=..\..\..\dist\HL7Parser\HL7Parser.exe
if not exist !EXE_PATH! (
    echo ERROR: Executable not found at !EXE_PATH!
    echo ERROR: Executable not found at !EXE_PATH! >> !LOG_FILE!
    echo Please build the executable first with build_installer.bat
    echo Please build the executable first with build_installer.bat >> !LOG_FILE!
    exit /b 1
)

echo Executable found at !EXE_PATH!
echo Executable found at !EXE_PATH! >> !LOG_FILE!

:: Check for resources directory
echo Checking for resources...
echo Checking for resources... >> !LOG_FILE!
if not exist ..\..\..\dist\HL7Parser\resources (
    echo WARNING: Resources directory not found
    echo WARNING: Resources directory not found >> !LOG_FILE!
) else (
    echo Resources directory found
    echo Resources directory found >> !LOG_FILE!
    dir ..\..\..\dist\HL7Parser\resources /b >> !LOG_FILE!
)

:: Check for examples directory
echo Checking for example files...
echo Checking for example files... >> !LOG_FILE!
if not exist ..\..\..\dist\HL7Parser\examples (
    echo WARNING: Examples directory not found
    echo WARNING: Examples directory not found >> !LOG_FILE!
) else (
    echo Examples directory found
    echo Examples directory found >> !LOG_FILE!
    dir ..\..\..\dist\HL7Parser\examples /b >> !LOG_FILE!
)

:: Launch the executable in the background
echo Launching the executable to test...
echo Launching the executable to test... >> !LOG_FILE!
start "" "!EXE_PATH!"

:: Wait a moment for the application to start
timeout /t 3 > nul

:: Check if the process is running
echo Checking if process is running...
echo Checking if process is running... >> !LOG_FILE!
tasklist | find "HL7Parser.exe" > nul
if %ERRORLEVEL% neq 0 (
    echo ERROR: Application failed to start or crashed immediately
    echo ERROR: Application failed to start or crashed immediately >> !LOG_FILE!
    echo Check the application logs for details
    echo Check the application logs for details >> !LOG_FILE!
    exit /b 1
) else (
    echo Application is running successfully
    echo Application is running successfully >> !LOG_FILE!
)

:: Kill the process to clean up
echo Closing the application...
echo Closing the application... >> !LOG_FILE!
taskkill /F /IM HL7Parser.exe > nul 2>&1

echo Test completed successfully!
echo Test completed successfully! >> !LOG_FILE!
echo See log file for details: !LOG_FILE!

endlocal