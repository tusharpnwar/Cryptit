import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

# Placeholder for your model prediction function
def predict_future(model, data, scaler, future_days):
    # Dummy predictions for illustration (replace with your actual model prediction)
    last_value = data[-1]
    predictions = [last_value + i for i in range(1, future_days + 1)]
    predictions = np.array(predictions).reshape(-1, 1)
    return scaler.inverse_transform(predictions)

# Placeholder model (replace with your actual model)
model = None

def main():
    st.set_page_config(page_title="Crypto Price Prediction", page_icon="📈", layout="wide")

    st.title("📊 Cryptocurrency Price Prediction Using LSTM")
    st.write("""
        Welcome to the Crypto Price Prediction app! You can select a cryptocurrency and predict future prices using historical data.
        This tool fetches real-time data from the web and predicts future prices for various cryptocurrencies.
        Adjust the slider below to predict prices for the next few days.
    """)

    # Select cryptocurrency
    st.sidebar.header('User Input Parameters')
    currencies = ['BTC-USD', 'ETH-USD', 'LTC-USD', 'XRP-USD', 'DOGE-USD']
    selected_currency = st.sidebar.selectbox('Select Cryptocurrency', currencies)

    # Slider to select the number of future days to predict
    future_days = st.sidebar.slider('Number of days to predict', min_value=1, max_value=30, value=7)

    # Fetch data from yfinance
    data = yf.download(selected_currency, period='1y', interval='1d')

    if not data.empty:
        # Display a preview of the data
        st.subheader(f'Historical Data for {selected_currency}')
        st.write(data.tail())

        # Initialize and fit the scaler with the 'Close' price data
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1, 1))

        # Display historical data chart
        st.subheader('Historical Price Data')
        st.line_chart(data['Close'], use_container_width=True)

        # Predict future prices
        future_predictions = predict_future(model, scaled_data, scaler, future_days=future_days)

        # Display predicted prices
        st.subheader('Predicted Future Prices')
        future_dates = pd.date_range(start=data.index[-1], periods=future_days + 1)[1:]  # Avoid overlap with last actual date
        predicted_df = pd.DataFrame(future_predictions, index=future_dates, columns=['Predicted Price'])
        st.dataframe(predicted_df.style.format('${:.2f}'))

        # Plot predicted prices
        st.subheader(f"Price Prediction for the Next {future_days} Days")
        plt.figure(figsize=(10, 5))
        plt.plot(data.index[-100:], data['Close'][-100:], label='Historical Price', color='blue', linewidth=2)
        plt.plot(predicted_df.index, predicted_df['Predicted Price'], label='Predicted Price', color='red', linestyle='--', linewidth=2)
        plt.xlabel('Date')
        plt.ylabel('Price (USD)')
        plt.title(f'{selected_currency} Price Prediction for the Next {future_days} Days')
        plt.legend()
        plt.grid(True)
        st.pyplot(plt)

        # Footer
        st.markdown("""
            **Note:** The predictions are generated using a basic model and are for illustration purposes only. 
            The accuracy of the model may vary based on various factors including market conditions.
        """, unsafe_allow_html=True)
    else:
        st.error("Failed to retrieve data. Please try again later.")

if __name__ == "__main__":
    main()
