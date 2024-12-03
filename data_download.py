import yfinance as yf
import pandas as pd


def fetch_stock_data(ticker, period='1mo'):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    # print(data)
    # pd.DataFrame(data).to_csv('out.csv', index=True)
    return data

def add_moving_average(data, window_size=5):
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data

def calculate_and_display_average_price(data, period2):
    data2 = pd.DataFrame(data['Close'])
    data3 = data2.resample(period2).mean() # рассчитывает среднее значение по заданному периоду
    data3 = data3.ffill() # Убирает NaN, если имеется
    # print(data3)
    return data3
