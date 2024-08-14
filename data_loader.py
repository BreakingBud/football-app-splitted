import streamlit as st
import pandas as pd
import os
import zipfile

# Define the file path and extraction directory
zip_file_path = 'football_data_matches_scorers_shootouts.zip'
extraction_dir = 'data/football_data/'

# Extract the zip file function
def extract_zip_file(zip_path, extract_to):
    if not os.path.exists(extract_to):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)

# Extract the data
extract_zip_file(zip_file_path, extraction_dir)

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

    return goalscorers_df, merged_df, shootouts_df
