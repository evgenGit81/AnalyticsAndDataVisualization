import data_download as dd
import data_plotting as dplt


def main():
    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print("""Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: 
        AAPL (Apple Inc), GOOGL (Alphabet Inc), MSFT (Microsoft Corporation),
        AMZN (Amazon.com Inc), TSLA (Tesla Inc).""")
    print("""Общие периоды времени для данных о запасах включают:
           1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5г, 10л, с начала года, макс
           (формат ввода: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max).""")
    stock_data = None
    while stock_data is None:
        ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc): ")

        second_request = input("Вы хотите ввести период по начальной и конечной дате (Y/N)? ")
        if second_request == 'Y' or second_request == 'y':
            period = []
            start_p = input("Введите дату начала периода в формате 'YYYY-MM-DD': ")
            period.append(start_p)
            end_p = input("Введите дату конца периода в формате 'YYYY-MM-DD': ")
            period.append(end_p)
            interval_in_p = input("""Введите интервал внутри периода, 
                            принимаемые интервалы - 1м, 2м, 5м, 15м, 30м, 60м, 90м, 1ч, 1д, 5д, 1нед, 1мес,3мес;
                            (вводить в формате - 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo;
                            внутридневные данные не могут распространяться за последние 60 дней): """)
            period.append(interval_in_p)
            stock_data = dd.fetch_stock_data(ticker, period, second_request)

        else:
            period = input("Введите период для данных (например, '1mo' для одного месяца): ")
            # Fetch stock data
            stock_data = dd.fetch_stock_data(ticker, period, second_request)

    # Добавление средних значений за период внутри выше принятого
    period2 = input("""Введите период для расчета среднего значения внутри
                        выбранного периода (например, '3d' для одного месяца): """)
    data3 = dd.calculate_and_display_average_price(stock_data, period2)

    # Add moving average to the data
    stock_data = dd.add_moving_average(stock_data)
    alpha_ = float(input("Введите коэффициент alpha (0 - 1)) для рассчета RSI: "))
    stock_data = dd.rsi_func(stock_data, alpha_)
    # Plot the data
    dplt.create_and_save_plot(stock_data, ticker, period, data3, period2, alpha_)

    print("_________________________________________________")
    threshold = float(input("Введите величину процента колебания цены: "))
    dd.notify_if_strong_fluctuations(stock_data, threshold)

    print("_________________________________________________")
    filename = input("Введите названия файла, для сохранения данных: ")
    filename = filename + f'_{period}' + f'_{period2}' + f'_{alpha_}'
    dd.export_data_to_csv(stock_data, filename)
    input("Нажмите Enter для завершения.")


if __name__ == "__main__":
    main()
