import streamlit as st
import importlib

# Set up the app configuration
st.set_page_config(
    page_title="Football Analysis App",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Define available pages and their module names
pages = {
    "Introduction": "introduction",
    "Head-to-Head Analysis": "head_to_head",
    "Player-to-Player Analysis": "player_analysis",
    "Choropleth Map": "choropleth_map"
}

def main():
    st.sidebar.title("Football Analysis App")
    selected_page = st.sidebar.radio("Choose a page", list(pages.keys()))

    # Load and show the selected page
    module = importlib.import_module(pages[selected_page])
    module.show_page()

if __name__ == "__main__":
    main()
