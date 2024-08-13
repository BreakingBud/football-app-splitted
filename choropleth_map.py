import streamlit as st
import pandas as pd
import plotly.express as px
from data_loader import load_data

# Load the data
goalscorers_df, results_df, shootouts_df = load_data()

def show_choropleth_map():
    st.title("Choropleth Map")

    st.markdown("""
    ### Global Football Match Insights
    Use the map below to visualize the geographic distribution of football matches based on various metrics.
    """)

    # Aggregate data for the map
    map_data = results_df.groupby('tournament')['home_team'].count().reset_index()
    map_data.columns = ['Tournament', 'Match Count']

    # Create a choropleth map
    fig = px.choropleth(
        map_data,
        locations='Tournament',
        locationmode='country names',
        color='Match Count',
        hover_name='Tournament',
        color_continuous_scale=px.colors.sequential.Plasma,
        title="Distribution of Matches by Tournament Location",
        projection='natural earth'
    )

    # Adjust the layout to make the map larger
    fig.update_layout(
        width=1200,  # Adjust width
        height=800,  # Adjust height
        margin={"r":0,"t":50,"l":0,"b":0},  # Remove margins
    )

    st.plotly_chart(fig, use_container_width=True)

show_choropleth_map()
