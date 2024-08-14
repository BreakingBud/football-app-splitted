import streamlit as st
import zipfile
import os

# Path to the uploaded zip file and extraction directory
uploaded_zip_file = 'data.zip'
extracted_path = 'extracted_data'

# Check if the zip file exists
if not os.path.exists(uploaded_zip_file):
    st.error(f"The file {uploaded_zip_file} was not found. Please upload the file and try again.")
else:
    # Extract the zip file if it exists
    if not os.path.exists(extracted_path):
        with zipfile.ZipFile(uploaded_zip_file, 'r') as zip_ref:
            zip_ref.extractall(extracted_path)

    # Set up the Streamlit app configuration
    st.set_page_config(
        page_title="Football Analysis App",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    pages = {
        "Introduction": "introduction",
        "Head-to-Head Analysis": "head_to_head",
        "Player-to-Player Analysis": "player_analysis",
        "Choropleth Map": "choropleth_map",
        "World Cup 2026 Prediction": "predict_wc"
    }

    # Radio buttons for page selection
    selected_page = st.sidebar.radio("Go to", list(pages.keys()))

    # Load the selected page as a module
    page = pages[selected_page]
    exec(open(f"{page}.py").read())
