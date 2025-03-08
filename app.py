#!/usr/bin/env python3
"""
Standalone HL7 Parser application with all code in a single file.
This avoids module import issues when bundled with PyInstaller.
"""
import sys
import os
import traceback
import datetime
import pathlib
from pathlib import Path

# Global log file handle for use throughout
global_log_file = None
log_handler = None

def log_message(msg):
    """Write a message to the log file and print it."""
    try:
        if log_handler:
            log_handler.write(f"{msg}\n")
            log_handler.flush()
        print(msg)
    except Exception as e:
        print(f"Error logging: {e}")

try:
    # Setup logging
    def setup_logging():
        """Set up logging to capture errors and debug information."""
        global log_handler, global_log_file
        
        try:
            if getattr(sys, 'frozen', False):
                # Running as compiled exe
                app_dir = Path(os.path.dirname(sys.executable))
            else:
                # Running from source
                app_dir = Path(os.path.dirname(os.path.abspath(__file__)))
            
            # Create logs directory
            log_dir = app_dir / "logs"
            log_dir.mkdir(exist_ok=True)
            
            # Create timestamped log file
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = log_dir / f"hl7parser_{timestamp}.log"
            global_log_file = str(log_file)
            
            # Set up logging to file
            log_handler = open(log_file, "w", encoding="utf-8")
            
            # Only redirect in frozen mode
            if getattr(sys, 'frozen', False):
                # Keep reference to original stdout/stderr
                original_stdout = sys.stdout
                original_stderr = sys.stderr
                
                # Create a custom file-like object that writes to both log and console
                class MultiWriter:
                    def __init__(self, file, original):
                        self.file = file
                        self.original = original
                    
                    def write(self, text):
                        try:
                            self.file.write(text)
                            self.file.flush()  # Ensure immediate writing
                            self.original.write(text)
                        except Exception as e:
                            self.original.write(f"Error writing to log: {e}\n")
                    
                    def flush(self):
                        try:
                            self.file.flush()
                            self.original.flush()
                        except:
                            pass
                
                # Replace stdout and stderr with our custom writer
                sys.stdout = MultiWriter(log_handler, original_stdout)
                sys.stderr = MultiWriter(log_handler, original_stderr)
            
            return log_file
        except Exception as e:
            print(f"Error setting up logging: {e}")
            traceback.print_exc()
            return None

    # Set up logging
    log_file = setup_logging()

    # Log startup information
    log_message("=" * 50)
    log_message(f"HL7 Parser starting at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log_message("=" * 50)
    log_message(f"Python version: {sys.version}")
    log_message(f"Executable: {sys.executable}")
    log_message(f"Current directory: {os.getcwd()}")
    
    if getattr(sys, 'frozen', False):
        log_message("Running as frozen application")
        log_message(f"Path to executable: {sys.executable}")
        base_dir = os.path.dirname(sys.executable)
        log_message(f"Base directory: {base_dir}")
        log_message("Directory contents:")
        try:
            for item in os.listdir(base_dir):
                log_message(f"  {item}")
        except Exception as e:
            log_message(f"Error listing directory: {e}")
    else:
        log_message("Running from source code")

    # Import PyQt6
    log_message("Importing PyQt6...")
    try:
        from PyQt6.QtWidgets import (
            QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
            QTextEdit, QPushButton, QFileDialog, QMessageBox,
            QTreeView, QLabel, QSplitter, QFrame
        )
        from PyQt6.QtCore import Qt, QModelIndex, QSettings
        from PyQt6.QtGui import QStandardItemModel, QStandardItem, QClipboard
        log_message("PyQt6 imported successfully")
    except ImportError as e:
        log_message(f"Error importing PyQt6: {e}")
        log_message("This is a critical error. The application cannot run without PyQt6.")
        log_message(traceback.format_exc())
        
        # If we're in a frozen app, show a visual error message
        if getattr(sys, 'frozen', False):
            # Use tkinter as a fallback for displaying an error message
            try:
                import tkinter as tk
                from tkinter import messagebox
                root = tk.Tk()
                root.withdraw()  # Hide the main window
                messagebox.showerror("HL7 Parser Error", 
                                  f"Failed to import PyQt6. The application cannot run.\n\n"
                                  f"Error: {str(e)}\n\n"
                                  f"Please check the log file at: {global_log_file}")
            except:
                # If even tkinter fails, we're out of options
                pass
            
        # Re-raise to stop execution
        raise

    # HL7 Segment and Field Definitions
    HL7_SEGMENTS = {
        'ABS': 'Abstract',
        'ACC': 'Accident',
        'ADD': 'Addendum',
        'ADJ': 'Adjustment',
        'AFF': 'Professional Affiliation',
        'AIG': 'Appointment Information - General Resource',
        'AIL': 'Appointment Information - Location Resource',
        'AIP': 'Appointment Information - Personnel Resource',
        'AIS': 'Appointment Information - Service Resource',
        'AL1': 'Patient Allergy Information',
        'APR': 'Appointment Preferences',
        'ARQ': 'Appointment Request',
        'ARV': 'Access Restriction',
        'AUT': 'Authorization Information',
        'BHS': 'Batch Header',
        'BLC': 'Blood Code',
        'BLG': 'Billing',
        'BPO': 'Blood Product Order',
        'BPX': 'Blood Product Dispense Status',
        'BTX': 'Blood Product Transfusion/Disposition',
        'BUI': 'Blood Unit Information',
        'CDM': 'Charge Description Master',
        'CDO': 'Clinical Study with Phases and Schedules',
        'CER': 'Certificate Detail',
        'CM0': 'Clinical Study Master',
        'CM1': 'Clinical Study Phase Master',
        'CM2': 'Clinical Study Schedule Master',
        'CNS': 'Clear Notification',
        'CON': 'Consent Segment',
        'CSP': 'Clinical Study Phase',
        'CSR': 'Clinical Study Registration',
        'CSS': 'Clinical Study Data Schedule Segment',
        'CTD': 'Contact Data',
        'CTI': 'Clinical Trial Identification',
        'DB1': 'Disability',
        'DG1': 'Diagnosis',
        'DMI': 'DRG Master File Information',
        'DON': 'Donation Segment',
        'DRG': 'Diagnosis Related Group',
        'DSC': 'Continuation Pointer',
        'DSP': 'Display Data',
        'ECD': 'Equipment Command',
        'ECR': 'Equipment Command Response',
        'EDU': 'Educational Detail',
        'EQP': 'Equipment/log Service',
        'EQU': 'Equipment Detail',
        'ERR': 'Error',
        'EVN': 'Event Type',
        'FAC': 'Facility',
        'FHS': 'File Header',
        'FT1': 'Financial Transaction',
        'FTS': 'File Trailer',
        'GOL': 'Goal Detail',
        'GP1': 'Grouping/Reimbursement - Visit',
        'GP2': 'Grouping/Reimbursement - Procedure Line Item',
        'GT1': 'Guarantor',
        'IAM': 'Patient Adverse Reaction Information',
        'IAR': 'Allergy Reaction',
        'IIM': 'Inventory Item Master',
        'ILT': 'Material Lot',
        'IN1': 'Insurance',
        'IN2': 'Insurance Additional Information',
        'IN3': 'Insurance Additional Information, Certification',
        'INV': 'Inventory Detail',
        'IPC': 'Imaging Procedure Control Segment',
        'IPR': 'Invoice Processing Results',
        'ISD': 'Interaction Status Detail',
        'ITM': 'Material Item',
        'IVC': 'Invoice Segment',
        'IVT': 'Material Location',
        'LAN': 'Language Detail',
        'LCC': 'Location Charge Code',
        'LCH': 'Location Characteristic',
        'LDP': 'Location Department',
        'LOC': 'Location Identification',
        'LRL': 'Location Relationship',
        'MFA': 'Master File Acknowledgment',
        'MFE': 'Master File Entry',
        'MFI': 'Master File Identification',
        'MRG': 'Merge Patient Information',
        'MSA': 'Message Acknowledgment',
        'MSH': 'Message Header',
        'NCK': 'System Clock',
        'NDS': 'Notification Detail',
        'NK1': 'Next of Kin / Associated Parties',
        'NPU': 'Bed Status Update',
        'NSC': 'Application Status Change',
        'NST': 'Application Control Level Statistics',
        'NTE': 'Notes and Comments',
        'OBR': 'Observation Request',
        'OBX': 'Observation/Result',
        'ODS': 'Dietary Orders, Supplements, and Preferences',
        'ODT': 'Diet Tray Instructions',
        'OM1': 'General Segment',
        'OM2': 'Numeric Observation',
        'OM3': 'Categorical Service/Test/Observation',
        'OM4': 'Observations that Require Specimens',
        'OM5': 'Observation Batteries (Sets)',
        'OM6': 'Observations that are Calculated from Other Observations',
        'OM7': 'Additional Basic Attributes',
        'ORC': 'Common Order',
        'ORG': 'Practitioner Organization Unit',
        'OVR': 'Override Segment',
        'PAC': 'Shipment Packaging',
        'PCE': 'Patient Charge Cost Center Exceptions',
        'PCR': 'Possible Causal Relationship',
        'PD1': 'Patient Additional Demographic',
        'PDA': 'Patient Death and Autopsy',
        'PDC': 'Product Detail Country',
        'PEO': 'Product Experience Observation',
        'PES': 'Product Experience Sender',
        'PID': 'Patient Identification',
        'PKG': 'Item Packaging',
        'PMT': 'Payment Information',
        'PR1': 'Procedures',
        'PRA': 'Practitioner Detail',
        'PRB': 'Problem Details',
        'PRC': 'Pricing',
        'PRD': 'Provider Data',
        'PRT': 'Participation Information',
        'PSG': 'Product/Service Group',
        'PSH': 'Product Summary Header',
        'PSL': 'Product/Service Line Item',
        'PSS': 'Product/Service Section',
        'PTH': 'Pathway',
        'PV1': 'Patient Visit',
        'PV2': 'Patient Visit - Additional Information',
        'PYE': 'Payee Information',
        'QAK': 'Query Acknowledgment',
        'QID': 'Query Identification',
        'QPD': 'Query Parameter Definition',
        'QRD': 'Original-Style Query Definition',
        'QRF': 'Original style query filter',
        'QRI': 'Query Response Instance',
        'RCP': 'Response Control Parameter',
        'RDF': 'Table Row Definition',
        'RDT': 'Table Row Data',
        'REL': 'Clinical Relationship Segment',
        'RF1': 'Referral Information',
        'RFI': 'Request for Information',
        'RGS': 'Resource Group',
        'RMI': 'Risk Management Incident',
        'ROL': 'Role',
        'RQ1': 'Requisition Detail-1',
        'RQD': 'Requisition Detail',
        'RXA': 'Pharmacy/Treatment Administration',
        'RXC': 'Pharmacy/Treatment Component Order',
        'RXD': 'Pharmacy/Treatment Dispense',
        'RXE': 'Pharmacy/Treatment Encoded Order',
        'RXG': 'Pharmacy/Treatment Give',
        'RXO': 'Pharmacy/Treatment Order',
        'RXR': 'Pharmacy/Treatment Route',
        'RXV': 'Pharmacy/Treatment Infusion',
        'SAC': 'Specimen Container detail',
        'SCH': 'Scheduling Activity Information',
        'SCP': 'Sterilizer Configuration',
        'SDD': 'Sterilization Device Data',
        'SFT': 'Software Segment',
        'SHP': 'Shipment',
        'SID': 'Substance Identifier',
        'SLT': 'Sterilization Lot',
        'SPM': 'Specimen',
        'SPS': 'Specimen Source',
        'STF': 'Staff Identification',
        'STZ': 'Sterilization Parameter',
        'TCC': 'Test Code Configuration',
        'TCD': 'Test Code Detail',
        'TQ1': 'Timing/Quantity',
        'TQ2': 'Timing/Quantity Relationship',
        'TXA': 'Transcription Document Header',
        'UB1': 'UB82 Billing',
        'UB2': 'UB92 Uniform Billing',
        'URD': 'Results/Update Definition',
        'URS': 'Results/Update Selection Criteria',
        'VAR': 'Variance',
        'VND': 'Purchasing Vendor',
        'ZXX': 'User-defined Segment'
    }

    # Field definitions for each segment
    HL7_FIELDS = {
        'MSH': {
            '1': 'Field Separator (always |)',
            '2': 'Encoding Characters',
            '3': 'Sending Application',
            '4': 'Sending Facility',
            '5': 'Receiving Application',
            '6': 'Receiving Facility',
            '7': 'Date/Time of Message',
            '8': 'Security',
            '9': 'Message Type',
            '10': 'Message Control ID',
            '11': 'Processing ID',
            '12': 'Version ID',
            '13': 'Sequence Number',
            '14': 'Continuation Pointer',
            '15': 'Accept Acknowledgment Type',
            '16': 'Application Acknowledgment Type',
            '17': 'Country Code',
            '18': 'Character Set',
            '19': 'Principal Language Of Message',
            '20': 'Alternate Character Set Handling Scheme',
            '21': 'Message Profile Identifier',
            '22': 'Sending Responsible Organization',
            '23': 'Receiving Responsible Organization',
            '24': 'Sending Network Address',
            '25': 'Receiving Network Address'
        },
        'EVN': {
            '1': 'Event Type Code',
            '2': 'Recorded Date/Time',
            '3': 'Date/Time Planned Event',
            '4': 'Event Reason Code',
            '5': 'Operator ID',
            '6': 'Event Occurred',
            '7': 'Event Facility'
        },
        'PID': {
            '1': 'Set ID - PID',
            '2': 'Patient ID',
            '3': 'Patient Identifier List',
            '4': 'Alternate Patient ID - PID',
            '5': 'Patient Name',
            '6': "Mother's Maiden Name",
            '7': 'Date/Time of Birth',
            '8': 'Administrative Sex',
            '9': 'Patient Alias',
            '10': 'Race',
            '11': 'Patient Address',
            '12': 'County Code',
            '13': 'Phone Number - Home',
            '14': 'Phone Number - Business',
            '15': 'Primary Language',
            '16': 'Marital Status',
            '17': 'Religion',
            '18': 'Patient Account Number',
            '19': 'SSN Number - Patient',
            '20': "Driver's License Number - Patient",
            '21': "Mother's Identifier",
            '22': 'Ethnic Group',
            '23': 'Birth Place',
            '24': 'Multiple Birth Indicator',
            '25': 'Birth Order',
            '26': 'Citizenship',
            '27': 'Veterans Military Status',
            '28': 'Nationality',
            '29': 'Patient Death Date and Time',
            '30': 'Patient Death Indicator',
            '31': 'Identity Unknown Indicator',
            '32': 'Identity Reliability Code',
            '33': 'Last Update Date/Time',
            '34': 'Last Update Facility',
            '35': 'Taxonomic Classification Code',
            '36': 'Breed Code',
            '37': 'Strain',
            '38': 'Production Class Code',
            '39': 'Tribal Citizenship',
            '40': 'Patient Telecommunication Information'
        },
        'PV1': {
            '1': 'Set ID - PV1',
            '2': 'Patient Class',
            '3': 'Assigned Patient Location',
            '4': 'Admission Type',
            '5': 'Preadmit Number',
            '6': 'Prior Patient Location',
            '7': 'Attending Doctor',
            '8': 'Referring Doctor',
            '9': 'Consulting Doctor',
            '10': 'Hospital Service',
            '11': 'Temporary Location',
            '12': 'Preadmit Test Indicator',
            '13': 'Re-admission Indicator',
            '14': 'Admit Source',
            '15': 'Ambulatory Status',
            '16': 'VIP Indicator',
            '17': 'Admitting Doctor',
            '18': 'Patient Type',
            '19': 'Visit Number',
            '20': 'Financial Class',
            '21': 'Charge Price Indicator',
            '22': 'Courtesy Code',
            '23': 'Credit Rating',
            '24': 'Contract Code',
            '25': 'Contract Effective Date',
            '26': 'Contract Amount',
            '27': 'Contract Period',
            '28': 'Interest Code',
            '29': 'Transfer to Bad Debt Code',
            '30': 'Transfer to Bad Debt Date',
            '31': 'Bad Debt Agency Code',
            '32': 'Bad Debt Transfer Amount',
            '33': 'Bad Debt Recovery Amount',
            '34': 'Delete Account Indicator',
            '35': 'Delete Account Date',
            '36': 'Discharge Disposition',
            '37': 'Discharged to Location',
            '38': 'Diet Type',
            '39': 'Servicing Facility',
            '40': 'Bed Status',
            '41': 'Account Status',
            '42': 'Pending Location',
            '43': 'Prior Temporary Location',
            '44': 'Admit Date/Time',
            '45': 'Discharge Date/Time',
            '46': 'Current Patient Balance',
            '47': 'Total Charges',
            '48': 'Total Adjustments',
            '49': 'Total Payments',
            '50': 'Alternate Visit ID',
            '51': 'Visit Indicator',
            '52': 'Other Healthcare Provider',
            '53': 'Service Episode Description',
            '54': 'Service Episode Identifier'
        },
        'NK1': {
            '1': 'Set ID - NK1',
            '2': 'Name',
            '3': 'Relationship',
            '4': 'Address',
            '5': 'Phone Number',
            '6': 'Business Phone Number',
            '7': 'Contact Role',
            '8': 'Start Date',
            '9': 'End Date',
            '10': 'Next of Kin / Associated Parties Job Title',
            '11': 'Next of Kin / Associated Parties Job Code/Class',
            '12': 'Next of Kin / Associated Parties Employee Number',
            '13': 'Organization Name - NK1',
            '14': 'Marital Status',
            '15': 'Administrative Sex',
            '16': 'Date/Time of Birth',
            '17': 'Living Dependency',
            '18': 'Ambulatory Status',
            '19': 'Citizenship',
            '20': 'Primary Language',
            '21': 'Living Arrangement',
            '22': 'Publicity Code',
            '23': 'Protection Indicator',
            '24': 'Student Indicator',
            '25': 'Religion',
            '26': "Mother's Maiden Name",
            '27': 'Nationality',
            '28': 'Ethnic Group',
            '29': 'Contact Reason',
            '30': "Contact Person's Name",
            '31': "Contact Person's Telephone Number",
            '32': "Contact Person's Address",
            '33': "Next of Kin/Associated Party's Identifiers",
            '34': 'Job Status',
            '35': 'Race',
            '36': 'Handicap',
            '37': 'Contact Person Social Security Number',
            '38': 'Next of Kin Birth Place',
            '39': 'VIP Indicator',
            '40': 'Next of Kin Telecommunication Information',
            '41': "Contact Person's Telecommunication Information"
        },
        'OBR': {
            '1': 'Set ID - OBR',
            '2': 'Placer Order Number',
            '3': 'Filler Order Number',
            '4': 'Universal Service Identifier',
            '5': 'Priority',
            '6': 'Requested Date/Time',
            '7': 'Observation Date/Time #',
            '8': 'Observation End Date/Time #',
            '9': 'Collection Volume *',
            '10': 'Collector Identifier *',
            '11': 'Specimen Action Code *',
            '12': 'Danger Code',
            '13': 'Relevant Clinical Information',
            '14': 'Specimen Received Date/Time',
            '15': 'Specimen Source',
            '16': 'Ordering Provider',
            '17': 'Order Callback Phone Number',
            '18': 'Placer Field 1',
            '19': 'Placer Field 2',
            '20': 'Filler Field 1 +',
            '21': 'Filler Field 2 +',
            '22': 'Results Rpt/Status Chng - Date/Time +',
            '23': 'Charge to Practice +',
            '24': 'Diagnostic Serv Sect ID',
            '25': 'Result Status +',
            '26': 'Parent Result +',
            '27': 'Quantity/Timing',
            '28': 'Result Copies To',
            '29': 'Parent Results Observation Identifier',
            '30': 'Transportation Mode',
            '31': 'Reason for Study',
            '32': 'Principal Result Interpreter +',
            '33': 'Assistant Result Interpreter +',
            '34': 'Technician +',
            '35': 'Transcriptionist +',
            '36': 'Scheduled Date/Time +',
            '37': 'Number of Sample Containers *',
            '38': 'Transport Logistics of Collected Sample *',
            '39': "Collector's Comment *",
            '40': 'Transport Arrangement Responsibility',
            '41': 'Transport Arranged',
            '42': 'Escort Required',
            '43': 'Planned Patient Transport Comment',
            '44': 'Procedure Code',
            '45': 'Procedure Code Modifier',
            '46': 'Placer Supplemental Service Information',
            '47': 'Filler Supplemental Service Information',
            '48': 'Medically Necessary Duplicate Procedure Reason',
            '49': 'Result Handling',
            '50': 'Parent Universal Service Identifier',
            '51': 'Observation Group ID',
            '52': 'Parent Observation Group ID',
            '53': 'Alternate Placer Order Number',
            '54': 'Parent Order'
        },
        'OBX': {
            '1': 'Set ID - OBX',
            '2': 'Value Type',
            '3': 'Observation Identifier',
            '4': 'Observation Sub-ID',
            '5': 'Observation Value',
            '6': 'Units',
            '7': 'References Range',
            '8': 'Interpretation Codes',
            '9': 'Probability',
            '10': 'Nature of Abnormal Test',
            '11': 'Observation Result Status',
            '12': 'Effective Date of Reference Range',
            '13': 'User Defined Access Checks',
            '14': 'Date/Time of the Observation',
            '15': "Producer's ID",
            '16': 'Responsible Observer',
            '17': 'Observation Method',
            '18': 'Equipment Instance Identifier',
            '19': 'Date/Time of the Analysis',
            '20': 'Observation Site',
            '21': 'Observation Instance Identifier',
            '22': 'Mood Code',
            '23': 'Performing Organization Name',
            '24': 'Performing Organization Address',
            '25': 'Performing Organization Medical Director',
            '26': 'Patient Results Release Category',
            '27': 'Root Cause',
            '28': 'Local Process Control'
        }
    }

    # ADT Event Codes
    ADT_CODES = {
        'A01': 'Admit/visit notification',
        'A02': 'Transfer a patient',
        'A03': 'Discharge/end visit',
        'A04': 'Register a patient',
        'A05': 'Pre-admit a patient',
        'A06': 'Change an outpatient to an inpatient',
        'A07': 'Change an inpatient to an outpatient',
        'A08': 'Update patient information',
        'A09': 'Patient departing - tracking',
        'A10': 'Patient arriving - tracking',
        'A11': 'Cancel admit/visit notification',
        'A12': 'Cancel transfer',
        'A13': 'Cancel discharge/end visit',
        'A14': 'Pending admit',
        'A15': 'Pending transfer',
        'A16': 'Pending discharge',
        'A17': 'Swap patients',
        'A18': 'Merge patient information',
        'A19': 'Patient query',
        'A20': 'Bed status update',
        'A21': 'Patient goes on a leave of absence',
        'A22': 'Patient returns from a leave of absence',
        'A23': 'Delete a patient record',
        'A24': 'Link patient information',
        'A25': 'Cancel pending discharge',
        'A26': 'Cancel pending transfer',
        'A27': 'Cancel pending admit',
        'A28': 'Add person information',
        'A29': 'Delete person information',
        'A30': 'Merge person information',
        'A31': 'Update person information',
        'A32': 'Cancel patient arriving - tracking',
        'A33': 'Cancel patient departing - tracking',
        'A34': 'Merge patient information - patient ID only',
        'A35': 'Merge patient information - account number only',
        'A36': 'Merge patient information - patient ID and account number',
        'A37': 'Unlink patient information',
        'A38': 'Cancel pre-admit',
        'A39': 'Merge person - patient ID',
        'A40': 'Merge patient - patient identifier list',
        'A41': 'Merge account - patient account number',
        'A42': 'Merge visit - visit number',
        'A43': 'Move patient information - patient identifier list',
        'A44': 'Move account information - patient account number',
        'A45': 'Move visit information - visit number',
        'A46': 'Change patient ID',
        'A47': 'Change patient identifier list',
        'A48': 'Change alternate patient ID',
        'A49': 'Change patient account number',
        'A50': 'Change visit number',
        'A51': 'Change alternate visit ID',
        'A52': 'Cancel leave of absence for a patient',
        'A53': 'Cancel patient returns from a leave of absence',
        'A54': 'Change attending doctor',
        'A55': 'Cancel change attending doctor',
        'A60': 'Update allergy information',
        'A61': 'Change consulting doctor',
        'A62': 'Cancel change consulting doctor'
    }

    # HL7 Parser implementation (from src/parser/hl7_parser.py)
    class HL7Parser:
        """Parser for HL7 messages."""
        
        def __init__(self):
            """Initialize the parser."""
            self.message_text = ""
            self.segments = []
            self.raw_message = None
            
        def parse_text(self, message_text):
            """Parse an HL7 message from text input."""
            self.message_text = message_text.strip()
            self.raw_message = message_text
            return self.parse_message(message_text)
            
        def parse_file(self, file_path):
            """Parse an HL7 message from file path."""
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                return self.parse_message(content)
            except Exception as e:
                raise ValueError(f"Failed to read or parse file: {str(e)}")
            
        def parse_message(self, message_text):
            """Parse an HL7 message and return the segment structure."""
            self.message_text = message_text
            self.segments = []
            
            # Split the message into segments (lines)
            lines = message_text.strip().splitlines()
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Extract segment name (first 3 characters)
                segment_name = line[:3] if len(line) >= 3 else "???"
                
                # Extract fields
                fields = []
                if "|" in line:
                    # Split by pipe character
                    parts = line.split("|")
                    
                    # Special handling for MSH segment
                    if segment_name == "MSH":
                        # MSH-1 is the field separator character (|)
                        fields.append({
                            "value": "|",
                            "components": [{
                                "value": "|",
                                "subcomponents": []
                            }]
                        })
                        
                        # Process the remaining fields with proper indexing
                        for i, part in enumerate(parts):
                            # Skip the segment name (already handled)
                            if i == 0:
                                continue
                                
                            # Add the field with components
                            self._add_field_with_components(fields, part)
                    else:
                        # For non-MSH segments, first part is segment name, skip it
                        for i, part in enumerate(parts):
                            if i == 0:
                                continue
                                
                            # Add the field with components
                            self._add_field_with_components(fields, part)
                
                # Add segment to the list
                self.segments.append({
                    "name": segment_name,
                    "content": line,
                    "fields": fields
                })
            
            return self.segments
            
        def _add_field_with_components(self, fields, field_value):
            """Helper method to add a field with its components to the fields list."""
            components = []
            if "^" in field_value:
                # Split by caret for components
                comp_parts = field_value.split("^")
                for comp in comp_parts:
                    # Handle subcomponents
                    if "&" in comp:
                        subcomps = comp.split("&")
                        components.append({
                            "value": comp,
                            "subcomponents": subcomps
                        })
                    else:
                        components.append({
                            "value": comp,
                            "subcomponents": []
                        })
            else:
                # No components, just the field
                components.append({
                    "value": field_value,
                    "subcomponents": []
                })
            
            fields.append({
                "value": field_value,
                "components": components
            })
        
        def get_structure(self):
            """Return hierarchical structure of the parsed message."""
            if not self.segments:
                return None
                
            # Create the message structure
            result = {
                'name': 'Message',
                'value': "",  # No value for the root element
                'description': "HL7 Message",
                'children': []
            }
            
            # Add segments as children
            for segment in self.segments:
                segment_node = self._create_segment_node(segment)
                result['children'].append(segment_node)
                
            return result
            
        def _create_segment_node(self, segment):
            """Create a segment node with its fields."""
            segment_name = segment['name']
            
            # Get segment description
            description = HL7_SEGMENTS.get(segment_name, f"Unknown Segment ({segment_name})")
            
            segment_node = {
                'name': segment_name,
                'value': segment['content'],
                'description': description,
                'children': []
            }
            
            # Add fields as children
            for i, field in enumerate(segment['fields']):
                # Get the correct field number (MSH segment is special)
                field_num = str(i+1)
                
                # Create field node
                field_node = self._create_field_node(segment_name, field_num, field)
                segment_node['children'].append(field_node)
                
            return segment_node
            
        def _create_field_node(self, segment_name, field_num, field):
            """Create a field node with its components."""
            # Format field name as 'MSH-1', 'PID-3', etc.
            field_name = f"{segment_name}-{field_num}"
            
            # Get field description
            description = ""
            if segment_name in HL7_FIELDS and field_num in HL7_FIELDS[segment_name]:
                description = HL7_FIELDS[segment_name][field_num]
            else:
                description = f"Field {field_num}"
                
            # Special handling for MSH-9 (Message Type) field
            if segment_name == 'MSH' and field_num == '9' and "^" in field["value"]:
                # Try to extract the message type and trigger event
                parts = field["value"].split("^")
                if len(parts) >= 2 and parts[0] == "ADT":
                    event_code = parts[1]
                    if event_code in ADT_CODES:
                        description += f" - {ADT_CODES[event_code]}"
            
            field_node = {
                'name': field_name,
                'value': field['value'],
                'description': description,
                'children': []
            }
            
            # Add components as children
            for j, component in enumerate(field['components']):
                comp_name = f"{field_name}.{j+1}"
                comp_node = {
                    'name': comp_name,
                    'value': component['value'],
                    'description': f"Component {j+1}",
                    'children': []
                }
                
                # Add subcomponents
                for k, subcomp in enumerate(component['subcomponents']):
                    if k > 0:  # Skip first subcomponent (already included in component)
                        subcomp_name = f"{comp_name}.{k+1}"
                        subcomp_node = {
                            'name': subcomp_name,
                            'value': subcomp,
                            'description': f"Subcomponent {k+1}",
                            'children': []
                        }
                        comp_node['children'].append(subcomp_node)
                
                field_node['children'].append(comp_node)
                
            return field_node
            
        @property
        def message(self):
            return self.raw_message

    # Tree Model for displaying HL7 messages (from src/gui/tree_model.py)
    class HL7TreeModel(QStandardItemModel):
        """Tree model for displaying HL7 message structure."""
        
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setHorizontalHeaderLabels(["Element", "Description", "Value"])
            
        def populate_from_message(self, message_structure):
            """
            Populate the tree model from parsed HL7 message structure.
            
            This is different from the old implementation that took segments directly.
            The new implementation expects a hierarchical structure from parser.get_structure().
            """
            self.clear()
            self.setHorizontalHeaderLabels(["Element", "Description", "Value"])
            
            # Get the message structure
            if not isinstance(message_structure, dict):
                # If not a dict, assume it's segments and return
                print("Error: Expected message structure but received:", type(message_structure))
                return
            else:
                structure = message_structure
                
            # Create root item with empty value as expected
            root_item = QStandardItem(structure['name'])
            desc_item = QStandardItem(structure['description'])
            value_item = QStandardItem(structure['value'])  # This should be empty for the root
            
            # Add root item to model
            self.appendRow([root_item, desc_item, value_item])
            
            # Process all children (segments) recursively
            self._populate_children(root_item, structure['children'])
            
        def _populate_children(self, parent_item, children):
            """Recursively populate the tree with children items."""
            for child in children:
                # Create items for this child
                name_item = QStandardItem(child['name'])
                desc_item = QStandardItem(child['description'])
                value_item = QStandardItem(child['value'] if child['value'] else "")
                
                # Add this child to its parent
                parent_item.appendRow([name_item, desc_item, value_item])
                
                # Process this child's children recursively
                if child['children']:
                    self._populate_children(name_item, child['children'])

    # Main application window (from src/gui/main_window.py)
    class MainWindow(QMainWindow):
        """Main window for the HL7 Parser application."""
        
        def __init__(self):
            super().__init__()
            
            # Create parser
            self.parser = HL7Parser()
            
            # Settings for the application
            self.settings = QSettings("HL7Parser", "hl7parser")
            
            # Setup UI
            self.setup_ui()
            
            # Set window properties
            self.setWindowTitle("HL7 Parser")
            self.resize(
                self.settings.value("window_width", 1000, type=int),
                self.settings.value("window_height", 800, type=int)
            )
            
        def setup_ui(self):
            """Set up the user interface."""
            # Central widget
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            
            # Main layout
            main_layout = QVBoxLayout(central_widget)
            
            # Create splitter for resizable sections
            splitter = QSplitter(Qt.Orientation.Vertical)
            main_layout.addWidget(splitter)
            
            # Top section: Input area
            input_widget = QWidget()
            input_layout = QVBoxLayout(input_widget)
            
            # Input label
            input_label = QLabel("Enter or paste HL7 message:")
            input_layout.addWidget(input_label)
            
            # Input text area
            self.input_text = QTextEdit()
            self.input_text.setPlaceholderText("Paste HL7 message here...")
            input_layout.addWidget(self.input_text)
            
            # Button layout
            button_layout = QHBoxLayout()
            
            # Parse button
            parse_button = QPushButton("Parse Message")
            parse_button.clicked.connect(self.parse_message)
            button_layout.addWidget(parse_button)
            
            # Open file button
            open_button = QPushButton("Open File...")
            open_button.clicked.connect(self.open_file)
            button_layout.addWidget(open_button)
            
            # Clear button
            clear_button = QPushButton("Clear")
            clear_button.clicked.connect(self.clear_input)
            button_layout.addWidget(clear_button)
            
            input_layout.addLayout(button_layout)
            
            # Add input widget to splitter
            splitter.addWidget(input_widget)
            
            # Bottom section: Tree view
            tree_widget = QWidget()
            tree_layout = QVBoxLayout(tree_widget)
            
            # Tree view label
            tree_label = QLabel("Message Structure:")
            tree_layout.addWidget(tree_label)
            
            # Tree view
            self.tree_view = QTreeView()
            self.tree_view.setAlternatingRowColors(True)
            self.tree_view.setSelectionMode(QTreeView.SelectionMode.SingleSelection)
            self.tree_view.setEditTriggers(QTreeView.EditTrigger.NoEditTriggers)
            self.tree_view.setExpandsOnDoubleClick(True)
            
            # Tree model
            self.tree_model = HL7TreeModel()
            self.tree_view.setModel(self.tree_model)
            
            # Copy button
            copy_button = QPushButton("Copy Selected Value")
            copy_button.clicked.connect(self.copy_selected_value)
            
            # Export button
            export_button = QPushButton("Export to File...")
            export_button.clicked.connect(self.export_to_file)
            
            # Button layout for tree view
            tree_button_layout = QHBoxLayout()
            tree_button_layout.addWidget(copy_button)
            tree_button_layout.addWidget(export_button)
            
            tree_layout.addWidget(self.tree_view)
            tree_layout.addLayout(tree_button_layout)
            
            # Add tree widget to splitter
            splitter.addWidget(tree_widget)
            
            # Set initial splitter sizes
            splitter.setSizes([int(self.height() * 0.4), int(self.height() * 0.6)])
            
            # Restore column widths
            self.tree_view.setColumnWidth(0, self.settings.value("col0_width", 200, type=int))
            self.tree_view.setColumnWidth(1, self.settings.value("col1_width", 200, type=int))
            self.tree_view.setColumnWidth(2, self.settings.value("col2_width", 400, type=int))
        
        def parse_message(self):
            """Parse the HL7 message from the input text area."""
            message_text = self.input_text.toPlainText().strip()
            if not message_text:
                QMessageBox.warning(self, "Empty Message", "Please enter an HL7 message to parse.")
                return
            
            try:
                # Parse the message using the parse_text method
                self.parser.parse_text(message_text)
                
                # Get the structure and populate the tree model
                structure = self.parser.get_structure()
                if structure:
                    self.tree_model.populate_from_message(structure)
                    
                    # Expand the first level
                    self.tree_view.expandToDepth(0)
                else:
                    QMessageBox.warning(self, "Error", "No structure was generated from the message.")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error parsing message: {str(e)}")
                traceback.print_exc()
        
        def open_file(self):
            """Open an HL7 message file."""
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Open HL7 File", "", "HL7 Files (*.hl7 *.txt);;All Files (*.*)"
            )
            
            if file_path:
                try:
                    # Parse the file directly using the parser
                    self.parser.parse_file(file_path)
                    
                    # Update the text area with the file contents
                    with open(file_path, 'r', encoding='utf-8') as f:
                        message_text = f.read()
                        self.input_text.setPlainText(message_text)
                    
                    # Get the structure and populate the tree model
                    structure = self.parser.get_structure()
                    if structure:
                        self.tree_model.populate_from_message(structure)
                        
                        # Expand the first level
                        self.tree_view.expandToDepth(0)
                    else:
                        QMessageBox.warning(self, "Error", "No structure was generated from the file.")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Error opening file: {str(e)}")
        
        def clear_input(self):
            """Clear the input text area and reset the tree view."""
            self.input_text.clear()
            self.tree_model.clear()
            self.tree_model.setHorizontalHeaderLabels(["Element", "Description", "Value"])
        
        def copy_selected_value(self):
            """Copy the selected tree item's value to the clipboard."""
            indexes = self.tree_view.selectedIndexes()
            if indexes and len(indexes) >= 3:
                # The value is in the third column
                value = indexes[2].data()
                if value:
                    # Copy to clipboard
                    clipboard = QApplication.clipboard()
                    clipboard.setText(value)
                    # Show status message
                    self.statusBar().showMessage("Value copied to clipboard", 2000)
        
        def export_to_file(self):
            """Export the parsed message to a file."""
            if not self.parser.segments:
                QMessageBox.warning(self, "No Data", "Parse a message first before exporting.")
                return
            
            # Make a filename suggestion based on message content or timestamp
            suggested_filename = "hl7_message"
            if self.parser.segments and len(self.parser.segments) > 0:
                # Try to use MSH-10 (Message Control ID) if available
                for segment in self.parser.segments:
                    if segment["name"] == "MSH" and len(segment["fields"]) >= 10:
                        control_id = segment["fields"][9]["value"]
                        if control_id:
                            suggested_filename = f"hl7_message_{control_id}"
                            break
            
            if suggested_filename == "hl7_message":
                # No control ID found, use timestamp
                suggested_filename = f"hl7_message_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Export Message", suggested_filename, "HL7 Files (*.hl7);;Text Files (*.txt);;All Files (*.*)"
            )
            
            if file_path:
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(self.parser.message_text)
                    QMessageBox.information(self, "Export Successful", f"Message exported to {file_path}")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Error exporting file: {str(e)}")
        
        def closeEvent(self, event):
            """Save settings when the window is closed."""
            # Save window size
            self.settings.setValue("window_width", self.width())
            self.settings.setValue("window_height", self.height())
            
            # Save column widths
            self.settings.setValue("col0_width", self.tree_view.columnWidth(0))
            self.settings.setValue("col1_width", self.tree_view.columnWidth(1))
            self.settings.setValue("col2_width", self.tree_view.columnWidth(2))
            
            event.accept()

    # Main function
    def main():
        """Main entry point for the application."""
        print("Starting HL7Parser application...")
        app = QApplication(sys.argv)
        main_window = MainWindow()
        main_window.show()
        sys.exit(app.exec())

    # This allows the script to be executed directly, or imported
    if __name__ == "__main__":
        main()
    # Make MainWindow available for import from main.py fallback
    else:
        # Export these for the fallback mechanism in main.py
        from PyQt6.QtWidgets import QApplication

except Exception as e:
    if getattr(sys, 'frozen', False):
        # Show error in GUI if possible
        error_details = f"Error: {str(e)}\n\n{traceback.format_exc()}"
        try:
            from PyQt6.QtWidgets import QApplication, QMessageBox
            app = QApplication(sys.argv)
            QMessageBox.critical(None, "HL7 Parser Error", 
                f"Error starting HL7 Parser:\n\n{str(e)}\n\nCheck the log file for details.")
        except:
            # If we can't show GUI error, write to file
            try:
                with open("hl7parser_error.log", "w") as f:
                    f.write(error_details)
            except:
                pass
    # Re-raise for non-frozen app
    raise