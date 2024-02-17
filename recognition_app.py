import streamlit as st
from PIL import Image, ImageDraw
import os
from google.oauth2 import service_account
from google.cloud import vision
from google.cloud import vision_v1
from google.cloud.vision_v1  import types
from googleapiclient.discovery import build
import io
from io import BytesIO
import requests

# Function to download the JSON file from the given URL and store it locally
def download_json_file(url, output_path):
    response = requests.get(url)
    with open(output_path, 'w') as json_file:
        json_file.write(response.text)

# Path to store the downloaded JSON file
json_file_path = "imapp.json"

# Download the JSON file if it does not exist
if not os.path.exists(json_file_path):
    url = "https://github.com/Sagarnr1997/Image_app/blob/main/imapp.json?raw=true"
    download_json_file(url, json_file_path)

# Initialize the Google Cloud Vision client
def initialize_client():
    try:
        credentials = service_account.Credentials.from_service_account_file(json_file_path)
        return vision.ImageAnnotatorClient(credentials=credentials)
    except Exception as e:
        st.error(f"Error initializing client: {e}")
        return None

# Function to recognize faces in an uploaded image using Google Cloud Vision API
def recognize_faces(uploaded_file, client):
    try:
        # Your face recognition code here
        pass
    except Exception as e:
        st.error(f"Error processing image: {e}")
        return None

# Main function
def main():
    # Initialize the client
    client = initialize_client()

    if client is not None:
        st.title("Face Recognition App")
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Image', use_column_width=True)
            detected_faces = recognize_faces(uploaded_file, client)
            if detected_faces:
                st.write("Detected Faces:")
                st.json(detected_faces)
            else:
                st.write("No faces detected in the uploaded image.")
        else:
            st.write("Please upload an image to recognize faces.")
    else:
        st.write("Failed to initialize client. Please check service account credentials and ensure billing is enabled.")

if __name__ == "__main__":
    main()
