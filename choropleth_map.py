import streamlit as st
import pandas as pd
import plotly.express as px
from data_loader import load_data

# Load the data
goalscorers_df, results_df, shootouts_df = load_data()

def show_choropleth_map():
    st.title("Choropleth Map")
    st.markdown("""
    ### Geographic Distribution of Match Results
    Visualize the distribution of match outcomes across different countries.
    """)

    # Select the metric for the map
    metric = st.selectbox('Select Metric', ['Total Matches', 'Wins', 'Losses', 'Draws'])

    # Aggregate data for the choropleth map
    results_df['home_win'] = (results_df['home_score'] > results_df['away_score']).astype(int)
    results_df['away_win'] = (results_df['away_score'] > results_df['home_score']).astype(int)
    results_df['draw'] = (results_df['home_score'] == results_df['away_score']).astype(int)
    
    country_stats = results_df.groupby('home_team').agg(
        total_matches=pd.NamedAgg(column='home_score', aggfunc='count'),
        wins=pd.NamedAgg(column='home_win', aggfunc='sum'),
        losses=pd.NamedAgg(column='away_win', aggfunc='sum'),
        draws=pd.NamedAgg(column='draw', aggfunc='sum')
    ).reset_index()

    if metric == 'Total Matches':
        fig = px.choropleth(country_stats, locations='home_team', locationmode='country names',
                            color='total_matches', hover_name='home_team',
                            color_continuous_scale='Viridis',
                            title='Total Matches per Country')
    elif metric == 'Wins':
        fig = px.choropleth(country_stats, locations='home_team', locationmode='country names',
                            color='wins', hover_name='home_team',
                            color_continuous_scale='Blues',
                            title='Total Wins per Country')
    elif metric == 'Losses':
        fig = px.choropleth(country_stats, locations='home_team', locationmode='country names',
                            color='losses', hover_name='home_team',
                            color_continuous_scale='Reds',
                            title='Total Losses per Country')
    else:
        fig = px.choropleth(country_stats, locations='home_team', locationmode='country names',
                            color='draws', hover_name='home_team',
                            color_continuous_scale='Greens',
                            title='Total Draws per Country')

    st.plotly_chart(fig, use_container_width=True)

show_choropleth_map()
