"""
The background trader runs forever in the background
and gets updates for price changes of different stocks.
Based on the events that get triggered it can issue
buy and sell orders.

Configures the Alpaca API  to
    1. monitor for changes in real time
    2. Trigger purchases or sales from real events

"""
from config import *
from alpaca_trade_api import StreamConn

# Used to retrieve stock specific data
polygon_data = api.polygon


conn = StreamConn()


@conn.on(r'account_updates')
async def on_account_updates(conn, channel, account):
    """
    Monitors for Alpaca's connection channel
    and triggers if any trade is made or the account
    is otherwise updated
    """
    print(f"Account {account} has been modified")


@conn.on(r'^AM.')
def on_bars(conn, channel, bar):
    """
    Triggers on price changes through the Polygon API.
    Bar represents the change you are being notified for
    """
    print('bars', bar)


# Connects to ALPACA and Polygon for price updates
conn.run(['account_updates', 'AM.*'])
