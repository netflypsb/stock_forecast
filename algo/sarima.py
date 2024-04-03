import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX

def sarima_forecast(data, order=(1,1,1), seasonal_order=(1,1,1,12), steps=180):
    """
    Forecast future values using a SARIMA model.

    Parameters:
    - data: Pandas Series of historical closing prices.
    - order: The (p,d,q) order of the model for the number of AR parameters, differences, and MA parameters.
    - seasonal_order: The (P,D,Q,s) seasonal order of the model.
    - steps: Number of future steps to forecast.

    Returns:
    - Pandas Series containing the forecasted values with a datetime index.
    """
    # Fit the SARIMA model
    model = SARIMAX(data, order=order, seasonal_order=seasonal_order, enforce_stationarity=False, enforce_invertibility=False)
    model_fit = model.fit(disp=False)
    
    # Forecast
    forecast = model_fit.forecast(steps=steps)
    
    # Create a pandas Series for the forecasted values with a date index
    future_dates = pd.date_range(start=data.index[-1] + pd.Timedelta(days=1), periods=steps)
    forecast_series = pd.Series(forecast, index=future_dates)
    
    return forecast_series
