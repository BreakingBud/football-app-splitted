import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data_loader import load_data
from helpers import get_color_theme

# Attempt to load the data
try:
    goalscorers_df, results_df, shootouts_df = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()  # Stop the app if data loading fails

def show_page():
    st.title("Head-to-Head Analysis")
    st.markdown("""
    Compare the performance of two teams across various matches. Use the filters to customize your analysis.
    """)

    # Ensure the 'date' column is in datetime format and clean the data
    if 'date' in results_df.columns:
        results_df['date'] = pd.to_datetime(results_df['date'], errors='coerce')
        results_df = results_df.dropna(subset=['date'])
    else:
        st.error("The 'date' column is missing in the results data.")
        return

    # Set minimum and maximum dates for the slider
    min_date = results_df['date'].min()
    max_date = results_df['date'].max()

    # User input for selecting teams, tournament, and date range
    team1 = st.selectbox('Select Team 1', options=sorted(results_df['home_team'].unique()))
    team2 = st.selectbox('Select Team 2', options=sorted(results_df['away_team'].unique()))

    tournament = st.selectbox('Select Tournament', ['All'] + sorted(results_df['tournament'].unique().tolist()))
    tournament = '' if tournament == 'All' else tournament

    start_date, end_date = st.slider(
        'Select Date Range',
        min_value=min_date.to_pydatetime(),
        max_value=max_date.to_pydatetime(),
        value=(min_date.to_pydatetime(), max_date.to_pydatetime()),
        format="YYYY-MM-DD"
    )

    # Filter the data based on user input
    head_to_head_df = results_df.loc[
        (((results_df['home_team'] == team1) & (results_df['away_team'] == team2)) |
        ((results_df['home_team'] == team2) & (results_df['away_team'] == team1))) &
        (results_df['tournament'].str.contains(tournament, case=False, na=False)) &
        (results_df['date'].between(start_date, end_date))
    ]

    total_matches = len(head_to_head_df)
    st.markdown(f"**{team1}** and **{team2}** played **{total_matches}** matches head to head.")
    
    if total_matches > 0:
        # Pie Chart for Win Rate
        head_to_head_df = head_to_head_df.copy()  # Avoid SettingWithCopyWarning
        head_to_head_df.loc[:, 'outcome_label'] = head_to_head_df['outcome'].apply(
            lambda x: f'{team1} Win' if x == team1 else f'{team2} Win' if x == team2 else 'Draw'
        )
        outcome_counts = head_to_head_df['outcome_label'].value_counts()
        fig = px.pie(outcome_counts, names=outcome_counts.index, values=outcome_counts.values, title="Win Rate")
        st.plotly_chart(fig, use_container_width=True)

        # Line Chart for Match Results Timeline
        fig2 = px.line(head_to_head_df, x='date', y='outcome_label', title='Match Results Over Time', markers=True)
        fig2.update_yaxes(title='Match Outcome', categoryorder='array', categoryarray=[f'{team1} Win', f'{team2} Win', 'Draw'])
        st.plotly_chart(fig2, use_container_width=True)

        # Grouped Bar Chart for Goals Scored Distribution
        fig3 = go.Figure()
        fig3.add_trace(go.Histogram(x=head_to_head_df['home_score'], name=f'{team1} Goals', marker_color='blue', opacity=0.75))
        fig3.add_trace(go.Histogram(x=head_to_head_df['away_score'], name=f'{team2} Goals', marker_color='orange', opacity=0.75))

        fig3.update_layout(
            barmode='group',  # Use group mode instead of overlay
            title='Goals Scored Distribution',
            xaxis_title='Goals',
            yaxis_title='Count'
        )

        st.plotly_chart(fig3, use_container_width=True)

        # Display Shootout Data if available
        shootout_matches = head_to_head_df[head_to_head_df['shootout'] == True]
        if not shootout_matches.empty:
            st.markdown("### Shootout Matches:")
            st.dataframe(shootout_matches[['date', 'home_team', 'away_team', 'winner']], use_container_width=True)
        
        # Display Table of Match Details
        st.markdown("### Match Details:")
        st.dataframe(head_to_head_df[['date', 'home_team', 'away_team', 'home_score', 'away_score', 'outcome']], use_container_width=True)
    else:
        st.markdown("No matches found for the selected filters.")
