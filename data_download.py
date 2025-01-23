import yfinance as yf
import pandas as pd


def fetch_stock_data(ticker, period, choise):
    """Берет данные по ценам акций в указанный временной период"""
    pperiod = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
    if choise == 'Y' or choise == 'y':
        """Запрос по датам начала и конца и запись их"""
        stock = yf.Ticker(ticker)
        data = stock.history(interval=period[2], start=period[0], end=period[1])
        pd.DataFrame(data).to_csv('out.csv', index=True)
        return data

    elif choise != 'Y' or choise != 'y':
        """Запрос данных за обозначенный, принятый в программе, период"""
        if period in pperiod:
            stock = yf.Ticker(ticker)
            data = stock.history(period=period)
            pd.DataFrame(data).to_csv('out.csv', index=True)
            return data
        else:
            print("Вы допустили ошибку в вводе данных. Повторите ввод.")

            return None


def add_moving_average(data, window_size=5):
    """Вычисляет движение средней MA"""
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()

    return data


def calculate_and_display_average_price(data, period2):
    """вычисляет и выводит среднюю цену закрытия акций за заданный период."""
    print(data['Close'])
    data2 = pd.DataFrame(data['Close'])
    # рассчитывает среднее значение по заданному периоду
    data3 = data2.resample(period2, origin='end').mean()
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


def chanel_keltner(data, period4):
    """Рассчет канала Кетлера.
     В начале расчитывается типичная цена прайса - средняя цена свечи, рассматриваемого периода,
     потом ценовой диапазон периода,
     затем расчитывается простая скользящая средняя для типичной цены
     и ценового диапазона на промежутке равном десяти рассматриваемым периодам,
     в закалючении производится рассчет верхних и нижних линий канала Кетлера.
     Информация взята с
https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D0%BD%D0%B0%D0%BB_%D0%9A%D0%B5%D0%BB%D1%8C%D1%82%D0%BD%D0%B5%D1%80%D0%B0"""
    data["Type_Price_0"] = (data["High"] + data["Low"] + data["Close"]) / 3
    dat2 = pd.DataFrame(data["Type_Price_0"])
    dat2["Type_Price_t"] = data["Type_Price_0"].resample(period4, origin='end').mean()
    data["Type_Price_t"] = dat2["Type_Price_t"].ffill()
    # Ценовой диапазон
    data["TradingRange_0"] = data["High"] - data["Low"]
    dat3 = pd.DataFrame(data["TradingRange_0"])
    dat3["TradingRange_t"] = data["TradingRange_0"].resample(period4, origin='end').mean()
    data["TradingRange_t"] = dat3["TradingRange_t"].ffill()
    # Простая скользящая средняя для типичной цены и ценового диапазона
    # period5 = 10 * period4 #Для оригинального рассчета канала Кельтнера
    period5 = 2 * period4
    dat4 = pd.DataFrame(data["Type_Price_0"])
    dat4["SMA_10_type_prise"] = data["Type_Price_0"].resample(period5, origin='end').mean()
    data["SMA_10_type_prise"] = dat4["SMA_10_type_prise"].ffill()
    dat5 = pd.DataFrame(data["TradingRange_0"])
    dat5["SMA_10_trading_rang"] = data["TradingRange_0"].resample(period5, origin='end').mean()
    data["SMA_10_trading_rang"] = dat5["SMA_10_trading_rang"].ffill()
    # Рассчет верхних и нижних линий канала
    data["Up_Line_Keltner"] = data["SMA_10_type_prise"] + data["SMA_10_trading_rang"]
    data["Down_Line_Keltner"] = data["SMA_10_type_prise"] - data["SMA_10_trading_rang"]

    return data
