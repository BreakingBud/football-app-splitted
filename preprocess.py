import pandas as pd
import zipfile
import os

def load_and_preprocess_data(zip_file_path, extract_path):
    # Extract the ZIP file
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    # Load the data from the extracted files
    goalscorers_df = pd.read_csv(os.path.join(extract_path, 'goalscorers.csv'))
    results_df = pd.read_csv(os.path.join(extract_path, 'results.csv'))
    shootouts_df = pd.read_csv(os.path.join(extract_path, 'shootouts.csv'))

    # Example preprocessing steps (you can add more based on your needs)
    goalscorers_df['date'] = pd.to_datetime(goalscorers_df['date'], errors='coerce')
    results_df['date'] = pd.to_datetime(results_df['date'], errors='coerce')
    shootouts_df['date'] = pd.to_datetime(shootouts_df['date'], errors='coerce')

    # Handle missing values and other preprocessing steps
    goalscorers_df['scorer'].fillna('Unknown', inplace=True)
    goalscorers_df['minute'].fillna(-1, inplace=True)
    shootouts_df['first_shooter'].fillna('None', inplace=True)

    # Additional preprocessing like encoding or scaling can go here

    return goalscorers_df, results_df, shootouts_df

# Usage example:
# load_and_preprocess_data('football_data_matches_scorers_shootouts.zip', '/tmp/extracted_data')
