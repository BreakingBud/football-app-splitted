import streamlit as st
import requests
from constants import COLOR_PALETTES

def get_color_theme(theme):
    return COLOR_PALETTES.get(theme, COLOR_PALETTES["Primary"])

def load_lottie_url(url: str):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Lottie animation not found.")
        return None
