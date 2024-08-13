import streamlit as st
import plotly.express as px
from data_loader import load_data

goalscorers_df, results_df, shootouts_df = load_data()

def show_head_to_head():
    st.title("Head-to-Head Analysis")
    team1 = st.selectbox('Select Team 1', results_df['home_team'].unique())
    team2 = st.selectbox('Select Team 2', results_df['home_team'].unique())
    tournament = st.selectbox('Select Tournament', ['All'] + sorted(results_df['tournament'].unique().tolist()))
    tournament = '' if tournament == 'All' else tournament
    start_date, end_date = st.slider(
        'Select Date Range',
        min_value=results_df['date'].min().to_pydatetime(),
        max_value=results_df['date'].max().to_pydatetime(),
        value=(results_df['date'].min().to_pydatetime(), results_df['date'].max().to_pydatetime()),
        format="YYYY-MM-DD"
    )

    head_to_head_df = results_df[
        (((results_df['home_team'] == team1) & (results_df['away_team'] == team2)) |
        ((results_df['home_team'] == team2) & (results_df['away_team'] == team1))) &
        (results_df['tournament'].str.contains(tournament, case=False, na=False)) &
        (results_df['date'].between(start_date, end_date))
    ]

    st.markdown(f"**{team1}** and **{team2}** played **{len(head_to_head_df)}** matches head to head.")
    if tournament:
        st.markdown(f"Filtering by tournament: **{tournament}**")

    head_to_head_df['outcome_label'] = head_to_head_df['outcome'].apply(
        lambda x: f'{team1} Win' if x == team1 else f'{team2} Win' if x == team2 else 'Draw'
    )

    fig = px.pie(head_to_head_df['outcome_label'].value_counts(), title="Win Rate")
    st.plotly_chart(fig, use_container_width=True)

    shootout_matches = head_to_head_df[head_to_head_df['shootout'] == True]
    if not shootout_matches.empty:
        st.markdown("### Shootout Matches:")
        st.dataframe(shootout_matches[['date', 'home_team', 'away_team', 'winner']], use_container_width=True)

show_head_to_head()
