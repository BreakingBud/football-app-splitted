import streamlit as st
import importlib
from data_loader import load_data

# Set up the app configuration
st.set_page_config(
    page_title="Football Analysis App",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load data
goalscorers_df, results_df, shootouts_df = load_data()

# Sidebar for navigation and theme selection
st.sidebar.title("Navigation")
pages = {
    "Introduction": "intro",
    "Head-to-Head Analysis": "head_to_head",
    "Player-to-Player Analysis": "player_analysis",
    "Choropleth Map": "choropleth_map"
}

# Theme selection
theme = st.sidebar.selectbox(
    "Choose your color theme",
    ["Primary", "Single Color", "Diverging"]
)

# Store the theme selection in session state
st.session_state['theme'] = theme

# Display color palette preview
def display_palette_preview(palette):
    for color in palette:
        st.sidebar.markdown(f'<div style="background-color:{color}; width: 30px; height: 30px; display: inline-block;"></div>', unsafe_allow_html=True)

color_palettes = {
    "Primary": ["#4285F4", "#34A853", "#FBBC05", "#FF0000"],  # Google colors
    "Single Color": ["#1f77b4", "#1f77b4", "#1f77b4", "#1f77b4"],  # Monochromatic blue
    "Diverging": ["#FF0000", "#FF8000", "#00FF00", "#0000FF"]  # Diverging colors
}

if theme in color_palettes:
    display_palette_preview(color_palettes[theme])

# Radio buttons for page selection
selected_page = st.sidebar.radio("Go to", list(pages.keys()))

# Load the selected page as a module using importlib
module = importlib.import_module(pages[selected_page])

# Pass the relevant data to each page
if selected_page == "Head-to-Head Analysis":
    module.show_page(results_df)
elif selected_page == "Player-to-Player Analysis":
    module.show_page(goalscorers_df)
elif selected_page == "Choropleth Map":
    module.show_page(results_df)
else:
    module.show_page()
