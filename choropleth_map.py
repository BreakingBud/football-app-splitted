import streamlit as st
import plotly.express as px
from data_loader import load_data

# Load the data
goalscorers_df, results_df, shootouts_df = load_data()

# Prepare data for choropleth map
country_metrics = results_df.groupby('country').agg(
    matches=('date', 'count'),
    wins=('outcome', lambda x: (x == results_df['home_team']).sum()),
    draws=('outcome', lambda x: (x == 'Draw').sum())
).reset_index()

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
