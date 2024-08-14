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

# Color theme selection
theme = st.sidebar.selectbox(
    "Choose your color theme",
    ["Primary Color", "Single Color", "Color Blind"]
)

# Store the theme selection in session state
st.session_state['theme'] = theme

# Display color palette preview in the sidebar
def display_palette_preview(theme):
    import plotly.colors as pc

    color_palettes = {
        "Primary Color": pc.qualitative.Plotly,
        "Single Color": ['#1f77b4', '#1f77b4', '#1f77b4', '#1f77b4'],  # Blue shades
        "Color Blind": pc.qualitative.Set1
    }

    palette = color_palettes.get(theme, pc.qualitative.Plotly)
    st.sidebar.subheader("Color Palette Preview")

    if len(palette) > 0:
        for color in palette:
            st.sidebar.markdown(f'<div style="background-color: {color}; height: 15px; width: 100%; border-radius: 5px;"></div>', unsafe_allow_html=True)

# Show color palette preview
display_palette_preview(st.session_state.get('theme', "Primary Color"))

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
