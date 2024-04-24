import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from authentication import is_subscriber_authorized, fetch_subscribers

# Importing forecasting algorithms from the algo directory
from algo.sarima import sarima_forecast
from algo.linear_regression import linear_regression_forecast
from algo.tbats import tbats_forecast
from algo.random_forest import random_forest_forecast
from algo.lstm import lstm_forecast

# Set up Streamlit configuration
st.set_page_config(page_title="netflypsb", page_icon="logo.png", menu_items=None)

# Initialize subscribers list on app load
subscribers = fetch_subscribers()

def main():
    st.write("# Stocks Forecast")
    st.markdown("""
    ## 🚀📝 Forecast Future Stock Price Movement 
    🌟 This app predicts 2 things: future price trajectory and future price
    ## How to use it? 🎉
    - **1. Choose a ticker**: Write the ticker symbol for the stock you want to trade/invest. Refer to yahoo finance for the ticker 📝
    - **2. Choose analysis length**: Pick the start date and the end date for the data you want to use in the prediction. More is not necessarily better! 🏥
    - **3. Choose horizon**: How far into the future do you want the app to predict. Shorter is mathematically better!
    - **4. Choose prediction day**: Choose ONE (1) day within the horizon that you picked in step 3. to see the predicted price for that day. 🔍
    - **5. Choose forecast models**: More is not necessarily better but usually takes longer.
    - **6. Press Analyze** 🚀🎉
    - **7. Wait a bit**: It may take some time. Watch the running guy on the top right 🤗
    - **8. Do your due diligence**: Don't believe everything. Do your own research. This app may be one of your tools but YOU decide.
    ## Let's Connect! 🌐
    - If you liked this app, see my other projects at:
      - [☕ My Buy Me a Coffee Page](https://www.buymeacoffee.com/magister)
      - [🤗 My Huggingface Page](https://huggingface.co/netflypsb)
      - [🐦 My X Account](https://twitter.com/VeloVates)
    """)
    
    # Authentication block
    st.sidebar.title("Subscriber Login")
    email = st.sidebar.text_input("Enter your email:")
    if st.sidebar.button("Login"):
        if is_subscriber_authorized(email, "Premium Plan", subscribers):
            st.session_state['authenticated'] = True
        else:
            st.sidebar.error("Access denied. Please ensure you are subscribed to the correct plan.")

    # Ensuring only authenticated users can access the forecasting functionality
    if 'authenticated' in st.session_state and st.session_state['authenticated']:
        perform_forecasting()
    else:
        st.warning("Please log in to access the forecasting features.")

def perform_forecasting():
    # Sidebar UI for input parameters
    ticker = st.sidebar.text_input('Enter Ticker Symbol', 'AAPL')
    start_date = st.sidebar.date_input('Select Start Date', value=pd.to_datetime('2020-01-01'))
    end_date = st.sidebar.date_input('Select End Date', value=pd.to_datetime('2023-01-01'))
    forecast_horizon = st.sidebar.number_input('Forecast Horizon (days)', min_value=1, value=180)
    forecast_date = st.sidebar.date_input('Forecast Date', min_value=end_date, value=end_date + pd.Timedelta(days=180))
    options = st.sidebar.multiselect('Select forecasting models to use',
                                     ['SARIMA', 'Linear Regression', 'TBATS', 'Random Forest', 'LSTM'],
                                     ['SARIMA', 'Linear Regression'])

    if st.sidebar.button('Analyze'):
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
        if 'LSTM' in options:
            forecasts['LSTM'] = lstm_forecast(data, forecast_horizon)

        plot_forecasts(data, forecasts, f"Forecasted Stock Prices for {ticker}")

        # Output the forecasted price for the selected date, if available
        forecast_date_str = forecast_date.strftime('%Y-%m-%d')
        for model_name, forecast in forecasts.items():
            if forecast_date_str in forecast.index:
                st.write(f"Forecasted price by {model_name} on {forecast_date_str}: {forecast.loc[forecast_date_str]:.2f}")

if __name__ == "__main__":
    main()
