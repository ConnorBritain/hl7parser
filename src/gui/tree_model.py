from PyQt6.QtCore import Qt, QAbstractItemModel, QModelIndex
from PyQt6.QtGui import QStandardItemModel, QStandardItem

class HL7TreeItem:
    def __init__(self, name, value=None, description=None, parent=None):
        self.name = name
        self.value = value
        self.description = description
        self.parent_item = parent
        self.child_items = []
        
    def appendChild(self, item):
        self.child_items.append(item)
        
    def child(self, row):
        if row < 0 or row >= len(self.child_items):
            return None
        return self.child_items[row]
        
    def childCount(self):
        return len(self.child_items)
        
    def columnCount(self):
        return 3  # Name, Value, and Description
        
    def data(self, column):
        if column == 0:
            return self.name
        elif column == 1:
            # Description column
            return self.description if hasattr(self, 'description') else ""
        elif column == 2:
            return self.value if self.value else ""
        return None
        
    def parent(self):
        return self.parent_item
        
    def row(self):
        if self.parent_item:
            return self.parent_item.child_items.index(self)
        return 0

class HL7TreeModel(QAbstractItemModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.root_item = HL7TreeItem("Root")
        
    def setData(self, structure):
        """Set data from HL7 parser structure"""
        self.beginResetModel()
        self.root_item = HL7TreeItem("Root")
        if structure:
            description = structure.get('description', '')
            root = HL7TreeItem(structure['name'], structure['value'], description)
            self.root_item.appendChild(root)
            self._populate_tree(root, structure['children'])
        self.endResetModel()
        
    def _populate_tree(self, parent, children):
        for child in children:
            description = child.get('description', '')
            item = HL7TreeItem(child['name'], child['value'], description, parent)
            parent.appendChild(item)
            if child['children']:
                self._populate_tree(item, child['children'])
                
    def index(self, row, column, parent=QModelIndex()):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
            
        if not parent.isValid():
            parent_item = self.root_item
        else:
            parent_item = parent.internalPointer()
            
        child_item = parent_item.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        return QModelIndex()
        
    def parent(self, index):
        if not index.isValid():
            return QModelIndex()
            
        child_item = index.internalPointer()
        parent_item = child_item.parent()
        
        if parent_item == self.root_item or parent_item is None:
            return QModelIndex()
            
        return self.createIndex(parent_item.row(), 0, parent_item)
        
    def rowCount(self, parent=QModelIndex()):
        if parent.column() > 0:
            return 0
            
        if not parent.isValid():
            parent_item = self.root_item
        else:
            parent_item = parent.internalPointer()
            
        return parent_item.childCount()
        
    def columnCount(self, parent=QModelIndex()):
        return 3
        
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
            
        if role != Qt.ItemDataRole.DisplayRole:
            return None
            
        item = index.internalPointer()
        return item.data(index.column())
        
    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            if section == 0:
                return "Element"
            elif section == 1:
                return "Description"
            elif section == 2:
                return "Value"
        return None