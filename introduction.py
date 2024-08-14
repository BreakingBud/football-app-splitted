import streamlit as st
from streamlit_lottie import st_lottie
import requests

# Function to load Lottie animation from URL
def load_lottie_url(url: str):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Lottie animation not found.")
        return None

def show_page():
    st.title("Football Analysis App")
    st.markdown("""
    Welcome to the Football Analysis App! Explore detailed statistics and insights about football matches.
    Please select your preferred color theme from the options below and navigate through the app using the menu.
    """)

    # Horizontal color theme selection with smaller palette preview
    st.markdown("### Choose your color theme:")
    
    color_palettes = {
        "Primary": ["#4285F4", "#34A853", "#FBBC05", "#EA4335"],
        "Single Color": ["#1f77b4", "#00509E", "#003F88", "#002A5E"],  # Blue shades
        "Diverging": ["#E69F00", "#56B4E9", "#009E73", "#F0E442"]
    }

    selected_palette = st.radio(
        label="",
        options=list(color_palettes.keys()),
        horizontal=True
    )

    # Store the theme selection in session state
    st.session_state['theme'] = selected_palette

    # Display selected color palette in a small, subtle way
    st.markdown("### Selected Color Palette:")
    cols = st.columns(len(color_palettes[selected_palette]))
    for idx, color in enumerate(color_palettes[selected_palette]):
        cols[idx].markdown(f'<div style="background-color: {color}; height: 20px; width: 20px; border-radius: 50%;"></div>', unsafe_allow_html=True)

    # Display a Lottie animation at the bottom right corner
    lottie_url = "https://assets5.lottiefiles.com/packages/lf20_YXD37q.json"
    lottie_data = load_lottie_url(lottie_url)
    if lottie_data:
        st_lottie(lottie_data, height=150, key="intro_lottie", quality="high", speed=0.8)

    # Display a brief description of the app
    st.markdown("""
    This application provides an in-depth analysis of football matches. 
    You can compare teams head-to-head, analyze individual match statistics, and review team performance.
    Use the sidebar to navigate between different analysis pages.
    """)

