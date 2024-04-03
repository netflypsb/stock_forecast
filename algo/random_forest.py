from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import numpy as np

def create_lagged_features(data, n_lags=5):
    """
    Prepares the dataset with lagged features necessary for Random Forest regression.

    Parameters:
    - data: Pandas Series of historical closing prices.
    - n_lags: The number of lagged observations to create as features.
    
    Returns:
    - A tuple (X, y) where X is a DataFrame of lagged features and y is the original dataset shifted.
    """
    df = pd.DataFrame(data)
    for lag in range(1, n_lags + 1):
        df[f'lag_{lag}'] = df[data.name].shift(lag)
    df.dropna(inplace=True)  # Drop rows with NaN values resulted from shifting
    X = df.drop(columns=[data.name])
    y = df[data.name]
    return X, y

def random_forest_forecast(data, n_lags=5, steps=180):
    """
    Forecast future values using a Random Forest Regressor.

    Parameters:
    - data: Pandas Series of historical closing prices.
    - n_lags: Number of past observations to use for forecasting.
    - steps: Number of future steps to forecast.
    
    Returns:
    - Pandas Series containing the forecasted values with a datetime index.
    """
    X, y = create_lagged_features(data, n_lags)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    # Prepare the data for forecasting
    last_obs = data.tail(n_lags).values[::-1]  # Reverse to get the correct order (most recent first)
    forecasts = []

    for _ in range(steps):
        # Reshape last_obs to match model input shape
        model_input = np.array(last_obs).reshape(1, -1)
        forecast = model.predict(model_input)[0]
        forecasts.append(forecast)

        # Update last_obs with the forecasted value
        last_obs = np.roll(last_obs, -1)
        last_obs[-1] = forecast

    future_dates = pd.date_range(start=data.index[-1] + pd.Timedelta(days=1), periods=steps)
    forecast_series = pd.Series(forecasts, index=future_dates)
    
    return forecast_series
