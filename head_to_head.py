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

    # Display dynamic content
    if head_to_head_df.empty:
        st.warning("No matches found for the selected filters.")
        return
    else:
        st.success(f"Found {len(head_to_head_df)} matches between {team1} and {team2}.")

    # Group visualizations in columns
    col1, col2 = st.columns(2)

    with col1:
        display_win_rate_pie_chart(head_to_head_df, team1, team2)
        display_goals_heatmap(head_to_head_df, team1, team2)
        
    with col2:
        display_match_results_timeline(head_to_head_df, team1, team2)
        display_goals_distribution_bar_chart(head_to_head_df, team1, team2)

    # Display tables at the end
    with st.expander("Detailed Match Information"):
        display_shootout_data(head_to_head_df)
        display_match_details_table(head_to_head_df)


def filter_head_to_head_data(df, team1, team2, tournament, start_date, end_date):
    # Filter data based on selected teams, tournament, and date range
    return df.loc[
        (((df['home_team'] == team1) & (df['away_team'] == team2)) |
        ((df['home_team'] == team2) & (df['away_team'] == team1))) &
        (df['tournament'].str.contains(tournament, case=False, na=False)) &
        (df['date'].between(start_date, end_date))
    ]


def display_win_rate_pie_chart(df, team1, team2):
    # Pie Chart for Win Rate
    df['outcome_label'] = df['outcome'].apply(
        lambda x: f'{team1} Win' if x == team1 else f'{team2} Win' if x == team2 else 'Draw'
    )
    outcome_counts = df['outcome_label'].value_counts()
    fig = px.pie(outcome_counts, names=outcome_counts.index, values=outcome_counts.values, title="Win Rate")
    st.plotly_chart(fig, use_container_width=True)


def display_match_results_timeline(df, team1, team2):
    # Line Chart for Match Results Timeline
    fig = px.line(df, x='date', y='outcome_label', title='Match Results Over Time', markers=True)
    fig.update_yaxes(title='Match Outcome', categoryorder='array', categoryarray=[f'{team1} Win', f'{team2} Win', 'Draw'])
    st.plotly_chart(fig, use_container_width=True)


def display_goals_distribution_bar_chart(df, team1, team2):
    # Grouped Bar Chart for Goals Scored Distribution
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=df['home_score'], name=f'{team1} Goals', marker_color='blue', opacity=0.75))
    fig.add_trace(go.Histogram(x=df['away_score'], name=f'{team2} Goals', marker_color='orange', opacity=0.75))

    fig.update_layout(
        barmode='group',  # Use group mode instead of overlay
        title='Goals Scored Distribution',
        xaxis_title='Goals',
        yaxis_title='Count'
    )

    st.plotly_chart(fig, use_container_width=True)


def display_goals_heatmap(df, team1, team2):
    # Create a pivot table for heatmap
    heatmap_data = df.pivot_table(index='home_score', columns='away_score', aggfunc='size', fill_value=0)

    # Plot the heatmap using Plotly
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='Blues'
    ))

    fig.update_layout(
        title=f"Goals Heatmap: {team1} vs {team2}",
        xaxis_title=f"{team2} Goals",
        yaxis_title=f"{team1} Goals"
    )

    st.plotly_chart(fig, use_container_width=True)


def display_shootout_data(df):
    # Display Shootout Data if available
    shootout_matches = df[df['shootout'] == True]
    if not shootout_matches.empty:
        st.markdown("### Shootout Matches:")
        st.dataframe(shootout_matches[['date', 'home_team', 'away_team', 'winner']], use_container_width=True)


def display_match_details_table(df):
    # Display Table of Match Details
    st.markdown("### Match Details:")
    st.dataframe(df[['date', 'home_team', 'away_team', 'home_score', 'away_score', 'outcome']], use_container_width=True)


# This function call assumes that `results_df` will be passed from the `app.py` file when this module is imported and executed
# show_page(results_df)
