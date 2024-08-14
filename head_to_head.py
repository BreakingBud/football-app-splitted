import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def show_page(results_df):
    st.title("Head-to-Head Analysis")

    # Ensure the 'date' column is in datetime format
    results_df['date'] = pd.to_datetime(results_df['date'], errors='coerce')
    results_df = results_df.dropna(subset=['date'])

    # Set a reasonable minimum and maximum date for the slider
    min_date = results_df['date'].min()
    max_date = results_df['date'].max()

    # Select teams
    team1 = st.selectbox('Select Team 1', options=sorted(results_df['home_team'].unique()))
    team2 = st.selectbox('Select Team 2', options=sorted(results_df['away_team'].unique()))

    # Select tournament
    tournament = st.selectbox('Select Tournament', ['All'] + sorted(results_df['tournament'].unique().tolist()))
    tournament = '' if tournament == 'All' else tournament

    # Select date range
    start_date, end_date = st.slider(
        'Select Date Range',
        min_value=min_date.to_pydatetime(),
        max_value=max_date.to_pydatetime(),
        value=(min_date.to_pydatetime(), max_date.to_pydatetime()),
        format="YYYY-MM-DD"
    )

    # Filter the data based on user input
    head_to_head_df = filter_head_to_head_data(results_df, team1, team2, tournament, start_date, end_date)

    # Display results
    display_head_to_head_results(head_to_head_df, team1, team2)


def filter_head_to_head_data(df, team1, team2, tournament, start_date, end_date):
    # Filter data based on selected teams, tournament, and date range
    return df.loc[
        (((df['home_team'] == team1) & (df['away_team'] == team2)) |
        ((df['home_team'] == team2) & (df['away_team'] == team1))) &
        (df['tournament'].str.contains(tournament, case=False, na=False)) &
        (df['date'].between(start_date, end_date))
    ]


def display_head_to_head_results(df, team1, team2):
    total_matches = len(df)
    st.markdown(f"**{team1}** and **{team2}** played **{total_matches}** matches head to head.")
    
    if total_matches > 0:
        # Pie Chart for Win Rate
        df['outcome_label'] = df['outcome'].apply(
            lambda x: f'{team1} Win' if x == team1 else f'{team2} Win' if x == team2 else 'Draw'
        )
        outcome_counts = df['outcome_label'].value_counts()
        fig = px.pie(outcome_counts, names=outcome_counts.index, values=outcome_counts.values, title="Win Rate")
        st.plotly_chart(fig, use_container_width=True)

        # Line Chart for Match Results Timeline
        fig2 = px.line(df, x='date', y='outcome_label', title='Match Results Over Time', markers=True)
        fig2.update_yaxes(title='Match Outcome', categoryorder='array', categoryarray=[f'{team1} Win', f'{team2} Win', 'Draw'])
        st.plotly_chart(fig2, use_container_width=True)

        # Grouped Bar Chart for Goals Scored Distribution
        fig3 = go.Figure()
        fig3.add_trace(go.Histogram(x=df['home_score'], name=f'{team1} Goals', marker_color='blue', opacity=0.75))
        fig3.add_trace(go.Histogram(x=df['away_score'], name=f'{team2} Goals', marker_color='orange', opacity=0.75))

        fig3.update_layout(
            barmode='group',  # Use group mode instead of overlay
            title='Goals Scored Distribution',
            xaxis_title='Goals',
            yaxis_title='Count'
        )

        st.plotly_chart(fig3, use_container_width=True)

        # Display Shootout Data if available
        shootout_matches = df[df['shootout'] == True]
        if not shootout_matches.empty:
            st.markdown("### Shootout Matches:")
            st.dataframe(shootout_matches[['date', 'home_team', 'away_team', 'winner']], use_container_width=True)
        
        # Display Table of Match Details
        st.markdown("### Match Details:")
        st.dataframe(df[['date', 'home_team', 'away_team', 'home_score', 'away_score', 'outcome']], use_container_width=True)
    else:
        st.markdown("No matches found for the selected filters.")
