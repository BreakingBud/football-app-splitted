import streamlit as st
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from preprocess import load_and_preprocess_data

# Load and preprocess data
zip_file_path = 'football_data_matches_scorers_shootouts.zip'
extract_path = '/tmp/extracted_data'
results_df, label_encoders, scaler, team_encoder = load_and_preprocess_data(zip_file_path, extract_path)

st.title("FIFA World Cup Knockout Stage Prediction")

# Get the original team names before encoding
team_names = team_encoder.classes_

# Get top 16 teams by goals scored
top_teams = results_df.groupby('home_team')['home_score'].sum().sort_values(ascending=False).head(16).index.tolist()
top_teams = [team_encoder.inverse_transform([team])[0] for team in top_teams]

# User inputs for the 16 teams
st.subheader("Select the 16 teams that qualified for the knockout stage")
teams = []
for i in range(16):
    team = st.selectbox(f"Team {i+1}", options=team_names, index=team_names.tolist().index(top_teams[i]), key=f"team_{i}")
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

    # Placeholder for winners (normally this would be done with predictions)
    winners = [match[0] for match in matches]  # Placeholder: always choose the first team

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

    # Display the filled bracket image
    st.image(image, caption="World Cup Knockout Predictions", use_column_width=True)
