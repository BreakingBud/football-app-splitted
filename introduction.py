import streamlit as st
from helpers import load_lottie_url

def show_page():
    st.title("Football Analysis App")
    st.markdown("Welcome to the Football Analysis App! Explore detailed statistics and insights about teams and players.")

    # Horizontal color theme selection
    st.markdown("### Choose your color theme:")
    color_palettes = ["Primary", "Single Color", "Diverging"]
    selected_palette = st.radio("", options=color_palettes, horizontal=True)

    # Store the theme selection in session state
    st.session_state['theme'] = selected_palette

    # Display the selected color palette in a small, subtle way
    st.markdown("### Selected Color Palette:")
    color_theme = get_color_theme(selected_palette)
    st.markdown(
        "".join(
            f'<span style="background-color: {color}; height: 20px; width: 20px; display: inline-block; margin-right: 5px; border-radius: 3px;"></span>'
            for color in color_theme
        ),
        unsafe_allow_html=True,
    )

    # Display a larger Lottie animation at the bottom
    lottie_url = "https://lottie.host/de4d9a89-99eb-4afc-8507-2475c4edfd56/4mwcHwmWjR.json"  # Use a football bouncing animation URL
    lottie_data = load_lottie_url(lottie_url)
    if lottie_data:
        st_lottie(lottie_data, height=400, key="intro_lottie", quality="high", speed=0.8)
