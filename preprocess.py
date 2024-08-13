import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

def load_and_preprocess_data(data_path):
    goalscorers_df = pd.read_csv(f'{data_path}/goalscorers.csv')
    results_df = pd.read_csv(f'{data_path}/results.csv')
    shootouts_df = pd.read_csv(f'{data_path}/shootouts.csv')

    # Convert 'date' columns to datetime format
    goalscorers_df['date'] = pd.to_datetime(goalscorers_df['date'], errors='coerce')
    results_df['date'] = pd.to_datetime(results_df['date'], errors='coerce')
    shootouts_df['date'] = pd.to_datetime(shootouts_df['date'], errors='coerce')

    # Handle missing values
    goalscorers_df['scorer'].fillna('Unknown', inplace=True)
    goalscorers_df['minute'].fillna(-1, inplace=True)
    shootouts_df['first_shooter'].fillna('None', inplace=True)

    # Encode categorical variables
    label_encoders = {}
    categorical_columns = ['home_team', 'away_team', 'tournament', 'country', 'city']

    for col in categorical_columns:
        le = LabelEncoder()
        results_df[col] = le.fit_transform(results_df[col])
        label_encoders[col] = le

    # Normalize numerical features
    numerical_columns = ['home_score', 'away_score']
    scaler = StandardScaler()

    results_df[numerical_columns] = scaler.fit_transform(results_df[numerical_columns])

    # Create additional features
    results_df['goal_difference'] = results_df['home_score'] - results_df['away_score']
    results_df['home_win'] = (results_df['home_score'] > results_df['away_score']).astype(int)

    return results_df, label_encoders, scaler
