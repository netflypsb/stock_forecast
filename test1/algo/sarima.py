import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX

def sarima_forecast(data, forecast_horizon, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12)):
    """
    Forecast future values using a SARIMA model with a dynamic forecast horizon.

    Parameters:
    - data: Pandas Series of historical closing prices.
    - forecast_horizon: Integer specifying the number of days to forecast.
    - order: The (p, d, q) order of the model for the number of AR parameters, differences, and MA parameters.
    - seasonal_order: The (P, D, Q, s) seasonal order of the model.

    Returns:
    - Pandas Series containing the forecasted values with a datetime index.
    """
    # Fit the SARIMA model
    model = SARIMAX(data, order=order, seasonal_order=seasonal_order, enforce_stationarity=False, enforce_invertibility=False)
    model_fit = model.fit(disp=False)
    
    # Forecast for the specified horizon
    forecast = model_fit.forecast(steps=forecast_horizon)
    
    # Create a pandas Series for the forecasted values with a date index
    future_dates = pd.date_range(start=data.index[-1] + pd.Timedelta(days=1), periods=forecast_horizon)
    forecast_series = pd.Series(forecast, index=future_dates)
    
    return forecast_series
