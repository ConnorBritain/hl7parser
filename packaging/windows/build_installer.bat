@echo off
setlocal

echo HL7 Parser Windows Installer Build Script
echo =========================================

:: Check if Python is available
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ERROR: Python not found in PATH
    echo Please ensure Python is installed and added to your PATH
    exit /b 1
)

:: Check if PyInstaller is available
python -c "import PyInstaller" >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ERROR: PyInstaller not found
    echo Installing PyInstaller...
    python -m pip install pyinstaller
    if %ERRORLEVEL% neq 0 (
        echo Failed to install PyInstaller
        exit /b 1
    )
)

:: Check if Inno Setup is available
where iscc >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ERROR: Inno Setup compiler (iscc) not found in PATH
    echo Please ensure Inno Setup is installed and added to your PATH
    echo Download from: https://jrsoftware.org/isdl.php
    exit /b 1
)

:: Create required directories
mkdir ..\..\resources 2>nul
mkdir ..\..\dist\installer 2>nul

:: Step 1: Build the executable with PyInstaller
echo.
echo Step 1: Building executable with PyInstaller...
python build_exe.py
if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to build executable
    exit /b 1
)

:: Step 2: Create the installer with Inno Setup
echo.
echo Step 2: Creating installer with Inno Setup...
iscc installer.iss
if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to create installer
    exit /b 1
)

echo.
echo Build completed successfully!
echo Installer can be found in: ..\..\dist\installer\

:: Open the folder containing the installer
explorer ..\..\dist\installer\

endlocal