import streamlit as st
import numpy as np
from preprocess import load_and_preprocess_data
from model import train_model, predict_match

def create_knockout_bracket(teams):
    st.title("FIFA World Cup Knockout Stage Bracket")

    st.write("Round of 16")
    col1, col2, col3 = st.columns([1, 0.5, 1])
    
    with col1:
        st.text(f"{teams[0]} vs {teams[1]}")
        st.text(f"{teams[2]} vs {teams[3]}")
        st.text(f"{teams[4]} vs {teams[5]}")
        st.text(f"{teams[6]} vs {teams[7]}")
    
    with col2:
        st.text("→ Winner 1")
        st.text("→ Winner 2")
        st.text("→ Winner 3")
        st.text("→ Winner 4")
    
    with col3:
        st.text(f"{teams[8]} vs {teams[9]}")
        st.text(f"{teams[10]} vs {teams[11]}")
        st.text(f"{teams[12]} vs {teams[13]}")
        st.text(f"{teams[14]} vs {teams[15]}")

    # Continue building out the bracket for quarterfinals, semifinals, and final
    st.write("Quarterfinals")
    col4, col5, col6 = st.columns([1, 0.5, 1])

    with col4:
        st.text("Winner 1 vs Winner 2")
        st.text("Winner 3 vs Winner 4")

    with col5:
        st.text("→ Semifinal 1")
        st.text("→ Semifinal 2")

    with col6:
        st.text("Winner 5 vs Winner 6")
        st.text("Winner 7 vs Winner 8")

    st.write("Semifinals")
    col7, col8 = st.columns([1, 1])

    with col7:
        st.text("Semifinal 1")

    with col8:
        st.text("Semifinal 2")

    st.write("Final")
    st.text("Winner Semifinal 1 vs Winner Semifinal 2")

# Assuming you have already preprocessed data and trained a model
try:
    # Load preprocessed data and model
    X_train, X_test, y_train, y_test, label_encoders, scaler, home_team_encoder = load_and_preprocess_data('data.zip', 'extracted_path')
    model = train_model(X_train, y_train, X_train.shape[1])

    # Dummy team names for placeholder purposes
    teams = [
        "Group A Winner", "Group B Runner-Up",
        "Group C Winner", "Group D Runner-Up",
        "Group B Winner", "Group A Runner-Up",
        "Group D Winner", "Group C Runner-Up",
        "Group E Winner", "Group F Runner-Up",
        "Group G Winner", "Group H Runner-Up",
        "Group F Winner", "Group E Runner-Up",
        "Group H Winner", "Group G Runner-Up"
    ]

    create_knockout_bracket(teams)

except Exception as e:
    st.error(f"An error occurred: {e}")
