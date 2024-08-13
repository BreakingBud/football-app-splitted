import streamlit as st
import plotly.express as px
from data_loader import load_data

# Load the data
goalscorers_df, results_df, shootouts_df = load_data()

# Set up the choropleth map page
st.title("Choropleth Map")
st.markdown("""
### Global Football Match Insights

Use the map below to visualize the geographic distribution of football matches based on various metrics.
""")

# Dropdown for metric selection
metric = st.selectbox(
    "Select Metric",
    options=["matches", "wins", "draws"],
    index=0
)

# Aggregate matches, wins, and draws by country
country_metrics = results_df.copy()
country_metrics['country'] = country_metrics['home_team']  # Assuming country data is in 'home_team'

country_metrics['win'] = country_metrics.apply(
    lambda row: 1 if row['outcome'] in [row['home_team'], row['away_team']] else 0, axis=1
)
country_metrics['draw'] = country_metrics.apply(
    lambda row: 1 if row['outcome'] == 'Draw' else 0, axis=1
)

country_metrics = country_metrics.groupby('country').agg(
    matches=('date', 'count'),
    wins=('win', 'sum'),
    draws=('draw', 'sum')
).reset_index()

# Generate the choropleth map based on the selected metric
fig = px.choropleth(
    country_metrics,
    locations="country",
    locationmode="country names",
    color=metric,
    hover_name="country",
    color_continuous_scale="Viridis",
    title=f"Distribution of {metric.capitalize()} by Country"
)

# Adjust the layout for larger map size
fig.update_layout(
    margin={"r":0,"t":50,"l":0,"b":0},
    height=600,
    geo=dict(showcoastlines=True)
)

st.plotly_chart(fig, use_container_width=True)
