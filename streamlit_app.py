import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import plotly.graph_objs as go

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

    st.title("📊 Cryptocurrency Price Prediction")
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

    # Slider to view historical data range
    history_days = st.sidebar.slider('Select history view range (days)', min_value=30, max_value=365, value=365)

    # Fetch data from yfinance
    data = yf.download(selected_currency, period=f'{history_days}d', interval='1d')

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

        # Candlestick chart
        st.subheader('Candlestick Chart')
        candlestick = go.Figure(data=[go.Candlestick(x=data.index,
                                                     open=data['Open'],
                                                     high=data['High'],
                                                     low=data['Low'],
                                                     close=data['Close'])])
        candlestick.update_layout(xaxis_rangeslider_visible=False)
        st.plotly_chart(candlestick, use_container_width=True)

        # Predict future prices
        future_predictions = predict_future(model, scaled_data, scaler, future_days=future_days)

        # Display predicted prices
        st.subheader('Predicted Future Prices')
        future_dates = pd.date_range(start=data.index[-1], periods=future_days + 1)[1:]  # Avoid overlap with last actual date
        predicted_df = pd.DataFrame(future_predictions, index=future_dates, columns=['Predicted Price'])
        st.dataframe(predicted_df.style.format('${:.2f}'))

        # Determine if price is increasing or decreasing
        last_actual_price = data['Close'][-1]
        last_predicted_price = future_predictions[-1][0]
        price_change = last_predicted_price - last_actual_price
        price_change_percent = (price_change / last_actual_price) * 100

        # Display predicted price in big, bold format with color based on price direction
        price_direction = "increasing" if price_change > 0 else "decreasing"
        price_color = "green" if price_change > 0 else "red"
        st.subheader(f"🔮 Predicted Price for {selected_currency} in {future_days} Days:")
        st.markdown(f"<h2 style='text-align: center; color: {price_color};'>${last_predicted_price:.2f} ({price_direction}, {price_change_percent:.2f}%)</h2>", unsafe_allow_html=True)

        # Show additional features like volume and market cap
        st.subheader('Additional Metrics')
        st.write(f"**Volume:** {data['Volume'][-1]:,.0f}")
        st.write(f"**Market Cap Estimate:** {(data['Close'][-1] * data['Volume'][-1]):,.0f} USD")

        # Download option for data
        csv = data.to_csv(index=True)
        st.download_button(label="Download Historical Data as CSV", data=csv, file_name=f'{selected_currency}_historical_data.csv', mime='text/csv')

        # Footer with "Made by"
        st.markdown("""
            <hr>
            <div style='text-align: center;'>
                <strong>Made by Tushar Panwar</strong>
            </div>
        """, unsafe_allow_html=True)
        
    else:
        st.error("Failed to retrieve data. Please try again later.")

if __name__ == "__main__":
    main()
