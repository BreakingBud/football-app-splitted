import streamlit as st
import plotly.express as px
from data_loader import load_data

goalscorers_df, results_df, shootouts_df = load_data()

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

    player1_goals = player1_data.groupby(pd.to_datetime(player1_data['date']).dt.year)['goals'].sum().reset_index()
    player2_goals = player2_data.groupby(pd.to_datetime(player2_data['date']).dt.year)['goals'].sum().reset_index()

    st.plotly_chart(px.line(player1_goals, x='date', y='goals', title=f'Goals Scored by {player1}'), use_container_width=True)
    st.plotly_chart(px.line(player2_goals, x='date', y='goals', title=f'Goals Scored by {player2}'), use_container_width=True)

    player_comparison = pd.DataFrame({
        'Player': [player1, player2],
        'Total Goals': [player1_data['goals'].sum(), player2_data['goals'].sum()]
    })
    st.plotly_chart(px.bar(player_comparison, x='Player', y='Total Goals', title='Total Goals Comparison'), use_container_width=True)

show_player_analysis()
