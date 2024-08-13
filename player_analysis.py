import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data_loader import load_data

# Load the data
goalscorers_df, results_df, shootouts_df = load_data()

def show_player_analysis():
    st.title("Player-to-Player Analysis")
    st.markdown("""
    ### Compare performance between two players
    Select players from the dropdown menus to see a side-by-side comparison of their performance over time.
    """)

    # Use 'scorer' instead of 'player' and allow selection from the list
    player_list = goalscorers_df['scorer'].unique()
    player1 = st.selectbox('Select Player 1', options=player_list, index=0, key="player1_select")
    player2 = st.selectbox('Select Player 2', options=player_list, index=1, key="player2_select")

    # Select tournament after selecting players
    tournaments = results_df['tournament'].unique()
    selected_tournament = st.selectbox('Select Tournament', ['All'] + sorted(tournaments.tolist()))

    # Filter data based on selected players and tournament
    filtered_goalscorers_df = goalscorers_df.loc[
        (goalscorers_df['scorer'].isin([player1, player2])) &
        ((goalscorers_df['team'].isin(results_df.loc[results_df['tournament'] == selected_tournament, 'home_team'])) |
         (goalscorers_df['team'].isin(results_df.loc[results_df['tournament'] == selected_tournament, 'away_team'])) if selected_tournament != 'All' else True)
    ]

    player1_data = filtered_goalscorers_df[filtered_goalscorers_df['scorer'] == player1]
    player2_data = filtered_goalscorers_df[filtered_goalscorers_df['scorer'] == player2]

    # Ensure 'date' is in datetime format
    player1_data['date'] = pd.to_datetime(player1_data['date'], errors='coerce')
    player2_data['date'] = pd.to_datetime(player2_data['date'], errors='coerce')

    # Group data by year and count goals
    player1_goals = player1_data.groupby(player1_data['date'].dt.year)['scorer'].count().reset_index(name=f'{player1} Goals')
    player2_goals = player2_data.groupby(player2_data['date'].dt.year)['scorer'].count().reset_index(name=f'{player2} Goals')

    if not player1_goals.empty or not player2_goals.empty:
        col1, col2 = st.columns(2)

        with col1:
            fig = px.line(player1_goals, x='date', y=f'{player1} Goals', title=f'{player1} Goals Over Time')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig2 = px.line(player2_goals, x='date', y=f'{player2} Goals', title=f'{player2} Goals Over Time')
            st.plotly_chart(fig2, use_container_width=True)

        # Bar chart for total goals comparison
        player_comparison = pd.DataFrame({
            'Player': [player1, player2],
            'Total Goals': [
                player1_goals[f'{player1} Goals'].sum(),
                player2_goals[f'{player2} Goals'].sum()
            ]
        })

        fig3 = px.bar(player_comparison, x='Player', y='Total Goals', title='Total Goals Comparison')
        st.plotly_chart(fig3, use_container_width=True)
        
        # Adding a pie chart to visualize goal distribution
        total_goals = player1_goals[f'{player1} Goals'].sum() + player2_goals[f'{player2} Goals'].sum()
        if total_goals > 0:
            goal_distribution = pd.DataFrame({
                'Player': [player1, player2],
                'Goals': [
                    player1_goals[f'{player1} Goals'].sum(),
                    player2_goals[f'{player2} Goals'].sum()
                ]
            })

            fig4 = px.pie(goal_distribution, values='Goals', names='Player', title='Goals Distribution')
            st.plotly_chart(fig4, use_container_width=True)
        
    else:
        st.warning("No data available for the selected players and tournament.")

show_player_analysis()
