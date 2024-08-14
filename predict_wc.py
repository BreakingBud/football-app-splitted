import streamlit as st
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from preprocess import load_and_preprocess_data
from model import create_model

# Load and preprocess data
zip_file_path = 'football_data_matches_scorers_shootouts.zip'
extract_path = '/tmp/extracted_data'
results_df, label_encoders, scaler = load_and_preprocess_data(zip_file_path, extract_path)

st.title("FIFA World Cup Knockout Stage Prediction")

# User inputs for the 16 teams
st.subheader("Select the 16 teams that qualified for the knockout stage")
teams = []
for i in range(1, 17):
    team = st.selectbox(f"Team {i}", options=results_df['home_team'].unique(), key=f"team_{i}")
    if team:
        teams.append(team)

# Ensure 16 teams are selected
if len(teams) == 16:
    # Define initial match pairings based on the bracket structure
    matches = [
        (teams[0], teams[15]), (teams[7], teams[8]),
        (teams[4], teams[11]), (teams[3], teams[12]),
        (teams[2], teams[13]), (teams[5], teams[10]),
        (teams[6], teams[9]), (teams[1], teams[14])
    ]

    # Predict winners for each match
    winners = []
    for match in matches:
        home_team_encoded = label_encoders['home_team'].transform([match[0]])[0]
        away_team_encoded = label_encoders['away_team'].transform([match[1]])[0]
        input_data = np.array([[home_team_encoded, away_team_encoded]])
        input_data = scaler.transform(input_data)
        
        model = create_model(input_dim=input_data.shape[1])
        model.load_weights("path_to_your_trained_model.h5")  # Replace with actual path
        prediction = model.predict(input_data)
        
        winner = match[0] if prediction[0][0] > 0.5 else match[1]
        winners.append(winner)

    # Predict subsequent rounds
    quarterfinals = [(winners[i], winners[i+1]) for i in range(0, len(winners), 2)]
    winners_quarterfinals = []
    for match in quarterfinals:
        home_team_encoded = label_encoders['home_team'].transform([match[0]])[0]
        away_team_encoded = label_encoders['away_team'].transform([match[1]])[0]
        input_data = np.array([[home_team_encoded, away_team_encoded]])
        input_data = scaler.transform(input_data)
        
        prediction = model.predict(input_data)
        
        winner = match[0] if prediction[0][0] > 0.5 else match[1]
        winners_quarterfinals.append(winner)

    semifinals = [(winners_quarterfinals[0], winners_quarterfinals[1]), (winners_quarterfinals[2], winners_quarterfinals[3])]
    winners_semifinals = []
    for match in semifinals:
        home_team_encoded = label_encoders['home_team'].transform([match[0]])[0]
        away_team_encoded = label_encoders['away_team'].transform([match[1]])[0]
        input_data = np.array([[home_team_encoded, away_team_encoded]])
        input_data = scaler.transform(input_data)
        
        prediction = model.predict(input_data)
        
        winner = match[0] if prediction[0][0] > 0.5 else match[1]
        winners_semifinals.append(winner)

    final = (winners_semifinals[0], winners_semifinals[1])
    home_team_encoded = label_encoders['home_team'].transform([final[0]])[0]
    away_team_encoded = label_encoders['away_team'].transform([final[1]])[0]
    input_data = np.array([[home_team_encoded, away_team_encoded]])
    input_data = scaler.transform(input_data)

    prediction = model.predict(input_data)
    final_winner = final[0] if prediction[0][0] > 0.5 else final[1]

    # Draw the bracket programmatically
    image = Image.new('RGB', (1000, 1000), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", 20)  # Replace with a path to a suitable font if needed

    # Define positions for the text
    positions = [
        (50, 150), (50, 250), (50, 350), (50, 450),
        (50, 550), (50, 650), (50, 750), (50, 850),
        (200, 200), (200, 400), (200, 600), (200, 800),
        (350, 300), (350, 700), (500, 500)
    ]

    # Draw the team names and winners on the image
    for i, team in enumerate(teams):
        draw.text(positions[i], team, font=font, fill="black")

    for i, winner in enumerate(winners):
        draw.text(positions[8+i], winner, font=font, fill="black")

    for i, winner in enumerate(winners_quarterfinals):
        draw.text(positions[12+i], winner, font=font, fill="black")

    draw.text(positions[14], final_winner, font=font, fill="black")

    # Display the filled bracket image
    st.image(image, caption="World Cup Knockout Predictions", use_column_width=True)
