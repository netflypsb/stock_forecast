from tbats import TBATS
import pandas as pd

def tbats_forecast(data, forecast_horizon):
    """
    Forecast future values using the TBATS model, with a dynamic forecast horizon.
    Parameters:
    - data: Pandas Series of historical closing prices.
    - forecast_horizon: Integer specifying the number of days to forecast.
    Returns:
    - Pandas Series containing the forecasted values with a datetime index.
    """
    # Instantiate the TBATS estimator with seasonal periods. Adjust these as necessary.
    estimator = TBATS(seasonal_periods=(7, 365.25), use_trend=True, use_box_cox=False)

    # Fit the model to the historical data
    model = estimator.fit(data)

    # Forecast for the specified horizon
    forecast = model.forecast(steps=forecast_horizon)

    # Creating a pandas Series for the forecast, indexed by future dates
    future_dates = pd.date_range(start=data.index[-1] + pd.Timedelta(days=1), periods=forecast_horizon)
    forecast_series = pd.Series(forecast, index=future_dates)

    return forecast_series
    
