from datetime import timedelta
from profolio import Profolio

class Trade:
    def __init__(self):
        self.profolio = Profolio(0)

    def dca(self, code, start_time, end_time, interval=30, cost=3000):
        current_time = start_time
        while not current_time > end_time:
            while not self.profolio.is_valid_day(code, current_time):
                current_time -= timedelta(days=1)
            print(current_time)
            self.profolio.save(cost)
            self.profolio.buy_cash(cost, code, current_time)     
            current_time += timedelta(days=interval)
        
