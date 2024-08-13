import streamlit as st
import numpy as np
from preprocess import load_and_preprocess_data
from model import create_model

st.title("World Cup 2026 Prediction")

# Load and preprocess data
data_path = "path_to_your_data_folder"
results_df, label_encoders, scaler = load_and_preprocess_data(data_path)

# Select inputs
home_team = st.selectbox("Select Home Team", options=label_encoders['home_team'].classes_)
away_team = st.selectbox("Select Away Team", options=label_encoders['away_team'].classes_)
tournament = st.selectbox("Select Tournament", options=label_encoders['tournament'].classes_)

# Encode inputs
home_team_encoded = label_encoders['home_team'].transform([home_team])[0]
away_team_encoded = label_encoders['away_team'].transform([away_team])[0]
tournament_encoded = label_encoders['tournament'].transform([tournament])[0]

# Prepare data for prediction
X_input = np.array([[home_team_encoded, away_team_encoded, 0, 0, tournament_encoded, 0, 0, 0]])
X_input = scaler.transform(X_input)

# Load model and predict
model = create_model(input_dim=X_input.shape[1])
model.load_weights("path_to_your_trained_model.h5")
prediction = model.predict(X_input)

st.write("Predicted Probability of Home Team Win:", prediction[0][0])
