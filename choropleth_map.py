import streamlit as st
import plotly.express as px
from data_loader import load_data

goalscorers_df, results_df, shootouts_df = load_data()

def show_choropleth_map():
    st.title("Choropleth Map Analysis")
    st.markdown("""
    ### Explore match data geographically
    Use the sliders to filter by year and tournament to see how teams performed geographically.
    """)

    year = st.slider('Select Year', min_value=int(results_df['date'].dt.year.min()), max_value=int(results_df['date'].dt.year.max()))
    tournament = st.selectbox('Select Tournament', ['All'] + sorted(results_df['tournament'].unique().tolist()))

    filtered_df = results_df[
        (results_df['date'].dt.year == year) &
        (results_df['tournament'].str.contains(tournament, case=False, na=False))
    ]

    # Choropleth map to be implemented based on available data and requirements
    fig = px.choropleth(filtered_df, locations='home_team', color='outcome',
                        locationmode='country names', title='Team Performance by Country')
    st.plotly_chart(fig, use_container_width=True)

show_choropleth_map()
