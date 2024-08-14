import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split

def load_and_preprocess_data(zip_file_path, extract_path):
    # Load data from the provided CSV files within the zip archive
    goalscorers_df = pd.read_csv(f'{extract_path}/goalscorers.csv')
    results_df = pd.read_csv(f'{extract_path}/results.csv')
    shootouts_df = pd.read_csv(f'{extract_path}/shootouts.csv')

    # Encode categorical variables
    label_encoders = {}
    categorical_columns = ['home_team', 'away_team', 'tournament']
    for col in categorical_columns:
        le = LabelEncoder()
        if col in results_df.columns:
            results_df[col] = le.fit_transform(results_df[col])
            label_encoders[col] = le

    # Only scale numeric columns that exist in the DataFrame
    numeric_columns = ['home_score', 'away_score']
    scaler = StandardScaler()
    results_df[numeric_columns] = scaler.fit_transform(results_df[numeric_columns])

    # Define features and target variable
    X = results_df[['home_team', 'away_team', 'home_score', 'away_score', 'tournament']].dropna()
    y = (results_df['home_score'] > results_df['away_score']).astype(int)  # 1 if home team wins, 0 otherwise

    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test, label_encoders, scaler, label_encoders.get('home_team', None)
