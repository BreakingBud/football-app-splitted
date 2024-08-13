import streamlit as st
import numpy as np
from preprocess import load_and_preprocess_data
from model import create_model

st.title("FIFA World Cup 2026 Prediction")

# Load and preprocess data
zip_file_path = 'football_data_matches_scorers_shootouts.zip'
extract_path = '/tmp/extracted_data'
results_df, label_encoders, scaler = load_and_preprocess_data(zip_file_path, extract_path)

# Assume we are processing stages of the World Cup
# Example: Group stage, Round of 16, Quarterfinals, etc.
stages = ["Group Stage", "Round of 16", "Quarterfinals", "Semifinals", "Final"]
selected_stage = st.selectbox("Select World Cup Stage", stages)

if selected_stage == "Group Stage":
    st.subheader("Predicting Group Stage Matches")
    # Code to predict group stage matches
    # Here you would simulate or input group stage matches and predict outcomes
elif selected_stage == "Round of 16":
    st.subheader("Predicting Round of 16 Matches")
    # Code to predict Round of 16 matches
elif selected_stage == "Quarterfinals":
    st.subheader("Predicting Quarterfinal Matches")
    # Code to predict Quarterfinal matches
elif selected_stage == "Semifinals":
    st.subheader("Predicting Semifinal Matches")
    # Code to predict Semifinal matches
elif selected_stage == "Final":
    st.subheader("Predicting the Final Match")
    # Code to predict the Final match outcome

# Placeholder for model prediction
# This would be expanded based on the specific stage of the World Cup
