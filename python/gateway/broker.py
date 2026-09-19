import os
from alpaca.trading.client import TradingClient
from dotenv import load_dotenv
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide
from alpaca.trading.enums import TimeInForce

load_dotenv()
api_key = os.getenv("ALPACA_API_KEY")
secret_key = os.getenv("SECRET_KEY")
if not api_key or not secret_key:
    raise Exception("Missing either key, - check your .env file")
trading_client = TradingClient(api_key, secret_key, paper=True)

def submit_order(symbol, side, quantity):
    order_data = MarketOrderRequest(
        symbol=symbol,
        qty=quantity,
        side =side,
        time_in_force=TimeInForce.DAY  #closes order if unfulfilled by trading day close
    )

    order = trading_client.submit_order(order_data=order_data) ##does the actual ordering of trades
    return order


if __name__ == "__main__":
    result = submit_order("AAPL", OrderSide.BUY, 1)
    print(result)