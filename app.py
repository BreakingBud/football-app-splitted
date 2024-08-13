import streamlit as st

# Set up the app configuration
st.set_page_config(
    page_title="Football Analysis App",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar for navigation
st.sidebar.title("Navigation")
pages = {
    "Introduction": "introduction",
    "Head-to-Head Analysis": "head_to_head",
    "Player-to-Player Analysis": "player_analysis",
    "Choropleth Map": "choropleth_map",
    "FIFA World Cup 2026 Prediction": "predict_wc"
}

# Radio buttons for page selection
selected_page = st.sidebar.radio("Go to", list(pages.keys()))

# Load the selected page as a module
page = pages[selected_page]
try:
    exec(open(f"{page}.py").read())
except FileNotFoundError:
    st.error(f"Page '{page}' not found. Please check the file path.")
except Exception as e:
    st.error(f"An error occurred while loading the page '{page}': {str(e)}")
