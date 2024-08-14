import streamlit as st
import importlib

# Set up the app configuration
st.set_page_config(
    page_title="Football Analysis App",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Page mappings
pages = {
    "Introduction": "introduction",
    "Head-to-Head Analysis": "head_to_head",
    "Player-to-Player Analysis": "player_analysis",
    "Choropleth Map": "choropleth_map"
}

def load_page(page_name):
    try:
        module = importlib.import_module(pages[page_name])
        return module.show_page
    except ModuleNotFoundError:
        st.error(f"Module for page '{page_name}' not found.")
        return None

def main():
    st.sidebar.title("Navigation")
    selected_page = st.sidebar.radio("Choose a page", list(pages.keys()))

    # Load and show the selected page
    page_function = load_page(selected_page)
    if page_function:
        page_function()

if __name__ == "__main__":
    main()
