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
    url = "https://github.com/Sagarnr1997/Image_app/blob/main/imapp_new.json?raw=true"
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
        # Read the content of the uploaded file
        content = uploaded_file.read()

        # Perform face detection
        image_content = vision.Image(content=content)
        response = client.face_detection(image=image_content)
        faces = response.face_annotations

        # Load the original image using PIL for drawing rectangles
        image_pil = Image.open(io.BytesIO(content))
        draw = ImageDraw.Draw(image_pil)

        # Draw rectangles around detected faces
        for face in faces:
            vertices = face.bounding_poly.vertices
            bounds = [(vertex.x, vertex.y) for vertex in vertices]
            draw.rectangle(bounds, outline='red')

            # Calculate the position for marking rectangle above the face
            x, y = bounds[0][0], bounds[0][1]  # Top-left corner of the bounding box
            width, height = bounds[1][0] - bounds[0][0], bounds[3][1] - bounds[0][1]

            # Draw rectangle above the face
            draw.rectangle([(x, y - 20), (x + width, y)], fill='red')
            draw.text((x, y - 20), "Face", fill="white")

        # Save the image with rectangles marked around faces
        marked_image_path = 'marked_faces.jpg'
        image_pil.save(marked_image_path)
        return marked_image_path
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
