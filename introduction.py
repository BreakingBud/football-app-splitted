import streamlit as st
from streamlit_lottie import st_lottie
import requests

# Function to load Lottie animation
def load_lottie_url(url: str):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Lottie animation not found.")
            return None
    except requests.RequestException as e:
        st.error(f"Request error: {e}")
        return None

def show_page():
    st.title("Football Analysis App")
    st.markdown("""
    Welcome to the Football Analysis App! Here you can explore various statistics and insights about football matches.

    Before you begin, please select your preferred color theme:
    """)

    # Color theme selection
    theme = st.selectbox(
        "Choose your color theme",
        ["Primary Color", "Single Color", "Color Blind"]
    )

    # Store the theme selection in session state
    st.session_state['theme'] = theme

    # Display a Lottie animation
    lottie_url = "https://assets5.lottiefiles.com/packages/lf20_YXD37q.json"
    lottie_data = load_lottie_url(lottie_url)
    if lottie_data:
        st_lottie(lottie_data, height=300, key="intro_lottie")

    # Display color palettes
    st.sidebar.title("Color Palette Preview")
    color_palettes = {
        "Primary Color": ["#4285F4", "#34A853", "#FBBC05", "#EA4335"],
        "Single Color": ["#009688", "#00796B", "#004D40", "#00251A"],
        "Color Blind": ["#E69F00", "#56B4E9", "#009E73", "#F0E442"]
    }
    
    if 'theme' in st.session_state:
        theme = st.session_state['theme']
    else:
        theme = "Primary Color"

    def display_palette_preview(colors):
        for color in colors:
            st.markdown(f'<div style="background-color: {color}; width: 100px; height: 30px; margin: 5px; display: inline-block;"></div>', unsafe_allow_html=True)

    st.sidebar.subheader("Color Palette Preview")
    display_palette_preview(color_palettes[theme])
