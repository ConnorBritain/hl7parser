@echo off
setlocal enabledelayedexpansion

:: Setup logging
set TIMESTAMP=%date:~10,4%%date:~4,2%%date:~7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set TIMESTAMP=!TIMESTAMP: =0!
set LOG_DIR=..\..\..\logs
set LOG_FILE=!LOG_DIR!\build_%TIMESTAMP%.log

:: Create logs directory
if not exist !LOG_DIR! mkdir !LOG_DIR!

echo HL7 Parser Windows Installer Build Script > !LOG_FILE!
echo ========================================= >> !LOG_FILE!
echo Build started at %date% %time% >> !LOG_FILE!
echo. >> !LOG_FILE!

echo HL7 Parser Windows Installer Build Script
echo =========================================

echo Logging to: !LOG_FILE!
echo.

:: Log system info
echo System Information: >> !LOG_FILE!
systeminfo | findstr /B /C:"OS Name" /C:"OS Version" >> !LOG_FILE!
echo. >> !LOG_FILE!

:: Check if Python is available
echo Checking for Python...
echo Checking for Python... >> !LOG_FILE!
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ERROR: Python not found in PATH
    echo ERROR: Python not found in PATH >> !LOG_FILE!
    echo Please ensure Python is installed and added to your PATH
    echo Please ensure Python is installed and added to your PATH >> !LOG_FILE!
    exit /b 1
)

:: Log Python version
echo Python version: >> !LOG_FILE!
python --version >> !LOG_FILE!
echo. >> !LOG_FILE!

:: Check if PyInstaller is available
echo Checking for PyInstaller...
echo Checking for PyInstaller... >> !LOG_FILE!
python -c "import PyInstaller" >nul 2>>!LOG_FILE!
if %ERRORLEVEL% neq 0 (
    echo ERROR: PyInstaller not found
    echo ERROR: PyInstaller not found >> !LOG_FILE!
    echo Installing PyInstaller...
    echo Installing PyInstaller... >> !LOG_FILE!
    python -m pip install pyinstaller >>!LOG_FILE! 2>&1
    if %ERRORLEVEL% neq 0 (
        echo Failed to install PyInstaller
        echo Failed to install PyInstaller >> !LOG_FILE!
        exit /b 1
    )
)

:: Log PyInstaller version
echo PyInstaller version: >> !LOG_FILE!
python -c "import PyInstaller; print(PyInstaller.__version__)" >> !LOG_FILE!
echo. >> !LOG_FILE!

:: Check for app dependencies
echo Checking for required libraries...
echo Checking for required libraries... >> !LOG_FILE!
python -c "import PyQt6, hl7apy" >>!LOG_FILE! 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: Required Python libraries not found
    echo ERROR: Required Python libraries not found >> !LOG_FILE!
    echo Installing required dependencies...
    echo Installing required dependencies... >> !LOG_FILE!
    python -m pip install -r ..\..\..\requirements.txt >>!LOG_FILE! 2>&1
    if %ERRORLEVEL% neq 0 (
        echo Failed to install dependencies
        echo Failed to install dependencies >> !LOG_FILE!
        exit /b 1
    )
)

:: Check if Inno Setup is available
echo Checking for Inno Setup...
echo Checking for Inno Setup... >> !LOG_FILE!
where iscc >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ERROR: Inno Setup compiler (iscc) not found in PATH
    echo ERROR: Inno Setup compiler (iscc) not found in PATH >> !LOG_FILE!
    echo Please ensure Inno Setup is installed and added to your PATH
    echo Please ensure Inno Setup is installed and added to your PATH >> !LOG_FILE!
    echo Download from: https://jrsoftware.org/isdl.php
    echo Download from: https://jrsoftware.org/isdl.php >> !LOG_FILE!
    exit /b 1
)

:: Create required directories
echo Setting up directories...
echo Setting up directories... >> !LOG_FILE!
if not exist ..\..\..\resources mkdir ..\..\..\resources 2>>!LOG_FILE!
if not exist ..\..\..\dist\installer mkdir ..\..\..\dist\installer 2>>!LOG_FILE!

:: Step 1: Build the executable with PyInstaller
echo.
echo. >> !LOG_FILE!
echo Step 1: Building executable with PyInstaller...
echo Step 1: Building executable with PyInstaller... >> !LOG_FILE!
python ..\scripts\build_exe.py >>!LOG_FILE! 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to build executable
    echo ERROR: Failed to build executable >> !LOG_FILE!
    echo Check log file for details: !LOG_FILE!
    exit /b 1
)

:: Verify the executable was created
if not exist ..\..\..\dist\HL7Parser\HL7Parser.exe (
    echo ERROR: Executable file not found after build
    echo ERROR: Executable file not found after build >> !LOG_FILE!
    echo Check log file for details: !LOG_FILE!
    exit /b 1
)
echo Executable created successfully.
echo Executable created successfully. >> !LOG_FILE!

:: Step 2: Create the installer with Inno Setup
echo.
echo. >> !LOG_FILE!
echo Step 2: Creating installer with Inno Setup...
echo Step 2: Creating installer with Inno Setup... >> !LOG_FILE!
iscc ..\config\installer.iss >>!LOG_FILE! 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to create installer
    echo ERROR: Failed to create installer >> !LOG_FILE!
    echo Check log file for details: !LOG_FILE!
    exit /b 1
)

:: Verify installer was created
if not exist ..\..\..\dist\installer\HL7Parser_Setup.exe (
    echo ERROR: Installer not found after build
    echo ERROR: Installer not found after build >> !LOG_FILE!
    echo Check log file for details: !LOG_FILE!
    exit /b 1
)

echo.
echo. >> !LOG_FILE!
echo Build completed successfully!
echo Build completed successfully! >> !LOG_FILE!
echo Installer can be found in: ..\..\..\dist\installer\
echo Installer can be found in: ..\..\..\dist\installer\ >> !LOG_FILE!
echo Log file: !LOG_FILE!

:: Open the folder containing the installer
explorer ..\..\..\dist\installer\

endlocal