from trading.config import *

polygon = api.polygon

import pandas as pd
import numpy as np


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
            positions = get_current_positions()


