from config import *

import pandas as pd
import numpy as np
import concurrent.futures
import datetime


async def _get_polygon_prices(symbols: List[str], end_dt = datetime.datetime.now(), max_workers: int = 5):
    '''Get the map of DataFrame price data from polygon, in parallel.'''

    start_dt = end_dt - pd.Timedelta('1200 days')
    _from = start_dt.strftime('%Y-%m-%d')
    to = end_dt.strftime('%Y-%m-%d')

    def historic_agg(symbol):
        return api.polygon.historic_agg(
            'day', symbol, _from=_from, to=to).df.sort_index()

    with concurrent.futures.ThreadPoolExecutor(
            max_workers=max_workers) as executor:
        results = {}
        future_to_symbol = {
            executor.submit(
                historic_agg,
                symbol): symbol for symbol in symbols}
        for future in concurrent.futures.as_completed(future_to_symbol):
            symbol = future_to_symbol[future]
            try:
                results[symbol] = future.result()
            except Exception as exc:
                pass
        return results