import streamlit as st
import traceback
from preprocess import load_and_preprocess_data
from model import train_model

try:
    # Load and preprocess data
    zip_file_path = 'football_data_matches_scorers_shootouts.zip'
    extract_path = '/tmp/extracted_data'
    
    # Check the number of returned values from the function
    unpacked_values = load_and_preprocess_data(zip_file_path, extract_path)
    st.write(f"Returned values count: {len(unpacked_values)}")
    st.write(f"Returned values: {unpacked_values}")

    # Unpack the values
    if len(unpacked_values) == 7:
        X_train, X_test, y_train, y_test, label_encoders, scaler, team_encoder = unpacked_values
    else:
        st.error("Unexpected number of values returned from load_and_preprocess_data()")
        raise ValueError("Unexpected number of values returned from load_and_preprocess_data()")

    # Train the model
    model = train_model(X_train, y_train, X_train.shape[1])

    st.title("FIFA World Cup Knockout Stage Prediction")

    # Define the bracket structure based on group winners and runners-up
    st.subheader("Select the 16 teams that qualified for the knockout stage")
    teams = []
    for i in range(16):
        team = st.selectbox(f"Team {i+1}", options=team_encoder.classes_, key=f"team_{i}")
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

        # Predict the winners for each match
        winners = []
        for match in matches:
            try:
                home_team_encoded = team_encoder.transform([match[0]])[0]
                away_team_encoded = team_encoder.transform([match[1]])[0]
                input_data = np.array([[home_team_encoded, away_team_encoded, 0, 0, 0]])  # Example input data
                input_data = scaler.transform(input_data)

                prediction = model.predict(input_data)
                winner = match[0] if prediction[0][0] > 0.5 else match[1]
                winners.append(winner)
            except Exception as e:
                st.error(f"Error predicting match {match[0]} vs {match[1]}: {e}")
                st.text(traceback.format_exc())

        st.write("### Predicted Winners of the Knockout Stage")
        for i, match in enumerate(matches):
            st.write(f"Match {i+1}: {match[0]} vs {match[1]} -> **{winners[i]}**")

        st.write("### Bracket Progression")
        for i in range(0, len(winners), 2):
            st.write(f"Quarterfinal Match {i//2+1}: {winners[i]} vs {winners[i+1]}")

except Exception as e:
    st.error(f"An error occurred: {e}")
    st.text(traceback.format_exc())
