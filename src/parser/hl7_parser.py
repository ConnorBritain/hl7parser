from hl7apy.parser import parse_message
from hl7apy.core import Message
import io

class HL7Parser:
    def __init__(self):
        self.message = None
        
    def parse_text(self, text):
        """Parse HL7 message from text input"""
        try:
            # Remove any whitespace and process the message
            text = text.strip()
            self.message = parse_message(text)
            return True
        except Exception as e:
            self.message = None
            raise ValueError(f"Failed to parse HL7 message: {str(e)}")
    
    def parse_file(self, file_path):
        """Parse HL7 message from file path"""
        try:
            with open(file_path, 'r') as f:
                content = f.read().strip()
            return self.parse_text(content)
        except Exception as e:
            self.message = None
            raise ValueError(f"Failed to read or parse file: {str(e)}")
    
    def get_structure(self):
        """Returns hierarchical structure of the parsed message"""
        if not self.message:
            return None
        
        return self._traverse_element(self.message)
    
    def _traverse_element(self, element):
        """Recursively traverse HL7 elements to build a hierarchical structure"""
        result = {
            'name': element.name,
            'value': str(element.value) if hasattr(element, 'value') else None,
            'children': []
        }
        
        # If the element has children
        if hasattr(element, 'children'):
            for child in element.children:
                result['children'].append(self._traverse_element(child))
                
        return result