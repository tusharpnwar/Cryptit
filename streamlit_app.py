import streamlit as st
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta

# Function to fetch cryptocurrency data from Yahoo Finance
def fetch_crypto_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

# Function to predict future prices using a simple moving average model for demo purposes
def predict_future(model, data, scaler, future_days=30):
    # This is a placeholder prediction, normally you would use a trained model here
    last_price = data[-1]
    predictions = [last_price * (1 + np.random.normal(0, 0.02)) for _ in range(future_days)]
    predictions = np.array(predictions).reshape(-1, 1)
    
    return scaler.inverse_transform(predictions)

# Function to plot actual and predicted prices
def plot_predictions(dates, actual_prices, predicted_prices):
    # Create the figure and axes
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot the actual prices
    ax.plot(dates, actual_prices, label="Actual Prices", color="blue", marker="o")
    
    # Plot the predicted prices
    ax.plot(dates, predicted_prices, label="Predicted Prices", color="green", marker="x")

    # Set appropriate limits to avoid zooming in too much
    ax.set_xlim([min(dates), max(dates)])
    ax.set_ylim([min(min(actual_prices), min(predicted_prices)), max(max(actual_prices), max(predicted_prices))])

    # Set title and labels
    ax.set_title('Cryptocurrency Price Prediction')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')

    # Add grid and legend
    ax.grid(True)
    ax.legend()

    # Show the main plot
    st.pyplot(fig)

    # Different representations (Bar chart and scatter plot)
    fig, ax2 = plt.subplots(figsize=(10, 6))
    ax2.bar(dates[-len(predicted_prices):], predicted_prices, color='orange', label='Predicted Prices')
    ax2.set_title('Predicted Prices - Bar Chart')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Price')
    ax2.grid(True)
    ax2.legend()
    st.pyplot(fig)

    fig, ax3 = plt.subplots(figsize=(10, 6))
    ax3.scatter(dates[-len(predicted_prices):], predicted_prices, color='red', label='Predicted Prices')
    ax3.set_title('Predicted Prices - Scatter Plot')
    ax3.set_xlabel('Date')
    ax3.set_ylabel('Price')
    ax3.grid(True)
    ax3.legend()
    st.pyplot(fig)

# Main function for the Streamlit app
def main():
    st.title("Cryptocurrency Price Prediction")

    # User input for selecting cryptocurrency and prediction settings
    crypto = st.selectbox('Select Cryptocurrency', ['BTC-USD', 'ETH-USD', 'LTC-USD'])
    start_date = st.date_input('Start Date', datetime.now() - timedelta(days=365))
    end_date = st.date_input('End Date', datetime.now())
    future_days = st.slider('Days to Predict', min_value=1, max_value=60, value=30)

    if st.button('Fetch Data and Predict'):
        # Fetch the cryptocurrency data
        data = fetch_crypto_data(crypto, start_date, end_date)
        st.write(f"Data for {crypto}:")
        st.dataframe(data.tail())  # Show the last few rows of data

        # Prepare the data for prediction
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1, 1))

        # Predict future prices
        model = None  # Replace with your trained model
        future_predictions = predict_future(model, data['Close'].values.reshape(-1, 1), scaler, future_days=future_days)

        # Prepare dates for the prediction graph
        future_dates = pd.date_range(end_date + timedelta(days=1), periods=future_days).to_pydatetime().tolist()

        # Plot the results
        plot_predictions(data.index.to_pydatetime(), data['Close'].values, future_predictions)

if __name__ == '__main__':
    main()
