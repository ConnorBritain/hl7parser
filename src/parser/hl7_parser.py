from hl7apy.parser import parse_message
from hl7apy.core import Message
import io
import re
import sys

# Try to import definitions or provide fallback
try:
    from .hl7_definitions import HL7_SEGMENTS, HL7_FIELDS, ADT_CODES
    print("Successfully imported HL7 definitions", file=sys.stderr)
except ImportError as e:
    print(f"Error importing HL7 definitions: {e}", file=sys.stderr)
    # Fallback empty definitions
    HL7_SEGMENTS = {}
    HL7_FIELDS = {}
    ADT_CODES = {}

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
        
        # First, scan the message to count total segments of each type
        segment_totals = self._count_segment_types(self.message)
        
        # Get the structure with segment counting
        segment_counts = {}
        return self._traverse_element(self.message, segment_counts, segment_totals)
    
    def _count_segment_types(self, element):
        """Count how many of each segment type are in the message"""
        totals = {}
        
        # Process this element if it's a segment
        if len(element.name) == 3 and element.name.isalpha():
            totals[element.name] = 1
        
        # Process children
        if hasattr(element, 'children'):
            for child in element.children:
                if len(child.name) == 3 and child.name.isalpha():
                    totals[child.name] = totals.get(child.name, 0) + 1
        
        return totals
        
    def _traverse_element(self, element, segment_counts, segment_totals, parent_segment=None):
        """Recursively traverse HL7 elements to build a hierarchical structure"""
        element_name = element.name
        display_name = element_name
        
        # If this is a segment (3 letter name at top level)
        if len(element_name) == 3 and element_name.isalpha() and parent_segment is None:
            # Initialize counter for this segment type if not exists
            if element_name not in segment_counts:
                segment_counts[element_name] = 1
            else:
                segment_counts[element_name] += 1
            
            # Only add the number if there are multiple segments of this type
            if segment_totals.get(element_name, 0) > 1:
                display_name = f"{element_name} #{segment_counts[element_name]}"
            
            # Remember this segment name for children
            parent_segment = element_name
        # If this is a field or component inside a segment, show the proper index format
        elif parent_segment is not None:
            # For fields, use format "MSH-1", "MSH-2", etc.
            if '.' not in element_name and element_name.isdigit():
                display_name = f"{parent_segment}-{element_name}"
            # For existing field indices like "1", "2", just keep them
            elif element_name.isdigit():
                display_name = element_name
            
        # Add segment/field description
        description = ""
        if len(element_name) == 3 and element_name.isalpha() and parent_segment is None:
            # Segment description
            description = HL7_SEGMENTS.get(element_name, "Unknown Segment")
        elif parent_segment is not None and element_name.isdigit():
            # Field description
            if parent_segment in HL7_FIELDS and element_name in HL7_FIELDS[parent_segment]:
                description = HL7_FIELDS[parent_segment][element_name]
            else:
                description = f"Field {element_name}"
                
        value = str(element.value) if hasattr(element, 'value') else None
        
        # Special case for MSH-1 field - field separator character
        if parent_segment == 'MSH' and element_name == '1':
            # MSH-1 is always the field separator character (|)
            value = '|'
        
        # Special handling for MSH-9 (Message Type) field
        if parent_segment == 'MSH' and element_name == '9' and value and '^' in value:
            # Try to extract the message type and trigger event
            parts = value.split('^')
            if len(parts) >= 2 and parts[0] == 'ADT':
                event_code = parts[1]
                if event_code in ADT_CODES:
                    description += f" - {ADT_CODES[event_code]}"
                    
        result = {
            'name': display_name,  # Use the appropriate display name 
            'raw_name': element_name,  # Keep the original name
            'description': description,
            'value': value,
            'children': []
        }
        
        # If the element has children
        if hasattr(element, 'children'):
            for child in element.children:
                result['children'].append(self._traverse_element(child, segment_counts, segment_totals, parent_segment))
                
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
            
            # Special case for MSH segment - handle MSH-1 field correctly
            if segment_name == 'MSH':
                # MSH-1 is the field separator character (|)
                segment['fields'].append({
                    'index': 1,
                    'value': '|'  # This is always | per HL7 standard
                })
                
                # Continue with the rest of fields, but offset by 1
                for i, field in enumerate(fields[1:], 2):
                    segment['fields'].append({
                        'index': i,
                        'value': field
                    })
            else:
                # Regular segment - add each field to the segment
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
            'value': "",  # Remove Simplified Parser text
            'description': "HL7 Message",
            'children': []
        }
        
        # First pass - count total segments of each type
        segment_totals = {}
        for segment in self.segments:
            segment_name = segment['name']
            segment_totals[segment_name] = segment_totals.get(segment_name, 0) + 1
            
        # Track segment counts for the second pass
        segment_counts = {}
        
        # Add each segment as a child
        for segment in self.segments:
            segment_name = segment['name']
            
            # Count segments of the same type
            if segment_name not in segment_counts:
                segment_counts[segment_name] = 1
            else:
                segment_counts[segment_name] += 1
            
            # Only add segment number if there are multiple segments of this type
            display_name = segment_name
            if segment_totals[segment_name] > 1:
                display_name = f"{segment_name} #{segment_counts[segment_name]}"
            
            segment_node = {
                'name': display_name,
                'raw_name': segment_name,
                'description': HL7_SEGMENTS.get(segment_name, "Unknown Segment"),
                'value': '',
                'children': []
            }
            
            # Add fields as children of the segment
            for field in segment['fields']:
                field_index = str(field['index'])
                description = "Unknown Field"
                
                # Look up field description if available
                if segment_name in HL7_FIELDS and field_index in HL7_FIELDS[segment_name]:
                    description = HL7_FIELDS[segment_name][field_index]
                
                # Special handling for MSH-9 (Message Type) field
                if segment_name == 'MSH' and field_index == '9' and field['value'] and '^' in field['value']:
                    # Try to extract the message type and trigger event
                    parts = field['value'].split('^')
                    if len(parts) >= 2 and parts[0] == 'ADT':
                        event_code = parts[1]
                        if event_code in ADT_CODES:
                            description += f" - {ADT_CODES[event_code]}"
                
                field_node = {
                    'name': f"{segment_name}-{field_index}",  # Use dash format for segment fields
                    'raw_name': field_index,
                    'description': description,
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