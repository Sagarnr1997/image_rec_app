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

def initialize_client():
    key_path = "path/to/your/service_account_key.json"
    credentials = service_account.Credentials.from_service_account_file(key_path)
    return vision.ImageAnnotatorClient(credentials=credentials)

# Function to recognize faces in an uploaded image using Google Cloud Vision API
def recognize_faces(uploaded_file):
    try:
        # Read the content of the uploaded file
        content = uploaded_file.read()

        # Perform face detection
        image_content = vision.Image(content=io.BytesIO(content).read())
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

            # Mark rectangle above the face
            x, y = bounds[0]  # Top-left corner of the bounding box
            draw.rectangle([(x, y - 20), (x + 100, y)], fill='red')
            draw.text((x, y - 20), "Face", fill="white")

        # Save the image with rectangles marked around faces
        marked_image_path = 'marked_faces.jpg'
        image_pil.save(marked_image_path)
        return marked_image_path
    except Exception as e:
        st.error(f"Error processing image: {e}")
        return None

# Function to retrieve image files from Google Drive
def list_image_files():
    # Your code to list image files from Google Drive
    pass

# Main function
def main():
    global client
    client = initialize_client()

    st.title("Face Recognition App")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)
        detected_faces = recognize_faces(uploaded_file)
        if detected_faces:
            st.write("Detected Faces:")
            st.json(detected_faces)

            # List image files from Google Drive
            drive_images = list_image_files()

            # Compare detected faces with faces from Google Drive
            matching_images = []
            for drive_image in drive_images:
                # Your code to compare detected_faces with faces from Google Drive
                # You may use facial recognition algorithms or other techniques
                # to determine if a detected face matches a face in the drive
                pass

            if matching_images:
                st.write("Matching Faces from Google Drive:")
                for matching_image in matching_images:
                    st.image(matching_image, caption='Matching Face', use_column_width=True)
            else:
                st.write("No matching faces found in Google Drive.")
        else:
            st.write("No faces detected in the uploaded image.")
    else:
        st.write("Please upload an image to recognize faces.")

if __name__ == "__main__":
    main()
