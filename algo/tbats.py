from tbats import TBATS
import pandas as pd

def tbats_forecast(data):
    """
    Forecast future values using the TBATS model.

    Parameters:
    - data: Pandas Series of historical closing prices.
    
    Returns:
    - Pandas Series containing the forecasted values with a datetime index.
    """
    # Instantiate the TBATS estimator
    # Note: You may adjust seasonal_periods based on domain knowledge or prior analysis
    estimator = TBATS(seasonal_periods=(7, 365.25), use_trend=True, use_box_cox=False)

    # Fit the model
    model = estimator.fit(data)
    
    # Forecast the next 180 days
    forecast = model.forecast(steps=180)
    
    # Create a pandas Series for the forecasted values with a date index
    future_dates = pd.date_range(start=data.index[-1] + pd.Timedelta(days=1), periods=180)
    forecast_series = pd.Series(forecast, index=future_dates)
    
    return forecast_series
