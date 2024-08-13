import streamlit as st

def show_intro():
    st.title("Football Analysis App")
    st.markdown("""
    ### Welcome to the Football Analysis App
    
    Explore historical football match data and analyze head-to-head matchups and player performance across different teams.
    
    Use the sidebar to navigate through different sections of the app.
    """)

show_intro()
