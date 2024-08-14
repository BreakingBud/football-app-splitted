import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def show_page(results_df=None):
    st.title("Choropleth Map")
    st.markdown("""
    ### Global Football Match Insights

    Use the map below to visualize the geographic distribution of football matches based on various metrics.
    """)

    # Dropdown for tournament selection
    tournament = st.selectbox(
        "Select Tournament",
        options=["All"] + sorted(results_df['tournament'].unique().tolist()),
        index=0
    )

    # Filter the data by the selected tournament
    if tournament != "All":
        results_df = results_df[results_df['tournament'] == tournament]

    # Dropdown for metric selection
    metric = st.selectbox(
        "Select Metric",
        options=["matches", "wins", "draws", "losses"],
        index=0
    )

    # Dropdown for projection type
    projection_type = st.selectbox(
        "Select Projection Type",
        options=["Orthographic (Spherical)", "Equirectangular (Flat)"],
        index=0
    )

    # Aggregate matches, wins, draws, and losses by country
    country_metrics = results_df.copy()
    country_metrics['country'] = country_metrics['home_team']
    country_metrics['win'] = (country_metrics['home_score'] > country_metrics['away_score']).astype(int)

    # Define metric aggregation
    aggregation_functions = {
        'matches': 'size',
        'wins': 'sum',
        'draws': lambda x: ((x['home_score'] == x['away_score'])).sum(),
        'losses': lambda x: ((x['home_score'] < x['away_score'])).sum()
    }

    # Aggregate data based on the selected metric
    metric_data = country_metrics.groupby('country').agg(aggregation_functions[metric]).reset_index()
    metric_data.columns = ['country', metric]

    # Create the choropleth map
    fig = px.choropleth(
        metric_data,
        locations='country',
        locationmode='country names',
        color=metric,
        projection=projection_type.lower().replace(' (', '_').replace(')', ''),
        title=f'{metric.capitalize()} by Country'
    )

    # Display the map
    st.plotly_chart(fig, use_container_width=True)
