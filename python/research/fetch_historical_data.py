import os
from alpaca.data.historical import StockHistoricalDataClient
from dotenv import load_dotenv
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime

load_dotenv()
api_key = os.getenv("ALPACA_API_KEY")
secret_key = os.getenv("SECRET_KEY")
if not api_key or not secret_key:
    raise Exception("Missing either key, - check your .env file")

data_client = StockHistoricalDataClient(api_key, secret_key)

request = StockBarsRequest(
    symbol_or_symbols = "AAPL",
    timeframe=TimeFrame.Day,
    start=datetime(2024, 1, 1)
)

response = data_client.get_stock_bars(request)
print(response)