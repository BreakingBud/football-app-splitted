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
    "Introduction": "introduction",
    "Head-to-Head Analysis": "head_to_head",
    "Player-to-Player Analysis": "player_analysis",
    "Choropleth Map": "choropleth_map"
}

# Define color palettes
color_palettes = {
    "Primary": ["#4285F4", "#EA4335", "#FBBC05", "#34A853"],  # Google colors
    "Single Color (Blue)": ["#1f77b4"],  # Monochromatic blue palette
    "Viridis": px.colors.sequential.Viridis
}

# Theme selection
theme = st.sidebar.selectbox(
    "Choose your color theme",
    list(color_palettes.keys())
)

# Store the theme selection in session state
st.session_state['theme'] = theme

# Display the selected color palette
st.sidebar.markdown("### Selected Color Palette")
st.sidebar.write(color_palettes[theme])

# Radio buttons for page selection
selected_page = st.sidebar.radio("Go to", list(pages.keys()))

# Load the selected page as a module using importlib
module = importlib.import_module(pages[selected_page])

# Pass the relevant data to each page
if selected_page == "Head-to-Head Analysis":
    module.show_page(results_df, color_palettes)
elif selected_page == "Player-to-Player Analysis":
    module.show_page(goalscorers_df, color_palettes)
elif selected_page == "Choropleth Map":
    module.show_page(results_df, color_palettes)
else:
    module.show_page()
