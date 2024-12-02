import yfinance as yf
import pandas as pd


def fetch_stock_data(ticker, period='1mo'):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    print(data)
    pd.DataFrame(data).to_csv('out.csv', index=False)
    return data

def calculate_and_display_average_price(data):


def add_moving_average(data, window_size=5):
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data
