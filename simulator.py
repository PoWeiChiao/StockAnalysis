from datetime import datetime, timedelta
import random
from helper import Helper

class IndexSimulator:
    def __init__(self, start_time: datetime, end_time: datetime, init_value: float = 100.0,
                 change_rate_lower_bound: float = -3.0, change_rate_higher_bound: float = 3.0):
        self.start_time = start_time
        self.end_time = end_time
        self.init_value = init_value
        self.change_rate_lower_bound = change_rate_lower_bound
        self.change_rate_higher_bound = change_rate_higher_bound
        self.index = {}
        self._generate_index()

    def _generate_index(self):
        current_time = self.start_time
        helper = Helper()
        while current_time <= self.end_time:
            key = helper._generate_key_by_timestamp(current_time)
            if current_time == self.start_time:
                self.index[key] = self.init_value
            else:
                prev_key = helper._generate_key_by_timestamp(current_time - timedelta(days=1))
                prev_value = self.index[prev_key]
                self.index[key] = self._calculate_new_value(prev_value)
            current_time += timedelta(days=1)

    def _calculate_new_value(self, prev_value: float) -> float:
        change_rate = random.uniform(self.change_rate_lower_bound, self.change_rate_higher_bound) / 100
        return round(prev_value * (1 + change_rate), 2)

    def get_index(self) -> dict:
        """Return the dictionary containing the generated index values."""
        return self.index

class EtfSimulator:
    def __init__(self, index: 'IndexSimulator', leveraged: int, init_value: float = 100):
        self.index = index.get_index()
        self.leveraged = leveraged
        self.init_value = init_value
        self.etf = {}
        self._generate_etf()

    def _generate_etf(self):
        prev_index = None
        prev_etf = self.init_value

        for key, current_index in self.index.items():
            if prev_index is None:
                self.etf[key] = prev_etf
            else:
                change_ratio = (current_index - prev_index) / prev_index
                self.etf[key] = prev_etf * (1 + change_ratio * self.leveraged)
                prev_etf = self.etf[key]
            prev_index = current_index

    def get_etf(self) -> dict:
        """Returns the calculated ETF values."""
        return self.etf


    
    


