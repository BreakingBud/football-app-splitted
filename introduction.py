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

# Function to display Lottie animations
def st_lottie(url: str, height: int, key: str):
    import requests
    from streamlit_lottie import st_lottie

    response = requests.get(url)
    if response.status_code != 200:
        return None
    return st_lottie(response.json(), height=height, key=key)
