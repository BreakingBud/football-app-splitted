import streamlit as st
import importlib
import plotly.express as px
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

# Color palette options
color_palettes = {
    "Primary": ["#4285F4", "#34A853", "#FFBB33", "#FF4B4B"],
    "Single Color (Blue)": ["#1f77b4"],
    "Viridis": px.colors.sequential.Viridis
}

# Function to display a small color preview
def display_palette_preview(palette):
    # Display color previews directly in Streamlit
    st.write("Color Palette Preview:")
    for color in palette:
        st.markdown(f'<div style="background-color: {color}; height: 30px; width: 100%;"></div>', unsafe_allow_html=True)

# Sidebar for color theme selection
theme = st.sidebar.selectbox(
    "Choose your color theme",
    options=list(color_palettes.keys())
)

# Store the theme selection in session state
st.session_state['theme'] = theme

# Display color palette preview in sidebar
st.sidebar.subheader("Color Palette Preview")
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
