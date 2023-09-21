import streamlit as st
import cv2
import pytesseract
import tempfile
import os
import torch
import torchvision.transforms as transforms
from PIL import Image
import numpy as np

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def extract_text_and_numbers(image):
    # Extract text using Tesseract
    text = pytesseract.image_to_string(image)

    # Function to find unique numbers in the extracted text
    def find_unique_numbers(text):
        numbers = []
        for word in text.split():
            try:
                number = float(word)
                if number.is_integer():
                    numbers.append(int(number))
            except ValueError:
                pass
        return list(set(numbers))

    unique_numbers = find_unique_numbers(text)

    # Here, you can implement a CNN-based OCR model using PyTorch and torchvision.
    # Replace the following placeholder code with your actual CNN model.
    # You'll need to load your trained model and perform OCR using it.
    cnn_ocr_output = "Replace this with your CNN-based OCR output"

    return text, unique_numbers, cnn_ocr_output

def main():
    st.title("Text and Unique Number Extractor with CNN")

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

        # Open the uploaded image with OpenCV
        img = cv2.imread(temp_img_path)

        # Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Create a PIL Image from the grayscale image
        image = Image.fromarray(gray)

        # Extract text, unique numbers, and CNN-based OCR output
        text, unique_numbers, cnn_ocr_output = extract_text_and_numbers(image)

        # Display the extracted text
        st.write(text)

        # Display the unique numbers found in the text
        st.write("Unique Numbers:")
        st.write(unique_numbers)

        # Display the CNN-based OCR output (replace with your actual output)
        st.write("CNN-based OCR Output:")
        st.write(cnn_ocr_output)

        # Create a button to download the extracted text and CNN-based OCR output as a PDF file
        if st.button("Download as PDF"):
            pdf_filename = "extracted_data.pdf"
            # Create a PDF containing the extracted text, unique numbers, and OCR output
            # You can use a PDF generation library like ReportLab or FPDF for this task.

            st.success(f"[Download PDF]({pdf_filename})")

        # Remove the temporary image file after closing it
        os.remove(temp_img_path)

if __name__ == "__main__":
    main()
