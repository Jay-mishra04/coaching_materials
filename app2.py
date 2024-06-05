import streamlit as st
import os
import fitz  # PyMuPDF
from PIL import Image

# Function to list all PDF files in a directory
def list_pdfs(directory):
    return [f for f in os.listdir(directory) if f.endswith('.pdf')]

# Function to extract the first page of a PDF as an image
def get_first_page_image(pdf_path):
    doc = fitz.open(pdf_path)
    page = doc.load_page(0)
    pix = page.get_pixmap()
    image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    return image

# Main function to create the Streamlit app
def main():
    st.title("Welcome to Your Physics Learning Hub")
    st.subheader("Enhance your knowledge with curated materials")
    
    # Sidebar with photo and qualifications
    # st.sidebar.image("your_photo.jpg", use_column_width=True)
    st.sidebar.write("### Mritunjay Mishra")
    st.sidebar.write("M.Sc. in Physics")
    st.sidebar.write("Physics Teacher")
    st.sidebar.write("Aspiring Data Scientist")

    # Form for student details
    st.markdown("### Please fill in your details")
    with st.form(key='student_form'):
        name = st.text_input("Enter your name")
        phone_number = st.text_input("Enter your phone number")
        class_selected = st.selectbox("Select your class", ["Class 9", "Class 10", "Class 11", "Class 12"])
        submit_button = st.form_submit_button(label='Submit')

    # Display materials based on class selection
    if submit_button:
        st.write(f"Welcome, {name}! Here are the materials for {class_selected}:")

        # Directory based on class selection
        class_directories = {
            "Class 9": "class_9_materials",
            "Class 10": "class_10_materials",
            "Class 11": "class_11_materials",
            "Class 12": "class_12_materials"
        }
        directory = class_directories[class_selected]
        pdfs = list_pdfs(directory)

        # Display PDF previews and download links in a grid
        cols = st.columns(4)  # Create 4 columns
        for i, pdf in enumerate(pdfs):
            pdf_path = os.path.join(directory, pdf)
            image = get_first_page_image(pdf_path)
            # Resize image to fit in a column
            resized_image = image.resize((150, 200))
            
            with cols[i % 4]:  # Arrange images in grid
                st.image(resized_image, caption=pdf, use_column_width=True)
                with open(pdf_path, "rb") as file:
                    btn = st.download_button(
                        label="Download",
                        data=file,
                        file_name=pdf,
                        mime='application/octet-stream'
                    )

if __name__ == '__main__':
    main()
