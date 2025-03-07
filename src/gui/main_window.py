import sys
import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTextEdit, QPushButton, QFileDialog, QMessageBox,
                             QTreeView, QLabel, QSplitter, QFrame)
from PyQt6.QtCore import Qt, QModelIndex, QSettings
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QClipboard

from parser.hl7_parser import HL7Parser
from gui.tree_model import HL7TreeModel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.parser = HL7Parser()
        
        # Settings for the application
        self.settings = QSettings("HL7Parser", "hl7parser")
        
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("HL7 Parser")
        self.setGeometry(100, 100, 1200, 800)
        
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        
        # Create splitter for resizable sections
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Top section - Input area
        input_widget = QWidget()
        input_layout = QVBoxLayout()
        input_widget.setLayout(input_layout)
        
        input_label = QLabel("Enter or paste HL7 message:")
        self.input_text = QTextEdit()
        self.input_text.setMinimumHeight(200)
        
        button_layout = QHBoxLayout()
        
        self.parse_button = QPushButton("Parse Message")
        self.parse_button.clicked.connect(self.parse_input_text)
        
        self.load_button = QPushButton("Load File")
        self.load_button.clicked.connect(self.load_file)
        
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_input)
        
        button_layout.addWidget(self.parse_button)
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.clear_button)
        
        input_layout.addWidget(input_label)
        input_layout.addWidget(self.input_text)
        input_layout.addLayout(button_layout)
        
        # Bottom section - Tree view
        output_widget = QWidget()
        output_layout = QVBoxLayout()
        output_widget.setLayout(output_layout)
        
        output_label = QLabel("Parsed Message Structure:")
        self.tree_view = QTreeView()
        self.tree_view.setMinimumHeight(300)
        self.tree_model = QStandardItemModel()
        self.tree_model.setHorizontalHeaderLabels(["Element", "Description", "Value"])
        
        # Set tooltips for the headers
        self.tree_model.setHeaderData(0, Qt.Orientation.Horizontal, "Segment and field elements", Qt.ItemDataRole.ToolTipRole)
        self.tree_model.setHeaderData(1, Qt.Orientation.Horizontal, "Description of the HL7 element", Qt.ItemDataRole.ToolTipRole)
        self.tree_model.setHeaderData(2, Qt.Orientation.Horizontal, "Content values for each element", Qt.ItemDataRole.ToolTipRole)
        
        self.tree_view.setModel(self.tree_model)
        self.tree_view.setAlternatingRowColors(True)
        self.tree_view.setEditTriggers(QTreeView.EditTrigger.NoEditTriggers)
        
        # Make tree view expand to show all content
        self.tree_view.setTextElideMode(Qt.TextElideMode.ElideMiddle)  # Elide in middle if needed
        self.tree_view.setWordWrap(True)  # Enable word wrap
        
        # Make header responsive to user resizing
        self.tree_view.header().setSectionsClickable(True)
        self.tree_view.header().setDefaultSectionSize(150)
        
        # Connect signals to handle resizing when items expand
        self.tree_view.expanded.connect(self.on_item_expanded)
        self.tree_view.collapsed.connect(self.on_item_collapsed)
        
        export_layout = QHBoxLayout()
        self.copy_button = QPushButton("Copy to Clipboard")
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        self.export_button = QPushButton("Export to File")
        self.export_button.clicked.connect(self.export_to_file)
        
        export_layout.addWidget(self.copy_button)
        export_layout.addWidget(self.export_button)
        
        output_layout.addWidget(output_label)
        output_layout.addWidget(self.tree_view)
        output_layout.addLayout(export_layout)
        
        # Add widgets to splitter
        splitter.addWidget(input_widget)
        splitter.addWidget(output_widget)
        
        # Add splitter to main layout
        main_layout.addWidget(splitter)
        
        # Set central widget
        self.setCentralWidget(main_widget)
    
    def parse_input_text(self):
        text = self.input_text.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "Warning", "Please enter an HL7 message to parse.")
            return
        
        try:
            self.parser.parse_text(text)
            self.display_message_structure()
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
    
    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open HL7 File", "", "HL7 Files (*.hl7);;All Files (*)"
        )
        
        if not file_path:
            return
        
        try:
            self.parser.parse_file(file_path)
            with open(file_path, 'r') as f:
                self.input_text.setPlainText(f.read())
            self.display_message_structure()
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
    
    def display_message_structure(self):
        self.tree_model.clear()
        self.tree_model.setHorizontalHeaderLabels(["Element", "Description", "Value"])
        
        structure = self.parser.get_structure()
        if not structure:
            return
        
        root_item = QStandardItem(structure['name'])
        
        # Get description for root item
        description = ""
        if 'description' in structure and structure['description']:
            description = structure['description']
            root_item.setToolTip(description)
        
        # Create description item
        description_item = QStandardItem(description)
            
        if structure['value']:
            value_item = QStandardItem(structure['value'])
            self.tree_model.appendRow([root_item, description_item, value_item])
        else:
            self.tree_model.appendRow([root_item, description_item, QStandardItem()])
        
        self.populate_tree(root_item, structure['children'])
        
        # Expand the first level
        self.tree_view.expandToDepth(0)
        
        # Make columns interactive and resizable by user
        self.tree_view.header().setSectionResizeMode(0, self.tree_view.header().ResizeMode.Interactive)
        self.tree_view.header().setSectionResizeMode(1, self.tree_view.header().ResizeMode.Interactive)
        self.tree_view.header().setSectionResizeMode(2, self.tree_view.header().ResizeMode.Interactive)
        
        # Load saved column widths from settings or use defaults
        element_width = self.settings.value("column_widths/element", 150, type=int)
        description_width = self.settings.value("column_widths/description", 300, type=int)
        value_width = self.settings.value("column_widths/value", 150, type=int)
        
        # Set initial column sizes
        self.tree_view.header().resizeSection(0, element_width)  # Element column
        self.tree_view.header().resizeSection(1, description_width)  # Description column
        self.tree_view.header().resizeSection(2, value_width)  # Value column
        
        # Connect to column resize signal
        self.tree_view.header().sectionResized.connect(self.save_column_sizes)
        
        # Enable user ability to resize header sections
        self.tree_view.header().setStretchLastSection(False)
        self.tree_view.header().setSectionsMovable(False)  # Prevent column reordering
        self.tree_view.header().setMinimumSectionSize(50)  # Minimum column width
    
    def populate_tree(self, parent_item, children):
        for child in children:
            # Create item with name and description if available
            name_text = child['name']
            description = ""
            
            if 'description' in child and child['description']:
                # Add tooltip with description
                description = child['description']
                child_item = QStandardItem(name_text)
                child_item.setToolTip(description)
                # Print first 5 items for debugging
                if len(parent_item.text()) <= 3:  # Only for top-level segments
                    print(f"Added tooltip for {name_text}: {description}", file=sys.stderr)
            else:
                child_item = QStandardItem(name_text)
                if len(parent_item.text()) <= 3:  # Only for top-level segments
                    print(f"No description for {name_text}", file=sys.stderr)
                
            value_item = QStandardItem(child['value'] if child['value'] else "")
            description_item = QStandardItem(description)
            
            parent_item.appendRow([child_item, description_item, value_item])
            
            if child['children']:
                self.populate_tree(child_item, child['children'])
    
    def clear_input(self):
        self.input_text.clear()
        self.tree_model.clear()
        self.tree_model.setHorizontalHeaderLabels(["Element", "Description", "Value"])
    
    def copy_to_clipboard(self):
        if not self.parser.message:
            QMessageBox.warning(self, "Warning", "No parsed message to copy.")
            return
        
        clipboard = self.window().clipboard()
        clipboard.setText(str(self.parser.message))
        
        QMessageBox.information(
            self, 
            "Privacy Warning", 
            "The parsed message has been copied to your clipboard. "
            "Remember that this data may contain PHI. "
            "Paste it only in secure locations and clear your clipboard when done."
        )
    
    def export_to_file(self):
        if not self.parser.message:
            QMessageBox.warning(self, "Warning", "No parsed message to export.")
            return
        
        confirmation = QMessageBox.question(
            self,
            "Privacy Warning",
            "Exporting will save PHI to disk. Only do this if necessary and secure. Continue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if confirmation == QMessageBox.StandardButton.No:
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Parsed Message", "", "Text Files (*.txt);;All Files (*)"
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'w') as f:
                f.write(str(self.parser.message))
            
            QMessageBox.information(
                self,
                "Export Complete",
                f"Message exported to {file_path}. Please delete this file when no longer needed."
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export: {str(e)}")
            
    def on_item_expanded(self, index):
        """Handle item expansion without resizing columns to preserve user's column widths"""
        # We don't auto-resize columns anymore to respect user's manual sizing
        pass
        
    def on_item_collapsed(self, index):
        """Handle item collapse without resizing columns to preserve user's column widths"""
        # We don't auto-resize columns anymore to respect user's manual sizing
        pass
        
    def save_column_sizes(self, logical_index, old_size, new_size):
        """Save the column sizes when user resizes them"""
        if logical_index == 0:
            self.settings.setValue("column_widths/element", new_size)
        elif logical_index == 1:
            self.settings.setValue("column_widths/description", new_size)
        elif logical_index == 2:
            self.settings.setValue("column_widths/value", new_size)
        
        # Ensure settings are saved immediately
        self.settings.sync()
        
    def closeEvent(self, event):
        """Handle window close event"""
        # Save all column widths one last time before closing
        self.settings.setValue("column_widths/element", self.tree_view.header().sectionSize(0))
        self.settings.setValue("column_widths/description", self.tree_view.header().sectionSize(1))
        self.settings.setValue("column_widths/value", self.tree_view.header().sectionSize(2))
        self.settings.sync()
        
        # This ensures the application fully exits when the window is closed
        # so the terminal doesn't wait for keypress
        event.accept()  # Accept the close event
        self.window().deleteLater()  # Schedule the window for deletion
        # Use exit with code 0 to terminate completely
        import sys
        sys.exit(0)