@echo off
echo Installing PySide6 as an alternative to PyQt6...

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Show current Python and pip versions
python --version
pip --version

:: Uninstall PyQt6 components
pip uninstall -y PyQt6 PyQt6-Qt6 PyQt6-sip

:: Install PySide6 (alternative Qt binding)
pip install PySide6==6.5.3

:: Create compatibility layer
echo Creating compatibility layer...
if not exist venv\Lib\site-packages\PyQt6 mkdir venv\Lib\site-packages\PyQt6
echo from PySide6 import QtCore, QtGui, QtWidgets > venv\Lib\site-packages\PyQt6\__init__.py
echo # PySide6 compatibility layer >> venv\Lib\site-packages\PyQt6\__init__.py
echo QtCore.Qt.Orientation = QtCore.Qt.Orientation >> venv\Lib\site-packages\PyQt6\__init__.py
echo QtWidgets.QTreeView.EditTrigger = QtWidgets.QTreeView.EditTrigger >> venv\Lib\site-packages\PyQt6\__init__.py
echo QtGui.QStandardItemModel = QtGui.QStandardItemModel >> venv\Lib\site-packages\PyQt6\__init__.py
echo QtGui.QStandardItem = QtGui.QStandardItem >> venv\Lib\site-packages\PyQt6\__init__.py
echo QtGui.QClipboard = QtGui.QClipboard >> venv\Lib\site-packages\PyQt6\__init__.py

echo.
echo PySide6 installation complete! Run the application with:
echo run_windows.bat

pause