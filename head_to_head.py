import streamlit as st
import pandas as pd

def show_page(results_df=None):
    st.title("Head-to-Head Analysis")
    st.markdown("""
    ### Compare the Performance of Two Teams
    Select two teams and a tournament to see their head-to-head match history.
    """)

    # Dropdown for team selection
    team1 = st.selectbox("Select Team 1", options=sorted(results_df['home_team'].unique()))
    team2 = st.selectbox("Select Team 2", options=sorted(results_df['away_team'].unique()))

    # Dropdown for tournament selection
    tournament = st.selectbox(
        "Select Tournament",
        options=["All"] + sorted(results_df['tournament'].unique().tolist()),
        index=0
    )

    # Filter data by selected teams and tournament
    filtered_df = results_df[((results_df['home_team'] == team1) & (results_df['away_team'] == team2)) |
                             ((results_df['home_team'] == team2) & (results_df['away_team'] == team1))]

    if tournament != "All":
        filtered_df = filtered_df[filtered_df['tournament'] == tournament]

    if filtered_df.empty:
        st.warning("No matches found between the selected teams in the selected tournament.")
        return

    # Display match history
    st.write(f"Head-to-Head matches between {team1} and {team2}:")
    st.dataframe(filtered_df[['date', 'home_team', 'away_team', 'home_score', 'away_score', 'tournament']])

    # Calculate and display overall statistics
    team1_wins = filtered_df[((filtered_df['home_team'] == team1) & (filtered_df['home_score'] > filtered_df['away_score'])) |
                             ((filtered_df['away_team'] == team1) & (filtered_df['away_score'] > filtered_df['home_score']))].shape[0]

    team2_wins = filtered_df[((filtered_df['home_team'] == team2) & (filtered_df['home_score'] > filtered_df['away_score'])) |
                             ((filtered_df['away_team'] == team2) & (filtered_df['away_score'] > filtered_df['home_score']))].shape[0]

    draws = filtered_df[filtered_df['home_score'] == filtered_df['away_score']].shape[0]

    st.write(f"**{team1} Wins:** {team1_wins}")
    st.write(f"**{team2} Wins:** {team2_wins}")
    st.write(f"**Draws:** {draws}")
