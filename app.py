import streamlit as st
import importlib
from constants import PAGE_TITLES

# Set up the app configuration
st.set_page_config(
    page_title="Football Analysis App",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar for navigation
st.sidebar.title("Navigation")
selected_page = st.sidebar.radio("Go to", list(PAGE_TITLES.keys()))

# Load the selected page as a module and display it
page_module = PAGE_TITLES[selected_page]
module = importlib.import_module(page_module)
module.show_page()
