import streamlit as st
from PIL import Image
import os
from google.oauth2 import service_account
from google.cloud import vision_v1
from google.cloud.vision_v1  import types
from googleapiclient.discovery import build
from io import BytesIO

# Function to perform facial recognition using Google Cloud Vision API
def recognize_faces(uploaded_file):
    """
    Detect faces in the input image using Google Cloud Vision API.

    Args:
        uploaded_file (UploadedFile): The uploaded image file.

    Returns:
        list: List of dictionaries containing bounding box coordinates of detected faces.
    """
    client = vision_v1.ImageAnnotatorClient()

    # Convert the uploaded file to a PIL Image object
    image = Image.open(io.BytesIO(uploaded_file.read()))

    # Resize the image to reduce payload size
    resized_image = image.resize((image.width // 2, image.height // 2))
    img_byte_arr = resized_image.tobytes()
    image_content = vision_v1.Image(content=img_byte_arr)

    response = client.face_detection(image=image_content)
    faces = response.face_annotations

    face_data = []
    for face in faces:
        vertices = face.bounding_poly.vertices
        bounds = [{'x': vertex.x, 'y': vertex.y} for vertex in vertices]
        face_data.append(bounds)

    return face_data
# Function to retrieve image files from Google Drive
def list_image_files():
    # Your code to list image files from Google Drive
    pass

# Main function
def main():
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
