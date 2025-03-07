from hl7apy.parser import parse_message
from hl7apy.core import Message
import io
import re

class HL7Parser:
    def __init__(self):
        self.message = None
        self.raw_message = None
        
    def parse_text(self, text):
        """Parse HL7 message from text input"""
        try:
            # Remove any whitespace and process the message
            text = text.strip()
            self.raw_message = text
            
            # Detect HL7 version from the message
            msh_segment = text.split('\n')[0]
            version = self._extract_version(msh_segment)
            
            # Try to parse with version validation disabled if it's 2.5.1
            if version == '2.5.1':
                # Fall back to version 2.5 which is supported
                # Create a simple structure directly since hl7apy doesn't support forcing versions
                self._create_simple_structure(text)
            else:
                # Use default parser for supported versions
                self.message = parse_message(text)
                
            return True
        except Exception as e:
            self.message = None
            self.raw_message = text
            
            # Create a simplified structured representation for unsupported versions
            if "is not supported" in str(e):
                self._create_simple_structure(text)
                return True
                
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
    
    def _extract_version(self, msh_segment):
        """Extract the HL7 version from the MSH segment"""
        try:
            fields = msh_segment.split('|')
            if len(fields) >= 12:
                return fields[11]
            return None
        except:
            return None
            
    def _create_simple_structure(self, text):
        """Create a simplified message structure when parsing fails"""
        self.message = SimpleHL7Message(text)
    
    def get_structure(self):
        """Returns hierarchical structure of the parsed message"""
        if not self.message:
            return None
        
        if isinstance(self.message, SimpleHL7Message):
            return self.message.get_structure()
        
        # Get the structure with segment counting
        segment_counts = {}
        return self._traverse_element(self.message, segment_counts)
    
    def _traverse_element(self, element, segment_counts):
        """Recursively traverse HL7 elements to build a hierarchical structure"""
        # Add segment numbering for top-level segments
        element_name = element.name
        display_name = element_name
        
        # If this is a segment (3 letter name) and not the MSH segment
        if len(element_name) == 3 and element_name.isalpha():
            # Initialize counter for this segment type if not exists
            if element_name not in segment_counts:
                segment_counts[element_name] = 1
            else:
                segment_counts[element_name] += 1
                
            # Add the segment number to the name
            display_name = f"{element_name} #{segment_counts[element_name]}"
            
        result = {
            'name': display_name,  # Use the display name with segment number
            'raw_name': element_name,  # Keep the original name
            'value': str(element.value) if hasattr(element, 'value') else None,
            'children': []
        }
        
        # If the element has children
        if hasattr(element, 'children'):
            for child in element.children:
                result['children'].append(self._traverse_element(child, segment_counts))
                
        return result


class SimpleHL7Message:
    """A simple HL7 message parser for when hl7apy fails due to version incompatibility"""
    
    def __init__(self, raw_text):
        self.raw_text = raw_text
        self.segments = []
        self._parse()
        
    def _parse(self):
        """Parse the raw HL7 message into segments"""
        lines = self.raw_text.split('\n')
        
        for line in lines:
            if not line.strip():
                continue
                
            # Split the segment into fields
            fields = line.split('|')
            segment_name = fields[0]
            
            segment = {
                'name': segment_name,
                'fields': []
            }
            
            # Add each field to the segment
            for i, field in enumerate(fields[1:], 1):
                segment['fields'].append({
                    'index': i,
                    'value': field
                })
                
            self.segments.append(segment)
    
    def get_structure(self):
        """Get a hierarchical structure of the message"""
        if not self.segments:
            return None
            
        result = {
            'name': 'Message',
            'value': f"Simplified Parser (compatibility mode)",
            'children': []
        }
        
        # Track segment counts
        segment_counts = {}
        
        # Add each segment as a child
        for segment in self.segments:
            segment_name = segment['name']
            
            # Count segments of the same type
            if segment_name not in segment_counts:
                segment_counts[segment_name] = 1
            else:
                segment_counts[segment_name] += 1
            
            # Add segment number to the display name
            display_name = f"{segment_name} #{segment_counts[segment_name]}"
            
            segment_node = {
                'name': display_name,
                'raw_name': segment_name,
                'value': '',
                'children': []
            }
            
            # Add fields as children of the segment
            for field in segment['fields']:
                field_node = {
                    'name': f"{segment_name}.{field['index']}",
                    'value': field['value'],
                    'children': []
                }
                segment_node['children'].append(field_node)
                
            result['children'].append(segment_node)
            
        return result
        
    @property
    def value(self):
        return None
        
    @property
    def name(self):
        return "HL7Message"
        
    @property
    def children(self):
        return []