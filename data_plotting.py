import matplotlib.pyplot as plt
import pandas as pd
import data_download as dd


def create_and_save_plot(data, ticker, period, data3, period2, filename=None):
    plt.figure(figsize=(10, 6))

    if 'Date' not in data:
        if pd.api.types.is_datetime64_any_dtype(data.index):
            dates = data.index.to_numpy()
            dates2 = data3.index.to_numpy()
            plt.plot(dates, data['Close'].values, label='Close Price')
            plt.plot(dates, data['Moving_Average'].values, label='Moving Average')
            plt.plot(dates2, data3['Close'].values, label=f'Среднее значение периода {period2}') # добавлен
        else:
            print("Информация о дате отсутствует или не имеет распознаваемого формата.")
            return
    else:
        if (not pd.api.types.is_datetime64_any_dtype(data['Date'])
                and not pd.api.types.is_datetime64_any_dtype(data3['Date'])):
            data['Date'] = pd.to_datetime(data['Date'])
            data3['Date'] = pd.to_datetime(data3['Date'])
        plt.plot(data['Date'], data['Close'], label='Close Price')
        plt.plot(data['Date'], data['Moving_Average'], label='Moving Average')
        plt.plot(data3['Date'], data3['Close'].values, label=f'Среднее значение {period2}') #добавлен
    plt.title(f"{ticker} Цена акций с течением времени")
    plt.xlabel("Дата")
    plt.ylabel("Цена")
    plt.legend()

    if filename is None:
        filename = f"{ticker}_{period}_{period2}stock_price_chart.png"

    plt.savefig(filename)
    print(f"График сохранен как {filename}")
