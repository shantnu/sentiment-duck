import yfinance as yf
import datetime
from datetime import timedelta


def get_finance_data():
    date_today = datetime.date.today()

    yesterday = date_today - timedelta(days = 1)

    date_today = date_today.strftime("%Y-%m-%d")
    yesterday = yesterday.strftime("%Y-%m-%d")

    print("Today = Yesterday was: ", date_today, yesterday)

    # Get the data for the stock AAPL
    data = yf.download('^FTSE','2022-04-14','2022-04-15')

    diff = data['Adj Close'][0] - data['Open'][0]

    change_percent = diff * 100 / data['Adj Close'][0]

    print(f"FTSE change = {diff} percent = {change_percent}")

    return change_percent