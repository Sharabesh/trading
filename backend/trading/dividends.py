from trading.config import *

polygon = api.polygon

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import calendar


def fetch_dividends(sym):
    """Given a symbol returns a dataframe of dividends"""
    symbol_dividends = polygon.dividends(sym)
    fields = ['amount', 'declaredDate', 'exDate', 'indicated', 'paymentDate', 'qualified', 'recordDate', 'symbol',
              'type']
    # Initialize general data structure
    output = {}
    for field in fields:
        output[field] = []

    for dividend in symbol_dividends:
        for field in fields:
            converted = dividend._raw
            try:
                output[field].append(converted[field])
            except:
                output[field].append(np.nan)

    df = pd.DataFrame.from_dict(output)
    for date_field in [x for x in fields if 'Date' in x]:
        df[date_field] = pd.to_datetime(df[date_field])
    return df


def get_current_positions():
    """Get current positions returns a dataframe with columns:
        Date Purchased,
        Purchase Price,
        Quantity Held,
        Ex-dividend date
        Current Price,
        Symbol
    """
    positions = api.list_positions()
    target_columns = ['avg_entry_price', 'current_price', 'symbol', 'qty']

    output = {x: [] for x in target_columns}
    for elem in positions:
        for col in target_columns:
            output[col].append(elem._raw[col])

    return pd.DataFrame.from_dict(output)

def findDay(date):
    born = datetime.strptime(date, '%Y-%M-%d').weekday()
    return (calendar.day_name[born])


def get_next_weeks_dates(weeks = 2):
    """
    :return: a list of dates of the form [2019-Jul-22, ...] for the next week for NASDAQ parsing
    """
    def convert(timestamp):
        conversions = {
            "01": "Jan",
            "02": "Feb",
            "03": "Mar",
            "04": "Apr",
            "05": "May",
            "06": "Jun",
            "07": "Jul",
            "08": "Aug",
            "09": "Sep",
            "10": "Oct",
            "11": "Nov",
            "12": "Dec"
        }
        beginning_time = str(timestamp).split()[0].split("-")
        return f"{beginning_time[0]}-{conversions[beginning_time[1]]}-{beginning_time[2]}"

    output = []
    i = 0
    num_weekends = 0
    while True:
        target_date = datetime.now() + timedelta(i)
        if target_date.weekday() in {5,6}:
            num_weekends += 1
            if num_weekends == weeks:
                break
            continue
        output.append(convert(target_date))
        i += 1
    return output




def load_dividend_targets():
    # Get 1000 top dividend yield stocks
    dividend_data = pd.read_csv("../notebooks/dividend-stocks.csv")
    target_symbols = list(dividend_data.Symbol)

    # Get one weeks worth of future dividends
    DIVIDEND_BASE_URL = "https://www.nasdaq.com/dividend-stocks/dividend-calendar.aspx?date="
    future_dividend_dates = pd.concat([
        pd.read_html(f"{DIVIDEND_BASE_URL + date}")[0] for date in get_next_weeks_dates(4)
    ])
    return future_dividend_dates










def manage_positions():
    """
    Runs continuously and manages existing positions trying to sell
    as soon as a stock is past it's ex-dividend date and has value
    greater than or equal to it's current value
    :return:
    """
    done = None
    while True:
        clock = api.get_clock()
        now = clock.timestamp
        if clock.is_open() and done != now.strftime("%Y-%m-%d"):
            # TODO: Execute trades
            positions = get_current_positions()



