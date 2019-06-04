"""
Helper functions to issue orders for a given stock
at a given price.

Coordinates
    1. Market Orders --> Done
    2. Limit Orders --> Done
    3. Stop Loss orders --> Done
    4. Datetime specific orders (placing a market buy or sell at a given date)
        TODO: This seems a little hard, and I'm not sure there's a way
        to do this directly with the API


"""
from config import *

def get_pending_orders() -> List[Any]:
    """
    :return: Returns a list of pending orders if any are present
    """
    return api.list_orders()



def valid_response(resp) -> bool:
    failed_states = {
        "rejected",
        "stopped",
        "canceled",
        "expired",
    }
    return resp is not None and resp.status not in failed_states




#######################  Market Orders #############################################
def issue_market_buy(symbol: str,
                     quantity: int,
                     time_till_cancellation: TimeType = TimeType.DEFAULT) -> bool:
    """
    Issues a market buy and returns whether the order was accepted.
    Note that the order may or may not fill and that must be evaluated separately,
    see `pending_orders`
    :param symbol: the stock symbol
    :param quantity: the number of shares
    :param time_till_cancellation: how long the order is good for
    :return: boolean for success of the operation
    """
    resp: OrderResponseType = __issue_order(symbol,
                                    quantity,
                                    PurchaseType.BUY,
                                    OrderType.MARKET,
                                    time_till_cancellation)

    return valid_response(resp)



def issue_market_sell(symbol: str,
                      quantity: int,
                      time_till_cancellation: TimeType = TimeType.DEFAULT) -> bool:
    """
    Initiates a market sell order for a given number of stock at a given time
    :param symbol: the stock symbol
    :param quantity: the number of shares
    :param time_till_cancellation: how long the order is good for
    :return: boolean for success of the operation
    """

    resp: OrderResponseType = __issue_order(
        symbol=symbol,
        quantity=quantity,
        side=PurchaseType.SELL,
        type=OrderType.MARKET,
        time_till_cancellation=time_till_cancellation
    )

    return valid_response(resp)



#######################  Limit Orders #############################################

def issue_limit_buy(symbol: str,
                    quantity: int,
                    limit_price: float,
                    time_till_cancellation: TimeType = TimeType.DEFAULT) -> bool:
    resp: OrderResponseType = __issue_order(
        symbol = symbol,
        quantity = quantity,
        side = PurchaseType.BUY,
        type = OrderType.LIMIT,
        time_till_cancellation = time_till_cancellation,
        limit_price = limit_price
    )
    return valid_response(resp)


def issue_limit_sell(symbol: str,
                    quantity: int,
                    limit_price: float,
                    time_till_cancellation: TimeType = TimeType.DEFAULT) -> bool:
    resp: OrderResponseType = __issue_order(
        symbol = symbol,
        quantity = quantity,
        side = PurchaseType.SELL,
        type = OrderType.LIMIT,
        time_till_cancellation = time_till_cancellation,
        limit_price = limit_price
    )
    return valid_response(resp)


#######################  Stop Limit Orders ##############################
"""
Stop loss orders can create issues when the stocks blows past the expected
loss value and essentially becomes a market sell order to the lowest bidder. 
For that reason, we're currently only supporting stop limit orders which 
allow you to specify a lower limit to sell at in case all else fails. 
"""
def issue_stop_limit_sell(symbol: str,
                          quantity: int,
                          limit_price: float,
                          stop_price: float,
                          time_till_cancellation: TimeType = TimeType.DEFAULT) -> bool:

    resp: OrderResponseType = __issue_order(
        symbol = symbol,
        quantity = quantity,
        side = PurchaseType.SELL,
        type = OrderType.STOP_LIMIT,
        time_till_cancellation = time_till_cancellation,
        limit_price = limit_price,
        stop_price= stop_price
    )
    return valid_response(resp)



""" Private helper methods, do not use directly outside the file"""
def __issue_order(symbol: str,
                  quantity: int,
                  side: PurchaseType,
                  type: OrderType,
                  time_till_cancellation: TimeType,
                  limit_price: Optional[float] = None,
                  stop_price: Optional[float] = None,
                  ) -> Any:
    """
    A wrapper method around the original API accessed through the accessor methods below
    :param symbol: string representing stock symbol
    :param quantity: number of shares to move
    :param side: buy or sell
    :param type: OrderType
    :param time_till_cancellation: time to hold order as valid
    :param limit_price: limit price for the stock
    :param stop_price: valid for stop or stop loss
    :return: the response object from submitting the order
    """
    args_dict = {
        "symbol": symbol,
        "qty": quantity,
        "side": side,
        "type": type,
        "time_in_force": time_till_cancellation,
    }
    if type == OrderType.LIMIT or type == OrderType.STOP_LIMIT:
        assert limit_price is not None, "Limit price must be set for limit orders"
        args_dict['limit_price'] = limit_price
    if type == OrderType.STOP or type == OrderType.STOP_LIMIT:
        assert stop_price is not None, "Stop price must be set for stop orders"
        args_dict['stop_price'] = stop_price

    try:
        resp = api.submit_order(**args_dict)
        return resp
    except Exception as e:
        print(e)
        return None

