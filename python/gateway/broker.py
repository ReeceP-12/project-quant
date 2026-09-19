import os
from alpaca.trading.client import TradingClient
from dotenv import load_dotenv
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide
from alpaca.trading.enums import TimeInForce
from alpaca.trading.requests import LimitOrderRequest



load_dotenv()
api_key = os.getenv("ALPACA_API_KEY")
secret_key = os.getenv("SECRET_KEY")
if not api_key or not secret_key:
    raise Exception("Missing either key, - check your .env file")
trading_client = TradingClient(api_key, secret_key, paper=True)

def submit_order(symbol, side, quantity, limit_price=None):

    if limit_price is None:
        order_data = MarketOrderRequest(
            symbol=symbol,
            qty=quantity,
            side =side,
            time_in_force=TimeInForce.DAY  #closes order if unfulfilled by trading day close
    )
    elif limit_price <= 0:
        raise Exception("Limit price must be greater than 0")
    else:
        order_data = LimitOrderRequest(
            symbol=symbol,
            qty=quantity,
            side =side,
            time_in_force=TimeInForce.DAY,
            limit_price=limit_price
        )
    order = trading_client.submit_order(order_data=order_data) ##does the actual ordering of trades
    return order


def get_order_status(order_id):
    order = trading_client.get_order_by_id(order_id)
    return order.status


if __name__ == "__main__":
    result = submit_order("AAPL", OrderSide.BUY, 1,limit_price=150)
    print(result)
    print(result.id)

    status = get_order_status(result.id)
    print(status)