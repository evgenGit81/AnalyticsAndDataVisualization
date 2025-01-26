import matplotlib.pyplot as plt
import pandas as pd
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def create_and_save_plot(data, ticker, period, data3, period2, period4, alpha_, num_style, filename=None):
    fig = plt.figure(figsize=(10, 10))
    plt.style.use(plt.style.available[num_style])
    # Добавлено дополнительное поле для построения RSI
    ax1 = fig.add_axes((0.1, 0.5, 0.8, 0.4))
    ax2 = fig.add_axes((0.1, 0.1, 0.8, 0.3), ylim=(0, 110))

    if 'Date' not in data:
        if pd.api.types.is_datetime64_any_dtype(data.index):
            dates = data.index.to_numpy()
            dates2 = data3.index.to_numpy()
            ax1.plot(dates, data['Close'].values, label='Close Price')
            ax1.plot(dates, data['Moving_Average'].values, label='Moving Average')
            # добавлен
            ax1.plot(dates2, data['Average_close'].values, label=f'Среднее значение периода {period2}')
            ax1.plot(dates, data['Up_Line_Keltner'].values,
                     label=f'Верхняя линия канала Кельтнера с периодом {period4}', linestyle='-.')
            ax1.plot(dates, data['Down_Line_Keltner'].values,
                     label=f'Нижняя линия канала Кельтнера с периодом {period4}', linestyle='-.')
            ax1.plot(dates, data['Type_Price_t'].values,
                     label=f'Типичная цена канала Кельтнера с периодом {period4}', linestyle='-.')
            ax2.plot(dates, data[f"RSI alpha={alpha_}"].values, label=f"RSI alpha={alpha_}")
        else:
            print("Информация о дате отсутствует или не имеет распознаваемого формата.")
            return
    else:
        if (not pd.api.types.is_datetime64_any_dtype(data['Date'])
                and not pd.api.types.is_datetime64_any_dtype(data3['Date'])):
            data['Date'] = pd.to_datetime(data['Date'])
            data3['Date'] = pd.to_datetime(data3['Date'])
        ax1.plot(data['Date'], data['Close'], label='Close Price')
        ax1.plot(data['Date'], data['Moving_Average'], label='Moving Average')
        # добавлен
        ax1.plot(data3['Date'], data['Average_close'].values, label=f'Среднее значение периода {period2}')
        ax1.plot(data['Date'], data['Down_Line_Keltner'].values,
                 label=f'Нижняя линия канала Кельтнера с периодом {period4}', linestyle='-.')
        ax1.plot(data['Date'], data['Up_Line_Keltner'].values,
                 label=f'Верхняя линия канала Кельтнера с периодом {period4}', linestyle='-.')
        ax1.plot(data['Date'], data['Type_Price_t'].values,
                 label=f'Типичная цена канала Кельтнера с периодом {period4}', linestyle='-.')
        ax2.plot(data['Date'], data[f"RSI alpha={alpha_}"].values, label=f"RSI alpha={alpha_}")

    ax1.set_title(f"{ticker} Цена акций с течением времени", fontsize=11)
    ax1.legend()
    ax1.grid(True)
    ax2.set_title(f"RSI alpha={alpha_}", fontsize=11)
    ax2.legend()
    ax2.grid(True)
    if filename is None:
        filename = f"{ticker}_{period}_{period2}_{alpha_}_price_chart.png"
    fig.savefig(filename)
    print(f"График сохранен как {filename}")
    plt.show()


def interactiv_graf(data, ticker, filename, period2, period4, alpha_):
    """Функция извлекает данные из csv-файла с рассчетами данные
    и строит нтерактивный график, а также сохраняет его."""
    # fgraf = go.Figure()
    fgraf = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.2)
    dates = data.index.to_numpy()
    fgraf.add_trace(go.Scatter(x=dates, y=data['Close'], name=f"{ticker} Close"), 1, 1)
    fgraf.add_trace(go.Scatter(x=dates, y=data['Moving_Average'], name=f"{ticker} MA"), 1, 1)
    fgraf.add_trace(go.Scatter(x=dates, y=data['Average_close'], name=f'Среднее значение периода {period2}'), 1, 1)
    fgraf.add_trace(go.Scatter(x=dates, y=data['Down_Line_Keltner'],
                               name=f'Нижняя линия канала Кельтнера с периодом {period4}'), 1, 1)
    fgraf.add_trace(go.Scatter(x=dates, y=data['Up_Line_Keltner'],
                               name=f'Верхняя линия канала Кельтнера с периодом {period4}'), 1, 1)
    fgraf.add_trace(go.Scatter(x=dates, y=data['Type_Price_t'],
                               name=f'Типичная цена канала Кельтнера с периодом {period4}'), 1, 1)
    fgraf.add_trace(go.Scatter(x=dates, y=data[f'RSI alpha={alpha_}'], name=f"{ticker} RSI"), 2, 1)

    # свойства графика
    fgraf.update_layout(
        title_text=f'Финансы компании "{ticker}"',
        title_font_size=20,
        yaxis_title='Стоимость',
        xaxis_rangeslider_visible=True
    )
    fgraf.show()
    # сохраняем в файл html график
    plotly.offline.plot(fgraf, filename=f'{filename}.html', auto_open=False)
