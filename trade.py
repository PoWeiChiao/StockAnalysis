from datetime import datetime, timedelta
from stock import StockCenter
from profolio import Profolio

class Trade:
    def __init__(self, profolio: Profolio = Profolio(0)):
        self.profolio = profolio

    def dca(self, code: str, start_time: datetime, end_time: datetime, interval: int = 30, cost: float = 3000) -> None:
        """
        Executes Dollar-Cost Averaging strategy by purchasing a fixed amount of stock
        at regular intervals between start_time and end_time.

        :param code: Stock code to perform DCA on.
        :param start_time: Start date for DCA.
        :param end_time: End date for DCA.
        :param interval: Number of days between each purchase.
        :param cost: Fixed amount of cash to invest at each interval.
        """
        current_time = start_time
        stock_center = StockCenter()

        while current_time <= end_time:
            if stock_center.is_valid_day(code, current_time):
                self.profolio.save(cost)
                self.profolio.buy_fixed_cash(code, cost, current_time)
                current_time += timedelta(days=interval)
            else:
                current_time += timedelta(days=1)
        
