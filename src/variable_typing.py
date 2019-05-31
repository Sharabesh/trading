"""
Defines types for values used in the Alpaca API
"""

from enum import Enum
from mypy_extensions import TypedDict
from typing import List, Any, Union, Optional

class OrderType(Enum):
    MARKET = 'market'
    LIMIT = 'limit'
    STOP = 'stop'
    STOP_LIMIT = 'stop_limit'

class TimeType(Enum):
    """
     Note on OPG orders:
     The order is placed at the time the market opens.
     The order will be accepted if it is received before 9:15AM (ET).
     The order can be cancelled after 9:15AM,
       but it cannot be edited.
     After 9:28AM,  OPG orders cannot be edited or cancelled.
     Any unfilled orders after opening of the market
      will be cancelled.
     If you submit OPG orders during the market hours,
        it will appear as “rejected” in your dashboard.
    TODO #Basically don't use OPG because it's real complicated
    """
    DAY = 'day' # Order is good for the day and cancelled at the end of the day
    GTC = 'gtc' # Good till Cancelled
    OPG = 'opg' # See above
    DEFAULT = 'day' # default if time is not otherwise specified

class PurchaseType(Enum):

    SELL = 'sell'
    BUY = 'buy'

OrderResponseType = TypedDict('OrderResponseType', {
  "id": str, # "904837e3-3b76-47ec-b432-046db621571b",
  "client_order_id": str, #  "904837e3-3b76-47ec-b432-046db621571b",
  "created_at": str, # "2018-10-05T05:48:59Z",
  "updated_at": str, #"2018-10-05T05:48:59Z",
  "submitted_at": str, #"2018-10-05T05:48:59Z",
  "filled_at": str, #"2018-10-05T05:48:59Z",
  "expired_at": str, #"2018-10-05T05:48:59Z",
  "canceled_at": str, #"2018-10-05T05:48:59Z",
  "failed_at": str, #"2018-10-05T05:48:59Z",
  "asset_id": str, #"904837e3-3b76-47ec-b432-046db621571b",
  "symbol": str, #"AAPL",
  "asset_class": str, #"us_equity",
  "qty": str, #"15",
  "filled_qty": str, #"0",
  "type": str, #market",
  "side": str, #"buy",
  "time_in_force": str, #"day",
  "limit_price": str, #"107.00",
  "stop_price": str, #"106.00",
  "filled_avg_price": str, #"106.00",
  "status": str, #accepted"
})