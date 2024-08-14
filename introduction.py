import streamlit as st
from helpers import load_lottie_url, get_color_theme
from streamlit_lottie import st_lottie

def show_page():
    st.title("Football Analysis App")
    st.markdown("""
    Welcome to the Football Analysis App! Explore detailed statistics and insights about teams and players.
    """)

    # Horizontal color theme selection
    st.markdown("### Choose your color theme:")
    
    # Define the available color themes
    color_palettes = ["Primary", "Single Color", "Diverging"]

    # Display radio buttons for selecting a color theme
    selected_palette = st.radio(
        label="",
        options=color_palettes,
        horizontal=True
    )

    # Store the theme selection in session state
    st.session_state['theme'] = selected_palette

    # Display selected color palette in a small, subtle way
    color_theme = get_color_theme(selected_palette)
    st.markdown(
        "".join(
            f'<span style="background-color: {color}; height: 20px; width: 20px; display: inline-block; margin-right: 5px; border-radius: 3px;"></span>'
            for color in color_theme
        ),
        unsafe_allow_html=True,
    )

    # Display a larger Lottie animation at the bottom
    lottie_url = "https://lottie.host/89057c52-70ef-444e-952c-988c03e80a6a/KvI0AtqNdI.json"  # Use a football bouncing animation URL
    lottie_data = load_lottie_url(lottie_url)
    if lottie_data:
        st_lottie(lottie_data, height=400, key="intro_lottie", quality="high", speed=0.8)

