import streamlit as st
from helpers import load_lottie_url, get_color_theme

def show_page():
    st.title("Football Analysis App")
    st.markdown("""
    Welcome to the Football Analysis App! Explore detailed statistics and insights about teams and players.
    Please select your preferred color theme from the options below and navigate through the app using the menu.
    """)

    # Horizontal color theme selection with smaller palette preview
    st.markdown("### Choose your color theme:")
    selected_palette = st.radio(
        label="",
        options=list(get_color_theme(None).keys()),
        horizontal=True
    )

    # Store the theme selection in session state
    st.session_state['theme'] = selected_palette

    # Display selected color palette in a small, subtle way
    st.markdown("### Selected Color Palette:")
    cols = st.columns(len(get_color_theme(selected_palette)))
    for idx, color in enumerate(get_color_theme(selected_palette)):
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
