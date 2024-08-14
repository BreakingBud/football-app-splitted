import streamlit as st
from streamlit_lottie import st_lottie
import requests

def st_lottie(url: str, height: int, key: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return st_lottie(r.json(), height=height, key=key)

def show_page():
    st.title("Football Analysis App")
    st.markdown("""
    Welcome to the Football Analysis App! Here you can explore various statistics and insights about football matches.

    Before you begin, please select your preferred color theme from the sidebar:
    """)

    # Display a Lottie animation
    st_lottie_url = "https://assets5.lottiefiles.com/packages/lf20_YXD37q.json"  # Example football Lottie animation URL
    st_lottie(st_lottie_url, height=300, key="intro_lottie")
