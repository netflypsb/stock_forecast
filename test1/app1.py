import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

# Importing forecasting algorithms from the algo directory
from algo.sarima import sarima_forecast
from algo.linear_regression import linear_regression_forecast
from algo.tbats import tbats_forecast
from algo.random_forest import random_forest_forecast

# Function to fetch stock data
def fetch_stock_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data['Close']

# Function to plot forecasts
def plot_forecasts(data, forecasts, title='Stock Price Forecast'):
    plt.figure(figsize=(10, 6))
    plt.plot(data.index, data, label='Historical Prices', color='black', alpha=0.75)
    
    for name, forecast in forecasts.items():
        plt.plot(forecast.index, forecast, label=name)
    
    if len(forecasts) > 1:
        combined_forecast = pd.concat(forecasts.values()).groupby(level=0).mean()
        plt.plot(combined_forecast.index, combined_forecast, label='Combined Forecast', color='red', linestyle='--')
    
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    st.pyplot(plt)

# Streamlit UI
st.title("Stock Forecasting App")

ticker = st.text_input('Enter Ticker Symbol', 'AAPL')
start_date = st.date_input('Select Start Date', value=pd.to_datetime('2020-01-01'))
end_date = st.date_input('Select End Date', value=pd.to_datetime('2023-01-01'))
forecast_horizon = st.number_input('Forecast Horizon (days)', min_value=1, value=180)
forecast_date = st.date_input('Forecast Date', min_value=end_date, value=end_date + pd.Timedelta(days=180))

# User selects which forecasting models to use
options = st.multiselect('Select forecasting models to use',
                         ['SARIMA', 'Linear Regression', 'TBATS', 'Random Forest'],
                         ['SARIMA', 'Linear Regression'])

if st.button('Analyze'):
    data = fetch_stock_data(ticker, start_date, end_date)
    forecasts = {}
    
    if 'SARIMA' in options:
        forecasts['SARIMA'] = sarima_forecast(data, forecast_horizon)
    if 'Linear Regression' in options:
        forecasts['Linear Regression'] = linear_regression_forecast(data, forecast_horizon)
    if 'TBATS' in options:
        forecasts['TBATS'] = tbats_forecast(data, forecast_horizon)
    if 'Random Forest' in options:
        forecasts['Random Forest'] = random_forest_forecast(data, forecast_horizon)
    
    plot_forecasts(data, forecasts, f"Forecasted Stock Prices for {ticker}")
    
    # Output the forecasted price for the selected date, if available
    forecast_date_str = forecast_date.strftime('%Y-%m-%d')
    for model_name, forecast in forecasts.items():
        if forecast_date_str in forecast.index:
            st.write(f"Forecasted price by {model_name} on {forecast_date_str}: {forecast.loc[forecast_date_str]:.2f}")
