import yfinance as yf
import pandas as pd


def fetch_stock_data(ticker, period='1mo'):
    """Берет данные по ценам акций в указанный временной период"""
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    pd.DataFrame(data).to_csv('out.csv', index=True)

    return data


def add_moving_average(data, window_size=5):
    """Вычисляет движение средней MA"""
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()

    return data


def calculate_and_display_average_price(data, period2):
    """вычисляет и выводит среднюю цену закрытия акций за заданный период."""
    data2 = pd.DataFrame(data['Close'])
    # рассчитывает среднее значение по заданному периоду
    data3 = data2.resample(period2).mean()
    data["Average_close"] = data3
    data["Average_close"] = data["Average_close"].ffill()
    print(data)
    # Убирает NaN, если имеется
    data3 = data3.ffill()
    print("_____________________________________")
    print(data3)

    return data3


def notify_if_strong_fluctuations(data, threshold):
    """ анализирует данные и уведомляет
    пользователя, если цена акций колебалась более
    чем на заданный процент за период
    Колебания оцениваются относительно среднего значения
    за рассматриваемый момент времени, сравнение ведется
    к самому низкому или высокому значению и к цене закрытия
    дополнительно появляются два столбца"""
    data["Median"] = (data['High'] + data["Low"]) / 2
    #  Производим сравнение значений цен со средним значением в рамках заданного процента
    data.loc[(1 - data['Median'] / data["High"]) > (threshold / 100), [f"Signal_by_High_Low_{threshold}%"]] = "Yes"
    data.loc[(1 - data["Low"] / data['Median']) > (threshold / 100), [f"Signal_by_High_Low_{threshold}%"]] = "Yes"
    data.loc[(1 - data['Median'] / data["Close"]) > (threshold / 100), [f"Signal_by_Close_{threshold}%"]] = "Yes"
    data.loc[(1 - data["Close"] / data['Median']) > (threshold / 100), [f"Signal_by_Close_{threshold}%"]] = "Yes"

    print(data[f"Signal_by_High_Low_{threshold}%"])
    print("________________________________________")
    print(data[f"Signal_by_Close_{threshold}%"])


def export_data_to_csv(data, filename):
    """Результаты в файл с расширением .csv"""
    pd.DataFrame(data).to_csv(f'{filename}.csv', index=True)

    print(f"Файл {filename} был создан.")


def rsi_func(data, alpha=0.1):
    """ Функция расчитывает индикатор RSI.
    По заданному коэффициенту alpha, который задается
    в пределах от 0 до 1, чем выше коэффициент, тем меньше влияние
    предыдущих значений, расчитывается скользящая экспоненциальная
    средняя ЕМА, благодаря которой расчитывается RSI"""
    delta = data["Close"].diff()
    """Рассчет разницы между двумя близлижайшими значениями цен закрытия
    для определения локального роста или падения цен."""
    up = delta.clip(lower=0)
    down = (- 1) * delta.clip(upper=0)

    ema_u = pd.DataFrame(up).ewm(alpha=alpha, adjust=False).mean()
    ema_d = pd.DataFrame(down).ewm(alpha=alpha, adjust=False).mean()
    data[f"RSI alpha={alpha}"] = 100 * (ema_u / (ema_u + ema_d))
    print(data[f"RSI alpha={alpha}"])

    return data
    