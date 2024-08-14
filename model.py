from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

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
        model.fit(X_train, y_train, epochs=10, batch_size=16, validation_split=0.2, verbose=1)  # Reduced epochs and batch size
    except BrokenPipeError as e:
        print(f"Broken pipe error encountered: {e}")
    except Exception as e:
        print(f"An error occurred during model training: {e}")
    
    return model
