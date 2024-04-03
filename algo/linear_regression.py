import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def linear_regression_forecast(data, steps=180):
    """
    Forecast future values using Linear Regression.

    Parameters:
    - data: Pandas Series of historical closing prices.
    - steps: Number of future steps to forecast.

    Returns:
    - Pandas Series containing the forecasted values with a datetime index.
    """
    # Prepare the features (time) and target (data values)
    X = np.arange(len(data)).reshape(-1, 1)  # Time as the feature
    y = data.values  # Stock prices as the target
    
    # Fit the Linear Regression model
    model = LinearRegression()
    model.fit(X, y)
    
    # Prepare future time points for prediction
    future_X = np.arange(len(data), len(data) + steps).reshape(-1, 1)
    
    # Forecast future stock prices
    forecast = model.predict(future_X)
    
    # Create a pandas Series for the forecasted values with a date index
    future_dates = pd.date_range(start=data.index[-1] + pd.Timedelta(days=1), periods=steps)
    forecast_series = pd.Series(forecast, index=future_dates)
    
    return forecast_series
