import streamlit as st

def show_page():
    st.title("Football Analysis App")
    st.markdown("""
    Welcome to the Football Analysis App! Here you can explore various statistics and insights about football matches.

    Use the sidebar to navigate through different sections of the app and select your preferred color theme.
    The selected theme will be applied to all the visualizations throughout the app.
    """)

    # Display a Lottie animation to make the introduction more engaging
    st_lottie_url = "https://assets5.lottiefiles.com/packages/lf20_YXD37q.json"  # Example football Lottie animation URL
    st_lottie(st_lottie_url, height=300, key="intro_lottie")

    # Display a preview of the color themes
    st.markdown("### Color Theme Preview")

    # Define color palettes
    color_palettes = {
        "Primary": ["#4285F4", "#34A853", "#FFBB33", "#FF5733", "#AB47BC"],  # Google colors
        "Single Color": ["#1f77b4"],  # Monochromatic blue
        "Viridis": ["#440154", "#3b528b", "#21908d", "#5dc863", "#fde725"]  # Viridis colormap
    }

    selected_theme = st.session_state.get('theme', 'Primary')
    theme_colors = color_palettes.get(selected_theme, color_palettes["Primary"])

    # Display color palette
    st.write(f"**{selected_theme} Theme Preview:**")
    st.write("Here’s a preview of the selected color theme. All visualizations will use these colors.")
    st.write("###")

    # Display sample color palette
    for color in theme_colors:
        st.markdown(f'<div style="background-color:{color}; width:100px; height:30px; display:inline-block; margin:5px;"></div>', unsafe_allow_html=True)

# Function to display Lottie animations
def st_lottie(url: str, height: int, key: str):
    import requests
    from streamlit_lottie import st_lottie

    response = requests.get(url)
    if response.status_code != 200:
        return None
    return st_lottie(response.json(), height=height, key=key)
