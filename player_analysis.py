import streamlit as st
import pandas as pd
import plotly.express as px
from data_loader import load_data

# Load the data
goalscorers_df, results_df, shootouts_df = load_data()

def show_player_analysis():
    st.title("Player-to-Player Analysis")
    st.markdown("""
    ### Compare Performance Between Two Players

    Select players from the dropdown menus to see a side-by-side comparison of their goal-scoring performance over time.
    """)

    # Use 'scorer' instead of 'player' and allow selection from the list
    player_list = goalscorers_df['scorer'].unique()
    player1 = st.selectbox('Select Player 1', options=player_list, index=0, key="player1_select")
    player2 = st.selectbox('Select Player 2', options=player_list, index=1, key="player2_select")

    # Filter data based on selected players
    player1_data = goalscorers_df.loc[goalscorers_df['scorer'] == player1].copy()
    player2_data = goalscorers_df.loc[goalscorers_df['scorer'] == player2].copy()

    # Ensure 'date' is in datetime format and handle any conversion errors
    try:
        player1_data['date'] = pd.to_datetime(player1_data['date'], errors='coerce')
        player2_data['date'] = pd.to_datetime(player2_data['date'], errors='coerce')
    except Exception as e:
        st.error(f"Error converting dates: {e}")
        return

    # Drop rows with NaT values in the date column (in case conversion failed for some rows)
    player1_data = player1_data.dropna(subset=['date'])
    player2_data = player2_data.dropna(subset=['date'])

    if player1_data.empty or player2_data.empty:
        st.warning("No data available for the selected players.")
        return

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

    else:
        st.warning("No data available for the selected players.")

show_player_analysis()
