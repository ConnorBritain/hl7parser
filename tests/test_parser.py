import os
import sys
import pytest

# Add the src directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.parser.hl7_parser import HL7Parser

def test_parse_text():
    """Test parsing an HL7 message from text"""
    parser = HL7Parser()
    sample_hl7 = "MSH|^~\\&|SENDING_APP|SENDING_FAC|RECEIVING_APP|RECEIVING_FAC|20230101120000||ADT^A01|MSG00001|P|2.5.1"
    
    result = parser.parse_text(sample_hl7)
    assert result is True
    assert parser.message is not None
    assert parser.message.name == "MSH"
    
    structure = parser.get_structure()
    assert structure is not None
    assert structure["name"] == "MSH"
    assert len(structure["children"]) > 0

def test_invalid_message():
    """Test parsing an invalid HL7 message"""
    parser = HL7Parser()
    
    with pytest.raises(ValueError):
        parser.parse_text("This is not an HL7 message")
        
    # Message should be None after failed parse
    assert parser.message is None