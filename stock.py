from typing import List
import yfinance as yf
from datetime import datetime, timedelta

class StockCenter:
    _instance = None
    _stock_info = {}
    _stock_record = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def add_stock_record(self, code: str) -> None:
        """Add a stock record if it doesn't already exist."""
        if code not in self._stock_info:
            self._stock_info[code] = Stock(code)
            self._stock_record.append(code)

    def remove_stock_record(self, code: str) -> None:
        """Remove a stock record if it exists."""
        if code in self._stock_info:
            del self._stock_info[code]
            self._stock_record.remove(code)

    def get_stock_record_list(self) -> List[str]:
        """Return the list of stock records."""
        return self._stock_record

    def get_stock_price_info(self, code: str, start_time: datetime, end_time: datetime):
        """Retrieve price information for a stock over a specified time range."""
        if code not in self._stock_info:
            self.add_stock_record(code)
        return self._stock_info[code].get_price_info(start_time, end_time)

    def get_stock_price(self, code: str, target_datetime: datetime, type: str = 'Close'):
        """Retrieve the price of a stock at a specific date and time."""
        if code not in self._stock_info:
            self.add_stock_record(code)
        return self._stock_info[code].get_price(target_datetime, type)
    
    def is_valid_day(self, code: str, target_datetime: datetime, type: str = 'Close') -> bool:
        """Check if a specific day is valid for stock data."""
        if code not in self._stock_info:
            self.add_stock_record(code)
        return self._stock_info[code].get_price(target_datetime, type) != -1

class Stock:
    def __init__(self, code: str):
        self.code = code
        self.ticker = yf.Ticker(self.code)
        self.info = self._generate_info()

    def _generate_key_by_timestamp(self, target_datetime: datetime) -> str:
        """Generate a key in 'YYYYMMDD' format from a datetime object."""
        return target_datetime.strftime('%Y%m%d')

    def _generate_info(self) -> dict:
        """Populate the info dictionary with historical stock data."""
        data = self.ticker.history(period='max')
        return {self._generate_key_by_timestamp(index): row for index, row in data.iterrows()}

    def get_info(self) -> dict:
        """Return all stored stock information."""
        return self.info

    def get_price_info(self, start_time: datetime, end_time: datetime) -> dict:
        """Retrieve price information between two dates."""
        price_info = {}
        current_time = start_time
        while current_time <= end_time:
            key = self._generate_key_by_timestamp(current_time)
            if key in self.info:
                price_info[key] = self.info[key]
            current_time += timedelta(days=1)
        return price_info

    def get_price(self, target_datetime: datetime, type: str = 'Close') -> float:
        """Return a specific price type for a given date."""
        if target_datetime > datetime.now() or type not in {'Open', 'High', 'Low', 'Close'}:
            return -1
        key = self._generate_key_by_timestamp(target_datetime)
        return self.info.get(key, {}).get(type, -1)
        