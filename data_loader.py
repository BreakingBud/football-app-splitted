import streamlit as st
import pandas as pd
import os
import zipfile

# Define the file path and extraction directory
zip_file_path = 'football_data_matches_scorers_shootouts.zip'
extraction_dir = 'data/football_data/'

# Extract the zip file if it hasn't been extracted yet
if not os.path.exists(extraction_dir):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extraction_dir)

# Utility function to load datasets
@st.cache_data
def load_data():
    goalscorers_df = pd.read_csv(os.path.join(extraction_dir, 'goalscorers.csv'))
    results_df = pd.read_csv(os.path.join(extraction_dir, 'results.csv'))
    shootouts_df = pd.read_csv(os.path.join(extraction_dir, 'shootouts.csv'))

    results_df['date'] = pd.to_datetime(results_df['date'])
    shootouts_df['date'] = pd.to_datetime(shootouts_df['date'])

    results_df['outcome'] = results_df.apply(
        lambda row: row['home_team'] if row['home_score'] > row['away_score']
        else row['away_team'] if row['away_score'] > row['home_score'] else 'Draw',
        axis=1
    )

    merged_df = results_df.merge(
        shootouts_df[['date', 'home_team', 'away_team', 'winner']],
        on=['date', 'home_team', 'away_team'], 
        how='left'
    )
    merged_df['shootout'] = merged_df['winner'].notna()

    # Aggregate matches, wins, and draws by country
    country_metrics = merged_df.groupby('country').agg(
        matches=('date', 'count'),
        wins=('outcome', lambda x: ((x == merged_df.loc[x.index, 'home_team']) | (x == merged_df.loc[x.index, 'away_team'])).sum()),
        draws=('outcome', lambda x: (x == 'Draw').sum())
    ).reset_index()

    return goalscorers_df, merged_df, shootouts_df, country_metrics
