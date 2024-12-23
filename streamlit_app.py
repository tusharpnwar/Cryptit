import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mdates
from statsmodels.tsa.arima.model import ARIMA
from sklearn.linear_model import LinearRegression

# Function to fit the ARIMA model and predict future prices
def predict_future(data, order, future_days):
    model = ARIMA(data, order=order)
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=future_days)
    return forecast

# Function to calculate moving averages
def calculate_sma(data, window):
    return data.rolling(window=window).mean()

def main():
    st.set_page_config(page_title="Crypto Price Prediction", page_icon="📈", layout="wide")

    st.title("📊 Cryptocurrency Price Prediction")
    st.write("""
        Welcome to the Crypto Price Prediction app! You can select a cryptocurrency and predict future prices using historical data.
        This tool fetches real-time data from the web and predicts future prices for various cryptocurrencies using LSTM model.
    """)

    # Select cryptocurrency
    st.sidebar.header('User Input Parameters')
    currencies = ['BTC-USD', 'ETH-USD', 'LTC-USD', 'XRP-USD', 'DOGE-USD']
    selected_currency = st.sidebar.selectbox('Select Ticker Symbol', currencies)

    # Select date range
    start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2022-01-01"))
    end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("today"))

    # Slider for SMA parameters
    st.sidebar.subheader('SMA Parameters')
    short_sma_window = st.sidebar.slider('Short SMA Window:', min_value=1, max_value=100, value=20)
    long_sma_window = st.sidebar.slider('Long SMA Window:', min_value=1, max_value=200, value=50)

    # Slider for prediction steps
    prediction_steps = st.sidebar.slider('Prediction Steps (Days):', min_value=1, max_value=30, value=7)

    # Fetch data from yfinance
    data = yf.download(selected_currency, start=start_date, end=end_date, interval='1d')

    if not data.empty:
        # Display a preview of the data
        st.subheader(f'Historical Data for {selected_currency}')
        st.write(data.tail())

        # Calculate and plot moving averages
        data['Short SMA'] = calculate_sma(data['Close'], short_sma_window)
        data['Long SMA'] = calculate_sma(data['Close'], long_sma_window)

        # Display historical data chart
        st.subheader('Historical Price Data with SMAs')
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(data.index, data['Close'], label='Close Price', color='blue', linewidth=2)
        ax.plot(data.index, data['Short SMA'], label=f'Short SMA ({short_sma_window})', color='orange', linestyle='--')
        ax.plot(data.index, data['Long SMA'], label=f'Long SMA ({long_sma_window})', color='green', linestyle='--')
        plt.xlabel('Date')
        plt.ylabel('Price (USD)')
        plt.title(f'{selected_currency} Historical Price with SMAs')
        plt.legend()
        plt.grid(True)
        st.pyplot(fig)

        # Prepare data for prediction
        model_data = data[['Close']].dropna()
        model_data['Days'] = np.arange(len(model_data))

        # Fit Linear Regression model for prediction
        lr_model = LinearRegression()
        lr_model.fit(model_data['Days'].values.reshape(-1, 1), model_data['Close'].values)

        # Predict future prices
        future_days = np.arange(len(model_data), len(model_data) + prediction_steps).reshape(-1, 1)
        future_prices = lr_model.predict(future_days)

        # Create a DataFrame for predicted prices
        future_dates = pd.date_range(start=data.index[-1] + pd.Timedelta(days=1), periods=prediction_steps)
        predicted_df = pd.DataFrame(future_prices, index=future_dates, columns=['Predicted Price'])

        # Display predicted prices
        st.subheader('Predicted Future Prices')
        st.dataframe(predicted_df.style.format('${:.2f}'))

        # Plot predicted prices on line graph
        st.subheader(f"Price Prediction for the Next {prediction_steps} Days")
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(data.index, data['Close'], label='Historical Price', color='blue', linewidth=2)
        ax.plot(predicted_df.index, predicted_df['Predicted Price'], label='Predicted Price', color='red', linestyle='--', linewidth=2)
        plt.xlabel('Date')
        plt.ylabel('Price (USD)')
        plt.title(f'{selected_currency} Price Prediction for the Next {prediction_steps} Days')
        plt.legend()
        plt.grid(True)
        st.pyplot(fig)

        # Footer
        st.markdown("""---""")
        st.markdown("""Made by TUSHAR PANWAR 21BCE1074
PRITHVI RAJ DIXIT 21BCE5359
GARVIT BANSAL 21BCE55773
under the guidence of Dr.Punitha K
        """, unsafe_allow_html=True)
        st.markdown("""**Note:** The accuracy of the model may vary based on various factors including market conditions.
        """, unsafe_allow_html=True)

      

    else:
        st.error("Failed to retrieve data. Please try again later.")

if __name__ == "__main__":
    main()
