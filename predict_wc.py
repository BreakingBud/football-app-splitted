import streamlit as st
import numpy as np
from preprocess import load_and_preprocess_data
from model import create_model

st.title("World Cup 2026 Prediction")

# Load and preprocess data
zip_file_path = 'football_data_matches_scorers_shootouts.zip'
extract_path = '/tmp/extracted_data'

goalscorers_df, results_df, shootouts_df = load_and_preprocess_data(zip_file_path, extract_path)

# Select inputs
home_team = st.selectbox("Select Home Team", options=results_df['home_team'].unique())
away_team = st.selectbox("Select Away Team", options=results_df['away_team'].unique())
tournament = st.selectbox("Select Tournament", options=results_df['tournament'].unique())

# Prepare data for prediction (this is just a placeholder)
input_data = np.array([[1, 1, 0, 0, 0, 0, 0, 0]])  # Replace with actual data
input_dim = input_data.shape[1]

# Load and apply the model
model = create_model(input_dim)
model.load_weights("path_to_your_trained_model.h5")
prediction = model.predict(input_data)

st.write("Predicted Probability of Home Team Win:", prediction[0][0])
