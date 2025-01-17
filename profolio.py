from datetime import datetime
from typing import Dict, List
from stock import StockCenter

class Info:
    def __init__(self, code: str, share: int = 0, average: float = 0.0):
        """Initialize Info with share count and average price."""
        self._code = code
        self._share = share
        self._average = average

    def update_info(self, share: int, average: float) -> None:
        """Update the share count and average price."""
        self._share = share
        self._average = average

    def get_share(self) -> int:
        return self._share

    def get_average(self) -> float:
        return self._average

    def get_profit(self, target_datetime: datetime, type: str = 'Close') -> float:
        """
        Calculate the profit for a given stock code and date.

        :param target_datetime: Date for which to fetch the stock price
        :param type: Type of price to fetch (default is 'Close')
        :return: Profit as a float
        """
        target_price = StockCenter().get_stock_price(self._code, target_datetime, type)
        if target_price == -1:
            print(f'No data found for {self._code} on {target_datetime.strftime("%Y%m%d")}')
            return 0.0
        return (target_price - self._average) * self._share

    def get_profit_in_percentage(self, target_datetime: datetime, type: str = 'Close') -> float:
        """
        Calculate the profit percentage for a given stock code and date.

        :param target_datetime: Date for which to fetch the stock price.
        :param type: Type of price to fetch (default is 'Close').
        :return: Profit percentage as a float.
        """
        target_price = StockCenter().get_stock_price(self._code, target_datetime, type)
        if target_price == -1:
            print(f'No data found for {self._code} on {target_datetime.strftime("%Y%m%d")}')
            return 0.0
        return ((target_price / self._average) - 1) * 100

class Profolio:
    def __init__(self, cash: float = 0.0, print_details: bool = False):
        self.cash = cash
        self.print_details = print_details
        self.holding: Dict[str, List[float]] = {}
        self.holding_info: Dict[str, Info] = {}

    def save(self, cash: float) -> None:
        """Add cash to the portfolio."""
        self.cash += cash

    def buy_fixed_cash(self, code: str, cash: float, target_datetime: datetime, type: str = 'Close') -> None:
        """Buy stocks using a specified amount of cash."""
        if self.cash < cash:
            print('Not enough cash to buy')
            return
        price = StockCenter().get_stock_price(code, target_datetime, type)
        if price == -1:
            print(f'No data found for {code} on {target_datetime.strftime("%Y%m%d")}')
            return
        share = int(cash // price)
        if share == 0:
            print('Not enough cash to buy')
            return
        self._update_holding(code, share, price)
        self.cash -= share * price
        if self.print_details:
            print(f'Date: {target_datetime.strftime("%Y-%m-%d")}, buy {share} {code} at {price}')

    def buy_fixed_share(self, code: str, share: int, target_datetime: datetime, type: str = 'Close') -> None:
        """Buy a specified number of shares of a stock."""
        price = StockCenter().get_stock_price(code, target_datetime, type)
        if price == -1:
            print(f'No data found for {code} on {target_datetime.strftime("%Y%m%d")}')
            return
        total_cost = share * price
        if self.cash < total_cost:
            print('Not enough cash to buy')
            return
        self._update_holding(code, share, price)
        self.cash -= total_cost
        if self.print_details:
            print(f'Date: {target_datetime.strftime("%Y-%m-%d")}, buy {share} {code} at {price}')

    def sell_share(self, code: str, share: int, target_datetime: datetime, type: str = 'Close') -> None:
        """Sell a specified number of shares of a stock."""
        if code not in self.holding or len(self.holding[code]) < share:
            print(f'Not enough shares to sell or {code} not found in holding')
            return
        price = StockCenter().get_stock_price(code, target_datetime, type)
        if price == -1:
            print(f'No data found for {code} on {target_datetime.strftime("%Y%m%d")}')
            return
        self.cash += price * share
        self.holding[code] = self.holding[code][share:]
        if not self.holding[code]:
            del self.holding[code]
            del self.holding_info[code]
        else:
            self.holding_info[code].update_info(len(self.holding[code]), sum(self.holding[code]) / len(self.holding[code]))
        if self.print_details:
            print(f'Date: {target_datetime.strftime("%Y-%m-%d")}, sell {share} {code} at {price}')

    def get_cash(self) -> float:
        """Return the current cash balance."""
        return self.cash

    def get_holding(self) -> Dict[str, List[float]]:
        """Return the current stock holdings."""
        return self.holding

    def get_holding_list(self) -> list:
        """Return a list of stock codes in the holdings."""
        return list(self.holding.keys())

    def get_holding_info(self, code: str) -> Info:
        """Return detailed information about a specific stock holding."""
        return self.holding_info.get(code, Info(code))

    def _update_holding(self, code: str, share: int, price: float) -> None:
        """Update the holding with the given stock code, share, and price."""
        if code not in self.holding:
            self.holding[code] = []
            self.holding_info[code] = Info(code)
        self.holding[code].extend([price] * share)
        self.holding_info[code].update_info(len(self.holding[code]), sum(self.holding[code]) / len(self.holding[code]))
