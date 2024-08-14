import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from helpers import get_color_theme

def show_page(results_df):
    st.title("Head-to-Head Analysis")
    st.markdown("""
    Compare the performance of two teams across various matches. Use the filters to customize your analysis.
    """)

    # Ensure the 'date' column is in datetime format and clean the data
    results_df['date'] = pd.to_datetime(results_df['date'], errors='coerce')
    results_df = results_df.dropna(subset=['date'])

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
    head_to_head_df = filter_head_to_head_data(results_df, team1, team2, tournament, start_date, end_date)

    # Display message if no matches are found
    if head_to_head_df.empty:
        st.warning("No matches found for the selected filters.")
        return
    else:
        st.success(f"Found {len(head_to_head_df)} matches between {team1} and {team2}.")

    # Get the selected color theme
    color_theme = get_color_theme(st.session_state.get('theme', "Primary"))

    # Group visualizations into two columns for better layout
    col1, col2 = st.columns(2)

    # Display visualizations in the left column
    with col1:
        display_win_rate_pie_chart(head_to_head_df, team1, team2, color_theme)
        display_goals_heatmap(head_to_head_df, team1, team2, color_theme)
        
    # Display visualizations in the right column
    with col2:
        display_match_results_timeline(head_to_head_df, team1, team2, color_theme)
        display_goals_distribution_bar_chart(head_to_head_df, team1, team2, color_theme)

    # Expandable section for detailed match information
    with st.expander("Detailed Match Information"):
        display_match_details_table(head_to_head_df)

# Function to filter data based on user input
def filter_head_to_head_data(df, team1, team2, tournament, start_date, end_date):
    return df.loc[
        (((df['home_team'] == team1) & (df['away_team'] == team2)) |
        ((df['home_team'] == team2) & (df['away_team'] == team1))) &
        (df['tournament'].str.contains(tournament, case=False, na=False)) &
        (df['date'].between(start_date, end_date))
    ]

# Function to display a pie chart of match outcomes (win rate)
def display_win_rate_pie_chart(df, team1, team2, color_theme):
    df['outcome_label'] = df['outcome'].apply(
        lambda x: f'{team1} Win' if x == team1 else f'{team2} Win' if x == team2 else 'Draw'
    )
    outcome_counts = df['outcome_label'].value_counts()
    fig = px.pie(outcome_counts, names=outcome_counts.index, values=outcome_counts.values, title="Win Rate", color_discrete_sequence=color_theme)
    st.plotly_chart(fig, use_container_width=True)

# Function to display a timeline of match results
def display_match_results_timeline(df, team1, team2, color_theme):
    fig = px.line(df, x='date', y='outcome_label', title='Match Results Over Time', markers=True, color_discrete_sequence=color_theme)
    fig.update_yaxes(title='Match Outcome', categoryorder='array', categoryarray=[f'{team1} Win', f'{team2} Win', 'Draw'])
    st.plotly_chart(fig, use_container_width=True)

# Function to display a bar chart of goals scored by each team
def display_goals_distribution_bar_chart(df, team1, team2, color_theme):
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=df['home_score'], name=f'{team1} Goals', marker_color=color_theme[0], opacity=0.75))
    fig.add_trace(go.Histogram(x=df['away_score'], name=f'{team2} Goals', marker_color=color_theme[1] if len(color_theme) > 1 else color_theme[0], opacity=0.75))

    fig.update_layout(
        barmode='group',
        title='Goals Scored Distribution',
        xaxis_title='Goals',
        yaxis_title='Count'
    )
    st.plotly_chart(fig, use_container_width=True)

# Function to display a heatmap of goals scored by each team
def display_goals_heatmap(df, team1, team2, color_theme):
    heatmap_data = df.pivot_table(index='home_score', columns='away_score', aggfunc='size', fill_value=0)
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale=color_theme if isinstance(color_theme, list) else 'Viridis'
    ))
    fig.update_layout(
        title=f"Goals Heatmap: {team1} vs {team2}",
        xaxis_title=f"{team2} Goals",
        yaxis_title=f"{team1} Goals"
    )
    st.plotly_chart(fig, use_container_width=True)

# Function to display a detailed match information table
def display_match_details_table(df):
    st.dataframe(df[['date', 'home_team', 'away_team', 'home_score', 'away_score', 'outcome']], use_container_width=True)
