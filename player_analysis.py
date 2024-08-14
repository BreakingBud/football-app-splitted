import streamlit as st
import pandas as pd
import plotly.express as px

def show_page(goalscorers_df):
    st.title("Player-to-Player Analysis")
    st.markdown("""
    ### Compare the Performance of Two Players
    Select two players to compare their goal-scoring records over time.
    """)

    # Dropdowns for player selection
    player1 = st.selectbox("Select Player 1", options=sorted(goalscorers_df['scorer'].unique()))
    player2 = st.selectbox("Select Player 2", options=sorted(goalscorers_df['scorer'].unique()))

    # Filter data by selected players
    player1_data = goalscorers_df[goalscorers_df['scorer'] == player1]
    player2_data = goalscorers_df[goalscorers_df['scorer'] == player2]

    if player1_data.empty or player2_data.empty:
        st.warning("No data available for the selected players.")
        return

    # Convert 'date' column to datetime
    player1_data['date'] = pd.to_datetime(player1_data['date'], errors='coerce')
    player2_data['date'] = pd.to_datetime(player2_data['date'], errors='coerce')

    # Drop rows with NaT values in the date column
    player1_data = player1_data.dropna(subset=['date'])
    player2_data = player2_data.dropna(subset=['date'])

    if player1_data.empty or player2_data.empty:
        st.warning("No data available for the selected players after date filtering.")
        return

    # Group data by year and count goals
    player1_goals = player1_data.groupby(player1_data['date'].dt.year)['scorer'].count().reset_index(name=f'{player1} Goals')
    player2_goals = player2_data.groupby(player2_data['date'].dt.year)['scorer'].count().reset_index(name=f'{player2} Goals')

    # Plot goals over time for each player
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
