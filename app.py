import streamlit as st
import importlib
from constants import PAGE_TITLES
from data_loader import load_data

# Set up the app configuration
st.set_page_config(
    page_title="Football Analysis App",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load the data
goalscorers_df, results_df, shootouts_df = load_data()

# Sidebar for navigation
st.sidebar.title("Navigation")
selected_page = st.sidebar.radio("Go to", list(PAGE_TITLES.keys()))

# Load the selected page as a module and display it
page_module = PAGE_TITLES[selected_page]
module = importlib.import_module(page_module)
module.show_page(results_df)
