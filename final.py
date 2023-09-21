import streamlit as st
import cv2
import pytesseract
import tempfile
import os
import numpy as np
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import re
import pandas as pd
import pymongo

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Sample data for training the SVM model (you need to replace this with your labeled data)
# ...

# Create a connection to MongoDB
mongo_client = pymongo.MongoClient("mongodb+srv://comptition:Adi@#vasu0006@cluster0.a87ri9o.mongodb.net/")
db = mongo_client["database_name"]
collection = db["collection_name"]

data = [
    {"text": "1234567890", "label": "identification_number"},
    {"text": "DL No. : ABC1234567 1234", "label": "identification_number"},
    {"text": "Civil Case No. 1234/5678", "label": "civil_case_number"},
    {"text": "VA-123", "label": "case_identifier"},
    {"text": "Aff-456", "label": "case_identifier"},
    {"text": "APL-789", "label": "case_identifier"},
    {"text": "Evidence ID-987", "label": "evidence_identifier"},
    {"text": "Witness ID-A123", "label": "witness_identifier"},
    {"text": "Order No. 123/5678", "label": "order_number"},
    {"text": "BB-1234-567", "label": "case_identifier"},
    {"text": "CS-1234-567", "label": "case_identifier"},
    {"text": "CD-123", "label": "case_identifier"},
    {"text": "MP-1234-567", "label": "case_identifier"},
    {"text": "CA-1234-567", "label": "case_identifier"},
    {"text": "ER-1234-567", "label": "case_identifier"},
    {"text": "PIL No. 123/5678", "label": "case_identifier"},
    {"text": "Motion No. AB-123", "label": "motion_number"},
    {"text": "Adjournment Application - AA-1234-567", "label": "adjournment_application"},
    {"text": "EA-1234-567", "label": "case_identifier"},
    {"text": "LN-1234-567", "label": "case_identifier"},
    {"text": "SA-1234-567", "label": "case_identifier"},
    {"text": "RA-1234-567", "label": "case_identifier"},
    {"text": "CC-1234-567", "label": "case_identifier"},
    {"text": "MA-1234-567", "label": "case_identifier"},
    {"text": "Case No. XYZ 1234", "label": "case_number"},
    {"text": "Suit No. 1234/5678", "label": "suit_number"},
    {"text": "Writ Petition No. 1234/5678", "label": "writ_petition_number"},
    {"text": "Criminal Case No. ABC 1234", "label": "criminal_case_number"},
    {"text": "Appeal No. 123", "label": "appeal_number"},
    {"text": "Revision Petition No. DEF 1234", "label": "revision_petition_number"},
    {"text": "ID ABC1234567 1234567890", "label": "identification_number"},
    {"text": "Adhar Card No. 123456789012", "label": "aadhar_card_number"},
    {"text": "PAN Card No. ABCDE1234F", "label": "pan_card_number"},
    {"text": "FIR No. XYZ/123/2023", "label": "fir_number"},
    {"text": "Complaint No. 1234/5678", "label": "complaint_number"},
    {"text": "Suit for Declaration", "label": "suit_declaration"},
    {"text": "Petition for Divorce", "label": "petition_divorce"},
    {"text": "Ruling in Case No. XYZ 1234", "label": "ruling_case_number"},
    {"text": "Order of High Court", "label": "order_high_court"},
    {"text": "Judgment dated 01/12/2023", "label": "judgment_date"},
    {"text": "01/12/2023", "label": "date_format"},
    {"text": "1-12-2023", "label": "date_format"},
    {"text": "Registered Office: ABC Law Firm", "label": "registered_office"},
    {"text": "Advocate Mr. John Doe", "label": "advocate_name"},
    {"text": "Aadhar Card No. 123456789012", "label": "aadhar_card_number"},
    {"text": "PAN Card No. ABCDE1234F", "label": "pan_card_number"},
    {"text": "Voter ID No. ABCDE1234F", "label": "voter_id_number"},
    {"text": "Passport No. P12345678", "label": "passport_number"},
    {"text": "GSTIN No. 12ABCDE3456F7G8", "label": "gstin_number"},
    {"text": "EPIC No. ABCDE1234F", "label": "epic_number"},
    {"text": "IFSC Code: ABCD1234567", "label": "ifsc_code"},
    {"text": "MICR Code: 123456789", "label": "micr_code"},
    {"text": "UPC Code: 0A1B2C3D", "label": "upc_code"},
    {"text": "ESIC No. 1234567890", "label": "esic_number"},
    {"text": "TIN No. AB123456789012", "label": "tin_number"},
    {"text": "UAN No. 123456789012", "label": "uan_number"},
    {"text": "IMEI No. 123456789012345", "label": "imei_number"},
    {"text": "SIM No. 12345678901234567890", "label": "sim_number"},
    {"text": "Certificate | . 1N-KA178944269060915", "label": "certificate_number"},
]

# Convert the labeled data into a DataFrame
df = pd.DataFrame(data)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df["text"], df["label"], test_size=0.2, random_state=42)

# Create TF-IDF vectors from the text data
vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Train an SVM classifier
svm_classifier = SVC(kernel="linear")
svm_classifier.fit(X_train_tfidf, y_train)

# Define regular expression patterns for identification numbers using RE2
identification_patterns = [
      # Patterns for unique identification numbers
    r'\b\d{10}\b',                     # Matches 10-digit numbers
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
    r'Permanent Account Number Card\. [A-Z]{5}\d{4}[A-Z]',# PAN Card No.ABCDE1234F
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
    # Patterns for Indian government document identification numbers
    r'Aadhar Card No\. \d{12}',          # Aadhar Card No. 123456789012 (12-digit)
    r'PAN Card No\. [A-Z]{5}\d{4}[A-Z]', # PAN Card No. ABCDE1234F
    r'Voter ID No\. [A-Z0-9]{10}',       # Voter ID No. ABCDE1234F
    r'Passport No\. [A-Z0-9]+\d+',       # Passport No. P12345678 (Alphanumeric)
    r'GSTIN No\. [0-9A-Z]{15}',          # GSTIN No. 12ABCDE3456F7G8 (15-character)
    r'EPIC No\. [A-Z0-9]{10}',           # EPIC No. ABCDE1234F (10-character)
    r'IFSC Code: [A-Z]{4}\d{7}',         # IFSC Code: ABCD1234567
    r'MICR Code: \d{9}',                 # MICR Code: 123456789
    r'UPC Code: [0-9A-F]+',              # UPC Code: 0A1B2C3D
    r'ESIC No\. \d{10}',                 # ESIC No. 1234567890 (10-digit)
    r'TIN No\. [A-Z]{2}\d{11}',          # TIN No. AB123456789012 (13-character)
    r'UAN No\. \d{12}',                  # UAN No. 123456789012 (12-digit)
    r'IMEI No\. \d{15}',                 # IMEI No. 123456789012345 (15-digit)
    r'SIM No\. \d{20}',                  # SIM No. 12345678901234567890 (20-digit)
    r'Certificate \| \. \d+[A-Z]-[A-Z]+\d+', # Certificate | . 1N-KA178944269060915
    # Add more patterns as needed
]

# ...

def main():
    st.title("Text and Identification Number Extractor with Patterns")

    uploaded_image = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

    if uploaded_image:
        st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
        st.write("Extracted Text:")
        st.write("Please wait while we process the image...")

        # Save the uploaded image to a temporary file
        temp_img = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        temp_img.write(uploaded_image.read())
        temp_img_path = temp_img.name

        # Close the temporary file to release the resource
        temp_img.close()

        # Extract text, patterns, and classify identification numbers when the user uploads an image
        text, extracted_text, classified_identification_numbers = extract_identification_numbers(temp_img_path)

        # Display the extracted text
        st.write(text)

        # Display the extracted identification numbers
        st.write("Extracted Identification Numbers:")
        st.write(extracted_text)

        # Display the classified identification numbers
        st.write("Classified Identification Numbers:")
        for i, segment in enumerate(classified_identification_numbers, 1):
            st.write(f"{i}. Text: {segment['text']}, Classification: {segment['classification']}")

        # Store the extracted numbers and image data in MongoDB
        image_data = open(temp_img_path, 'rb').read()
        extracted_numbers = [segment['text'] for segment in classified_identification_numbers]

        data_to_insert = {
            "image_path": temp_img_path,
            "extracted_numbers": extracted_numbers,
            "image_data": image_data
        }
        collection.insert_one(data_to_insert)

        # Create a button to download the extracted text and classified numbers as a PDF file
        if st.button("Download as PDF"):
            pdf_filename = "extracted_data.pdf"
            doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
            styles = getSampleStyleSheet()
            style = styles["Normal"]
            elements = []

            # Add detected sentences to the PDF
            sentences = text.split('\n\n')
            for sentence in sentences:
                p = Paragraph(sentence, style)
                elements.append(p)

            # Add classified identification numbers to the PDF
            for segment in classified_identification_numbers:
                p = Paragraph(f"Text: {segment['text']}, Classification: {segment['classification']}", style)
                elements.append(p)

            doc.build(elements)
            st.success(f"[Download PDF]({pdf_filename})")

        # Remove the temporary image file after closing it
        os.remove(temp_img_path)

if __name__ == "__main__":
    main()
