# Crypto Price Prediction App

Streamlit app provides users with a tool for predicting and analyzing cryptocurrency prices using ARIMA models and SMA (Simple Moving Average) analysis. Users can select from various cryptocurrencies, set date ranges, and visualize both historical and predicted data.  
[DEPLOYED WEBSITE LINK](https://cryptit.streamlit.app/)


## Features

- **Real-time Data Fetching**: Fetches live historical cryptocurrency price data from Yahoo Finance.
- **Prediction**: Uses ARIMA and Linear Regression models to predict future prices based on historical data.
- **SMA Analysis**: Calculates short-term and long-term Simple Moving Averages to identify potential buy/sell signals.
- **Interactive UI**: A user-friendly interface built with Streamlit that allows users to input cryptocurrency symbols, date ranges, and customize analysis parameters like SMA windows and prediction steps.
- **Visual Charts**: Displays both historical data and predicted prices on interactive charts.

## Getting Started

To run this application locally, follow these steps:

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/tusharpnwar/Cryptit/
   ```
2. Install the required Python dependencies:
    ```bash
   pip install -r requirements.txt
    ```
3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
   ## Usage

1. **Input Ticker Symbol**: Select a cryptocurrency (e.g., `BTC-USD`, `ETH-USD`, `LTC-USD`) to fetch data for analysis.

2. **Select Date Range**: Set a date range for the historical data you wish to analyze and predict.

3. **Customize SMA Parameters**: Adjust short-term and long-term SMA windows via sliders to tailor the analysis.

4. **Set Prediction Steps**: Use the slider to specify the number of days for price prediction.

5. **Visualize Results**: View historical prices, SMA analysis, and predicted future prices on interactive charts.

