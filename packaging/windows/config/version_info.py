#!/usr/bin/env python3
"""
Version information generator for the HL7Parser Windows executable.
This script creates the version resource for the Windows binary.
"""

VERSION_INFO = {
    'CompanyName': 'Dovetree AI Holdings, LLC',
    'FileDescription': 'HL7 Message Parser and Viewer',
    'FileVersion': '1.0.0',
    'InternalName': 'HL7Parser',
    'LegalCopyright': '© 2025 Dovetree AI Holdings, LLC',
    'OriginalFilename': 'HL7Parser.exe',
    'ProductName': 'HL7 Parser',
    'ProductVersion': '1.0.0',
}

import sys
from pathlib import Path

def generate_version_info():
    """Generate the version info file for PyInstaller."""
    version_info = f"""VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'{VERSION_INFO['CompanyName']}'),
        StringStruct(u'FileDescription', u'{VERSION_INFO['FileDescription']}'),
        StringStruct(u'FileVersion', u'{VERSION_INFO['FileVersion']}'),
        StringStruct(u'InternalName', u'{VERSION_INFO['InternalName']}'),
        StringStruct(u'LegalCopyright', u'{VERSION_INFO['LegalCopyright']}'),
        StringStruct(u'OriginalFilename', u'{VERSION_INFO['OriginalFilename']}'),
        StringStruct(u'ProductName', u'{VERSION_INFO['ProductName']}'),
        StringStruct(u'ProductVersion', u'{VERSION_INFO['ProductVersion']}')
        ])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""
    output_path = Path(__file__).parent / "windows_version_info.txt"
    with open(output_path, 'w') as f:
        f.write(version_info)
    print(f"Version info written to {output_path}")

if __name__ == "__main__":
    generate_version_info()