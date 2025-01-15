from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf

class Stock:
    def __init__(self, code):
        self.code = code
        self.ticker = yf.Ticker(self.code)

    def get_info(self):
        return self.ticker.history(period='max')
    
    def get_price_info(self, start_time, end_time):
        return self.ticker.history(start=start_time, end=end_time)