from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
import numpy as np

def train_model(X_train, y_train, input_dim):
    model = Sequential([
        Dense(64, input_dim=input_dim, activation='relu'),
        Dropout(0.5),
        Dense(32, activation='relu'),
        Dropout(0.5),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    try:
        model.fit(X_train, y_train, epochs=10, batch_size=16, validation_split=0.2, verbose=1)
    except Exception as e:
        print(f"An error occurred during model training: {e}")
    
    return model

def predict_match(home_team, away_team, model, label_encoders, scaler):
    try:
        home_team_encoded = label_encoders['home_team'].transform([home_team])[0]
        away_team_encoded = label_encoders['away_team'].transform([away_team])[0]
        tournament_encoded = label_encoders['tournament'].transform(['FIFA World Cup'])[0]  # Example
        X = np.array([[home_team_encoded, away_team_encoded, 0, 0, tournament_encoded]])  # Adjust features accordingly
        X_scaled = scaler.transform(X)
        prediction = model.predict(X_scaled)
        return int(np.round(prediction[0][0]))
    except Exception as e:
        st.error(f"Error predicting match {home_team} vs {away_team}: {e}")
