import streamlit as st
import importlib
from constants import PAGE_TITLES

# Set up the app configuration
st.set_page_config(
    page_title="Football Analysis App",
    layout="wide",
    initial_sidebar_state="expanded",
)

def main():
    st.sidebar.title("Football Analysis App")
    selected_page = st.sidebar.radio("Choose a page", list(PAGE_TITLES.keys()))

    # Load and show the selected page
    module = importlib.import_module(PAGE_TITLES[selected_page])
    module.show_page()

if __name__ == "__main__":
    main()
