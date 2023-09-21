import streamlit as st
import cv2
import pytesseract
import tempfile
import os
import re
import numpy as np
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import pandas as pd

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Extended list of patterns for Indian government document identification numbers
identification_patterns = [
    # ... (previous patterns)

    # Patterns for Indian government document identification numbers
    r'Aadhar Card No\. \d{12}',          # Aadhar Card No. 123456789012 (12-digit)
    r'PAN Card No\. [A-Z]{5}\d{4}[A-Z]', # PAN Card No. ABCDE1234F
    # Add a custom pattern for the format "RIDXXXXXXXXXXX" (X represents a digit)
    r'RID\d{11}',  # Custom pattern for "RIDXXXXXXXXXXX"

    # Add more patterns as needed
]

# Sample data for training the SVM model with Indian government document identification numbers
sample_data = [
    {"text": "1234567890", "label": "identification_number"},
    {"text": "DL No. : ABC1234567 1234", "label": "identification_number"},
    {"text": "Aadhar Card No. 123456789012", "label": "aadhar_card_number"},
    {"text": "PAN Card No. ABCDE1234F", "label": "pan_card_number"},
    {"text": "Voter ID No. ABCDE1234F", "label": "identification_number"},
    {"text": "Passport No. P12345678", "label": "identification_number"},
    {"text": "GSTIN No. 12ABCDE3456F7G8", "label": "identification_number"},
    {"text": "EPIC No. ABCDE1234F", "label": "identification_number"},
    {"text": "IFSC Code: ABCD1234567", "label": "identification_number"},
    {"text": "MICR Code: 123456789", "label": "identification_number"},
    {"text": "UPC Code: 0A1B2C3D", "label": "identification_number"},
    {"text": "ESIC No. 1234567890", "label": "identification_number"},
    {"text": "TIN No. AB123456789012", "label": "identification_number"},
    {"text": "UAN No. 123456789012", "label": "identification_number"},
    {"text": "IMEI No. 123456789012345", "label": "identification_number"},
    {"text": "SIM No. 12345678901234567890", "label": "identification_number"},
    {"text": "Some other text", "label": "other"},
    # Add more labeled examples here
]

# Convert the sample data into a DataFrame
df = pd.DataFrame(sample_data)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df["text"], df["label"], test_size=0.2, random_state=42)

# Create TF-IDF vectors from the text data
vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Train an SVM classifier
svm_classifier = SVC(kernel="linear")
svm_classifier.fit(X_train_tfidf, y_train)

# Function to extract identification numbers from an image
def extract_identification_numbers(img_path):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    custom_config = r'--oem 3 --psm 6'
    detected_text = pytesseract.image_to_string(img, config=custom_config)

    # Define regular expression patterns for identification numbers using RE2
    identification_numbers = re.findall(r'\b\d{10}\b', detected_text)

    # Classify each extracted text segment using the SVM classifier
    classified_identification_numbers = []
    for text_segment in identification_numbers:
        tfidf_vector = vectorizer.transform([text_segment])
        classification = svm_classifier.predict(tfidf_vector)[0]
        if classification == "identification_number":
            classified_identification_numbers.append(text_segment)

    return detected_text, classified_identification_numbers

# Function to extract Aadhar card and PAN card numbers
def extract_aadhar_pan_numbers(img_path):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    custom_config = r'--oem 3 --psm 6'
    detected_text = pytesseract.image_to_string(img, config=custom_config)

    # Extract Aadhar card numbers using pattern
    aadhar_numbers = re.findall(r'Aadhar Card No\. \d{12}', detected_text)

    # Extract PAN card numbers using pattern
    pan_numbers = re.findall(r'PAN Card No\. [A-Z]{5}\d{4}[A-Z]', detected_text)

    return detected_text, aadhar_numbers, pan_numbers

# Streamlit UI
def main():
    st.title("Document Text and Number Extractor")

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

        # Extract text and classified identification numbers
        text, identification_numbers = extract_identification_numbers(temp_img_path)

        # Extract Aadhar card and PAN card numbers
        text, aadhar_numbers, pan_numbers = extract_aadhar_pan_numbers(temp_img_path)

        # Display the extracted text
        st.write(text)

        # Display the classified identification numbers
        if identification_numbers:
            st.write("Classified Identification Numbers:")
            for i, id_number in enumerate(identification_numbers, 1):
                st.write(f"{i}. {id_number}")

        # Display the extracted Aadhar card numbers
        if aadhar_numbers:
            st.write("Aadhar Card Numbers:")
            for i, aadhar_number in enumerate(aadhar_numbers, 1):
                st.write(f"{i}. {aadhar_number}")

        # Display the extracted PAN card numbers
        if pan_numbers:
            st.write("PAN Card Numbers:")
            for i, pan_number in enumerate(pan_numbers, 1):
                st.write(f"{i}. {pan_number}")

        # Create a button to download the extracted text and numbers as a PDF file
        if st.button
