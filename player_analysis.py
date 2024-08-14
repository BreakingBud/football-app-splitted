import streamlit as st
import plotly.express as px
import pandas as pd
from data_loader import load_data

# Load the data
goalscorers_df, _, _ = load_data()

def show_page():
    st.title("Player-to-Player Analysis")
    st.markdown("Compare the performance of different players across various matches.")

    player1 = st.selectbox('Select Player 1', sorted(goalscorers_df['player_name'].unique()))
    player2 = st.selectbox('Select Player 2', sorted(goalscorers_df['player_name'].unique()))

    player1_df = goalscorers_df[goalscorers_df['player_name'] == player1]
    player2_df = goalscorers_df[goalscorers_df['player_name'] == player2]

    # Example: Plot goals scored by each player
    player1_goals = player1_df.groupby('match_date')['goals'].sum()
    player2_goals = player2_df.groupby('match_date')['goals'].sum()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=player1_goals.index, y=player1_goals.values, mode='lines+markers', name=player1))
    fig.add_trace(go.Scatter(x=player2_goals.index, y=player2_goals.values, mode='lines+markers', name=player2))

    fig.update_layout(title="Goals Scored Over Time", xaxis_title="Date", yaxis_title="Goals")
    st.plotly_chart(fig, use_container_width=True)
