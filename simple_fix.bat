@echo off
echo Running simple PyQt6 wheel installation...

:: Activate virtual environment  
call venv\Scripts\activate.bat

:: Show current Python version
python --version

:: Uninstall previous PyQt6 attempts if they exist
pip uninstall -y PyQt6 PyQt6-Qt6 PyQt6-sip

:: Install prebuilt wheels directly using pip
pip install --only-binary=:all: PyQt6

echo.
echo Installation complete! Run the application with:
echo run_windows.bat

pause