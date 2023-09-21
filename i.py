import cv2
import pytesseract
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
import re  # Import the 're' module for regular expressions

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Load the image
img = cv2.imread('image.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Set the configuration for sentence extraction
custom_config = r'--oem 3 --psm 6'

# Extract complete sentences
detected_text = pytesseract.image_to_string(img, config=custom_config)

# Define regular expression patterns for specific identification numbers
# Add more patterns as needed
# Define all the patterns
patterns = [
    # Patterns for unique identification numbers
    r'\b\d{12}\b',                     # Matches 10-digit numbers
    r'DL No\. : [A-Z0-9]+\s\d{4,}',    # DL No. : 
    r'Civil Case No\. \d{4}/\d{4}',    # Civil Case No. 1234/5678
    r'VA-\d+',                          # VA-123
    r'Aff-\d+',                         # Aff-456
    r'APL-\d+',                         # APL-789
    r'Evidence ID-\d+',                 # Evidence ID-987
    r'Witness ID-[A-Z]\d+',             # Witness ID-A123
    r'Order No\. \d{3}/\d{4}',          # Order No. 123/5678
    r'BB-\d{4}-\d{3}',                  # BB-1234-567
    r'CS-\d{4}-\d{3}',                  # CS-1234-567
    r'CD-\d+',                          # CD-123
    r'MP-\d{4}-\d{3}',                  # MP-1234-567
    r'CA-\d{4}-\d{3}',                  # CA-1234-567
    r'ER-\d{4}-\d{3}',                  # ER-1234-567
    r'PIL No\. \d{3}/\d{4}',            # PIL No. 123/5678
    r'Motion No\. [A-Z]{2}-\d{3}',      # Motion No. AB-123
    r'Adjournment Application - AA-\d{4}-\d{3}',  # Adjournment Application - AA-1234-567
    r'EA-\d{4}-\d{3}',                  # EA-1234-567
    r'LN-\d{4}-\d{3}',                  # LN-1234-567
    r'SA-\d{4}-\d{3}',                  # SA-1234-567
    r'RA-\d{4}-\d{3}',                  # RA-1234-567
    r'CC-\d{4}-\d{3}',                  # CC-1234-567
    r'MA-\d{4}-\d{3}',                  # MA-1234-567

    # Patterns for other court-related identifiers and information
    r'Case No\. [A-Z0-9]+\s\d{4,}',      # Case No. XYZ 1234
    r'Suit No\. \d{4}/\d{4}',           # Suit No. 1234/5678
    r'Writ Petition No\. \d{4}/\d{4}',  # Writ Petition No. 1234/5678
    r'Criminal Case No\. [A-Z]+\s\d{4}',# Criminal Case No. ABC 1234
    r'Appeal No\. \d+',                 # Appeal No. 123
    r'Revision Petition No\. [A-Z]+\s\d{4}', # Revision Petition No. DEF 1234
    r'ID [A-Z0-9]+\s\d{10}',            # ID ABC1234567 1234567890
    r'Adhar Card No\. \d{12}',          # Adhar Card No. 123456789012
    r'PAN Card No\. [A-Z]{5}\d{4}[A-Z]',# PAN Card No. ABCDE1234F
    r'FIR No\. [A-Z]{3}/\d{3}/\d{4}',   # FIR No. XYZ/123/2023
    r'Complaint No\. \d{4}/\d{4}',      # Complaint No. 1234/5678
    r'Suit for Declaration',            # Suit for Declaration
    r'Petition for Divorce',            # Petition for Divorce
    r'Ruling in Case No\. [A-Z0-9]+\s\d{4,}',  # Ruling in Case No. XYZ 1234
    r'Order of [A-Z]+\sCourt',         # Order of High Court
    r'Judgment dated \d{2}/\d{2}/\d{4}', # Judgment dated 01/12/2023
    r'\d{2}/\d{2}/\d{4}',               # Date in DD/MM/YYYY format
    r'\d{1,2}-\d{1,2}-\d{4}',           # Date in D-M-YYYY format
    r'Registered Office: [A-Za-z\s]+', # Registered Office: ABC Law Firm
    r'Advocate [A-Za-z\s]+',            # Advocate Mr. John Doe
]

# Create a list to store extracted identification numbers
extracted_identification_numbers = []

# Find and extract identification numbers from the detected text
for pattern in patterns:
    identification_numbers = re.findall(pattern, detected_text)
    extracted_identification_numbers.extend(identification_numbers)

# Split the text into sentences based on double newline characters ("\n\n")
split_sentences = [sentence.strip() for sentence in detected_text.split('\n\n') if sentence.strip()]

# Create a PDF document using ReportLab
pdf_filename = "detected_sentences.pdf"
doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

styles = getSampleStyleSheet()
style = styles["Normal"]

# Define a list to hold the Paragraph elements
elements = []

# Write the detected sentences to the PDF
for sentence in split_sentences:
    p = Paragraph(sentence, style)
    elements.append(p)

# Write the extracted identification numbers to the PDF
for identification_number in extracted_identification_numbers:
    p = Paragraph(identification_number, style)
    elements.append(p)

# Build the PDF document
doc.build(elements)

print(f"PDF file '{pdf_filename}' created.")