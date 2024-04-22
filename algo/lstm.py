from keras.models import Sequential
from keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
import numpy as np

def lstm_forecast(data, forecast_horizon, epochs=10, batch_size=1):
    data = data.values.reshape(-1, 1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)

    # Prepare data for LSTM
    X, y = [], []
    for i in range(len(scaled_data) - batch_size):
        X.append(scaled_data[i:(i + batch_size), 0])
        y.append(scaled_data[i + batch_size, 0])
    X, y = np.array(X), np.array(y)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))
    
    # Build LSTM Model
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(X.shape[1], 1)))
    model.add(LSTM(units=50))
    model.add(Dense(1))
    
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(X, y, epochs=epochs, batch_size=batch_size, verbose=0)
    
    # Predict future values
    predictions = []
    last_batch = scaled_data[-batch_size:]
    current_batch = last_batch.reshape((1, batch_size, 1))
    
    for _ in range(forecast_horizon):
        predicted = model.predict(current_batch, verbose=0)
        current_batch = np.append(current_batch[:, 1:, :], [[predicted]], axis=1)
        predictions.append(predicted.flatten()[0])
    
    predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))
    forecast_dates = pd.date_range(start=data.index[-1], periods=forecast_horizon + 1, freq='B')[1:]
    
    return pd.Series(data=predictions.flatten(), index=forecast_dates)

