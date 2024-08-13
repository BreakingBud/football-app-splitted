import pandas as pd
import zipfile
import os
from sklearn.preprocessing import LabelEncoder, StandardScaler

def load_and_preprocess_data(zip_file_path, extract_path):
    # Extract the ZIP file
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    # Load the data from the extracted files
    goalscorers_df = pd.read_csv(os.path.join(extract_path, 'goalscorers.csv'))
    results_df = pd.read_csv(os.path.join(extract_path, 'results.csv'))
    shootouts_df = pd.read_csv(os.path.join(extract_path, 'shootouts.csv'))

    # Filter for FIFA World Cup matches
    results_df = results_df[results_df['tournament'] == 'FIFA World Cup']

    # Encode categorical variables
    categorical_columns = ['home_team', 'away_team', 'country', 'city']
    label_encoders = {}
    for col in categorical_columns:
        le = LabelEncoder()
        results_df[col] = le.fit_transform(results_df[col])
        label_encoders[col] = le

    # Normalize numerical features
    numerical_columns = ['home_score', 'away_score']
    scaler = StandardScaler()
    results_df[numerical_columns] = scaler.fit_transform(results_df[numerical_columns])

    # Feature engineering: add more features as needed
    results_df['goal_difference'] = results_df['home_score'] - results_df['away_score']
    results_df['home_win'] = (results_df['home_score'] > results_df['away_score']).astype(int)

    return results_df, label_encoders, scaler

# Example usage:
# results_df, label_encoders, scaler = load_and_preprocess_data('football_data_matches_scorers_shootouts.zip', '/tmp/extracted_data')
