import streamlit as st
import pandas as pd
import plotly.express as px
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

    # Filter data based on selected players
    filtered_goalscorers_df = goalscorers_df.loc[(goalscorers_df['scorer'] == player1) | (goalscorers_df['scorer'] == player2)].copy()

    player1_data = filtered_goalscorers_df.loc[filtered_goalscorers_df['scorer'] == player1]
    player2_data = filtered_goalscorers_df.loc[filtered_goalscorers_df['scorer'] == player2]

    # Ensure 'date' is in datetime format
    player1_data['date'] = pd.to_datetime(player1_data['date'], errors='coerce')
    player2_data['date'] = pd.to_datetime(player2_data['date'], errors='coerce')

    # Group data by year and count goals
    player1_goals = player1_data.groupby(player1_data['date'].dt.year)['scorer'].count().reset_index(name=f'{player1} Goals')
    player2_goals = player2_data.groupby(player2_data['date'].dt.year)['scorer'].count().reset_index(name=f'{player2} Goals')

    if not player1_goals.empty and not player2_goals.empty:
        col1, col2 = st.columns(2)

        with col1:
            fig1 = px.line(player1_goals, x='date', y=f'{player1} Goals', title=f'{player1} Goals Over Time')
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = px.line(player2_goals, x='date', y=f'{player2} Goals', title=f'{player2} Goals Over Time')
            st.plotly_chart(fig2, use_container_width=True)

        # Calculate total goals for each player
        total_goals_player1 = player1_goals[f'{player1} Goals'].sum()
        total_goals_player2 = player2_goals[f'{player2} Goals'].sum()

        # Display total goals using a bar chart
        goals_data = pd.DataFrame({
            'Player': [player1, player2],
            'Total Goals': [total_goals_player1, total_goals_player2]
        })

        fig3 = px.bar(goals_data, x='Player', y='Total Goals', title='Total Goals Comparison')
        st.plotly_chart(fig3, use_container_width=True)

        # Calculate total matches involving each player
        total_matches = filtered_goalscorers_df.groupby('scorer')['date'].count().reset_index(name='Total Matches')

        # Display total matches using a bar chart
        fig4 = px.bar(total_matches, x='scorer', y='Total Matches', title='Total Matches Involving Each Player')
        st.plotly_chart(fig4, use_container_width=True)

        # Pie chart for match outcomes
        outcome_counts = results_df[(results_df['home_team'].isin([player1_data['team'].unique()[0], player2_data['team'].unique()[0]])) | 
                                    (results_df['away_team'].isin([player1_data['team'].unique()[0], player2_data['team'].unique()[0]]))]
        outcome_counts = outcome_counts['outcome'].value_counts()
        fig5 = px.pie(outcome_counts, names=outcome_counts.index, values=outcome_counts.values, title="Match Outcomes")
        st.plotly_chart(fig5, use_container_width=True)

    else:
        st.warning("No data available for the selected players.")

show_player_analysis()
