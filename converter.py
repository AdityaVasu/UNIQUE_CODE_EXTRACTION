import pymongo
import bson
from PIL import Image
import streamlit as st
from io import BytesIO
impo

# Connect to MongoDB (replace with your MongoDB URI)
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["comp"]  # Change "image_db" to your database name
collection = db["images"]

# Streamlit app
st.title("Image Storage and Display")

# Function to store an image in MongoDB
def store_image(image, image_id):
    image_bytes = BytesIO()
    image.save(image_bytes, format="JPEG")
    image_data = image_bytes.getvalue()
    
    # Store the image data in MongoDB with a primary key (_id)
    collection.update_one({"_id": image_id}, {"$set": {"image_data": bson.Binary(image_data)}}, upsert=True)

# Function to retrieve and display an image from MongoDB
def display_image(image_id):
    result = collection.find_one({"_id": image_id})
    if result and "image_data" in result:
        image_data = result["image_data"]
        image = Image.open(BytesIO(image_data))
        st.image(image, caption="Stored Image", use_column_width=True)
    else:
        st.warning("Image not found.")

# Main Streamlit app
if st.button("Upload Image"):
    uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_image is not None:
        image_id = bson.ObjectId()
        store_image(uploaded_image, image_id)
        st.success("Image uploaded and stored with ID: " + str(image_id))

# Display image by ID
display_id = st.text_input("Enter Image ID:")
if display_id:
    display_image(bson.ObjectId(display_id))