from config import *

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

        # Ignore weekends
        if target_date.weekday() in {5,6}:
            num_weekends += 1
            if num_weekends == weeks:
                break
            else:
                i += 1 if target_date.weekday() == 6 else 2
                continue

        output.append(convert(target_date))
        i += 1
    return output


def filter_by_recovery(dividends):
    """
    Takes a dataframe and returns those stock symbols who have historically recovered well
    after dividend distributions
    :param dividends:
    :return:
    """
    # TODO: Write this entire method;
    return dividends

def load_dividend_targets(weeks = 2):
    # Get 1000 top dividend yield stocks
    dividend_data = pd.read_csv("../notebooks/dividend-stocks.csv")
    target_symbols = set(dividend_data.Symbol)

    # Get one months worth of future dividends
    DIVIDEND_BASE_URL = "https://www.nasdaq.com/dividend-stocks/dividend-calendar.aspx?date="
    future_dividend_dates = pd.concat([
        pd.read_html(f"{DIVIDEND_BASE_URL + date}")[0] for date in get_next_weeks_dates(weeks)
    ])
    future_dividend_dates =  future_dividend_dates.reset_index()
    future_dividend_dates['symbol'] = future_dividend_dates["Company (Symbol)"].str.extract(r"\s\(([A-Z]+)\)$")

    # Filter by top 1000 dividends of upcoming distributions
    target_dividends = future_dividend_dates[future_dividend_dates['symbol'].isin(target_symbols)]

    # Evaluate ability of each stock to "bounce back after each distribution"
    # TODO: Write this evaluation
    target_dividends = filter_by_recovery(target_dividends)

    # Of all stocks that reasonably bounce back, sort by maximal percentage returns
    prices = dividend_data[['Symbol', 'LastSale']]


    #TODO Current error is that the symbols in target_dividends are not in dividend data???
    price_and_dividend_data = pd.merge(target_dividends, prices, left_on='symbol', right_on='Symbol').drop(columns=['Symbol', 'Company (Symbol)', 'Record Date', 'Announcement Date'], axis =1)

    # Note this factors in quarterly vs monthly dividends
    price_and_dividend_data['yield'] = price_and_dividend_data['Dividend'] / price_and_dividend_data['LastSale']

    return price_and_dividend_data.sort_values(by="yield", ascending=False)




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



