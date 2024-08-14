import streamlit as st
import zipfile
import os

# Set up the app configuration
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

# File uploader for the user to upload the zip file
uploaded_file = st.sidebar.file_uploader("Upload your data.zip file", type="zip")

if uploaded_file is not None:
    # Path to extract the zip file
    extracted_path = 'extracted_data'

    # Extract the uploaded zip file
    with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
        zip_ref.extractall(extracted_path)

    # Load the selected page as a module
    page = pages[selected_page]
    exec(open(f"{page}.py").read())

else:
    st.sidebar.warning("Please upload the data.zip file to proceed.")
