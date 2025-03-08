@echo off
setlocal enabledelayedexpansion

echo HL7 Parser Windows Build Script
echo ==============================

:: Change to the script's directory to ensure relative paths work
cd /d "%~dp0"

:: Setup logging
set TIMESTAMP=%date:~10,4%%date:~4,2%%date:~7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set TIMESTAMP=!TIMESTAMP: =0!
set LOG_DIR=..\..\..\logs
set LOG_FILE=!LOG_DIR!\master_build_%TIMESTAMP%.log

if not exist !LOG_DIR! mkdir !LOG_DIR!

echo Build process started at %date% %time% > !LOG_FILE!
echo. >> !LOG_FILE!

:: Step 1: Build the installer
echo Step 1: Building installer...
echo Step 1: Building installer... >> !LOG_FILE!
call build_installer.bat
if %ERRORLEVEL% neq 0 (
    echo ERROR: Installer build failed
    echo ERROR: Installer build failed >> !LOG_FILE!
    exit /b 1
)

:: Step 2: Test the executable
echo.
echo. >> !LOG_FILE!
echo Step 2: Testing executable...
echo Step 2: Testing executable... >> !LOG_FILE!
call test_build.bat
if %ERRORLEVEL% neq 0 (
    echo ERROR: Executable test failed
    echo ERROR: Executable test failed >> !LOG_FILE!
    exit /b 1
)

:: Step 3: Verify the installer exists
echo.
echo. >> !LOG_FILE!
echo Step 3: Verifying installer...
echo Step 3: Verifying installer... >> !LOG_FILE!
if not exist ..\..\..\dist\installer\HL7Parser_Setup.exe (
    echo ERROR: Installer not found at expected location
    echo ERROR: Installer not found at expected location >> !LOG_FILE!
    exit /b 1
)

:: Build completed successfully
echo.
echo. >> !LOG_FILE!
echo Build process completed successfully!
echo Build process completed successfully! >> !LOG_FILE!
echo Installer: ..\..\..\dist\installer\HL7Parser_Setup.exe
echo Installer: ..\..\..\dist\installer\HL7Parser_Setup.exe >> !LOG_FILE!
echo Master log: !LOG_FILE!

echo.
echo Build process completed successfully!
echo Installer: ..\..\..\dist\installer\HL7Parser_Setup.exe
echo Master log: !LOG_FILE!

:: Open the folder containing the installer
explorer ..\..\..\dist\installer\

endlocal