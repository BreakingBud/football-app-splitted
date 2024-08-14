import streamlit as st
from helpers import load_lottie_url, get_color_theme
from streamlit_lottie import st_lottie

def show_page():
    st.title("Football Analysis App")
    st.markdown("""
    Welcome to the Football Analysis App! Explore detailed statistics and insights about teams and players.
    Please select your preferred color theme from the options below and navigate through the app using the menu.
    """)

    # Horizontal color theme selection with smaller palette preview
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
    st.markdown("### Selected Color Palette:")
    color_theme = get_color_theme(selected_palette)
    cols = st.columns(len(color_theme))
    for idx, color in enumerate(color_theme):
        cols[idx].markdown(f'<div style="background-color: {color}; height: 30px; width: 30px; border-radius: 5px;"></div>', unsafe_allow_html=True)

    # Display a Lottie animation at the bottom right corner
    lottie_url = "https://assets5.lottiefiles.com/packages/lf20_YXD37q.json"
    lottie_data = load_lottie_url(lottie_url)
    if lottie_data:
        st.markdown(
            f"""
            <div style="position: fixed; bottom: 0px; right: 0px;">
                {st_lottie(lottie_data, height=100, key="intro_lottie", quality="high", speed=0.8)}
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Display a brief description of the app
    st.markdown("""
    This application provides an in-depth analysis of football matches. 
    You can compare teams head-to-head, analyze individual match statistics, and review team performance.
    Use the sidebar to navigate between different analysis pages.
    """)

