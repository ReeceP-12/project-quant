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


##note for researchers - this is what you want to be editing
request = StockBarsRequest(
    symbol_or_symbols = "AAPL", ##this is the ticker you need to change - look up what the ticker is for what you want to test on
    timeframe=TimeFrame.Day, ##
    start=datetime(2024, 1, 1), ## change the date here, - year/month/day.
    end=datetime(2024, 6, 1) ##change the end date of the data, same format
)

response = data_client.get_stock_bars(request)
print(response)