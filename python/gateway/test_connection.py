import os
from alpaca.trading.client import TradingClient
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("ALPACA_API_KEY")
secret_key = os.getenv("SECRET_KEY")
if not api_key or not secret_key:
    raise Exception("Missing either key, - check your .env file")
trading_client = TradingClient(api_key, secret_key, paper=True)
account = trading_client.get_account()
print(f"Status: {account.status}")
print(f"Cash: {account.cash}")