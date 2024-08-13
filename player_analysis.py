import streamlit as st
import pandas as pd
import plotly.express as px
from data_loader import load_data

# Load the data
goalscorers_df, results_df, shootouts_df = load_data()

# Display the column names to check for potential issues
st.write("Available columns in goalscorers_df:", goalscorers_df.columns)

# Ensure the 'player' and 'date' columns exist and are correctly named
if 'player' not in goalscorers_df.columns or 'date' not in goalscorers_df.columns:
    st.error("The required columns ('player', 'date') are not present in the dataset.")
else:
    def show_player_analysis():
        st.title("Player-to-Player Analysis")
        st.markdown("""
        ### Compare performance between two players
        Select players from the dropdown menus to see a side-by-side comparison of their performance over time.
        """)

        player1 = st.selectbox('Select Player 1', goalscorers_df['player'].unique())
        player2 = st.selectbox('Select Player 2', goalscorers_df['player'].unique())

        player1_data = goalscorers_df[goalscorers_df['player'] == player1]
        player2_data = goalscorers_df[goalscorers_df['player'] == player2]

        # Ensure 'date' is in datetime format
        player1_data['date'] = pd.to_datetime(player1_data['date'], errors='coerce')
        player2_data['date'] = pd.to_datetime(player2_data['date'], errors='coerce')

        # Line chart of goals over time
        player1_goals = player1_data.groupby(player1_data['date'].dt.year)['goals'].sum().reset_index(name=f'{player1} Goals')
        player2_goals = player2_data.groupby(player2_data['date'].dt.year)['goals'].sum().reset_index(name=f'{player2} Goals')

        if not player1_goals.empty and not player2_goals.empty:
            fig = px.line(player1_goals, x='date', y=f'{player1} Goals', title=f'{player1} Goals Over Time')
            st.plotly_chart(fig, use_container_width=True)
            
            fig2 = px.line(player2_goals, x='date', y=f'{player2} Goals', title=f'{player2} Goals Over Time')
            st.plotly_chart(fig2, use_container_width=True)

            # Bar chart for total goals comparison
            player_comparison = pd.DataFrame({
                'Player': [player1, player2],
                'Total Goals': [player1_goals[f'{player1} Goals'].sum(), player2_goals[f'{player2} Goals'].sum()]
            })

            fig3 = px.bar(player_comparison, x='Player', y='Total Goals', title='Total Goals Comparison')
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.warning("No data available for the selected players.")

    show_player_analysis()
