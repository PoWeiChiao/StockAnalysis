from datetime import datetime, timedelta
from stock import Stock

class Profolio:
    def __init__(self, cash=0):
        self.cash = cash
        self.stock_record = {}
        self.holding = {}
        self.holding_details = {}

    def save(self, cash):
        self.cash += cash

    def buy_cash(self, cash, code, target_datetime, type='Close'):
        if self.cash < cash:
            return
        if code not in self.holding:
            self.holding[code] = []
            self.stock_record[code] = Stock(code=code)
        while not self.is_valid_day(code, target_datetime):
            target_datetime -= timedelta(days=1)
        price_info = self.stock_record[code].get_price_info(target_datetime, target_datetime + timedelta(days=1))
        price = price_info[type].iloc[0]
        share = int(cash // price)
        self.cash -= share * price
        self.holding[code].extend([price]*share)
        self._update_holding_details(code)
        print(f'Date: {target_datetime.strftime('%Y-%m-%d')}, buy {share} {code} in {price}')
    
    def buy_share(self, share, code, target_datetime, type='Close'):
        if code not in self.holding:
            self.holding[code] = []
            self.stock_record[code] = Stock(code=code)
        while not self.is_valid_day(code, target_datetime):
            target_datetime -= timedelta(days=1)
        price_info = self.stock_record[code].get_price_info(target_datetime, target_datetime + timedelta(days=1))
        price = price_info[type].iloc[0]
        if self.cash < share * price:
            return
        if code not in self.holding:
            self.holding[code] = []
        self.cash -= share * price
        self.holding[code].extend([price]*share)
        self._update_holding_details(code)
        print(f'Date: {target_datetime.strftime('%Y-%m-%d')}, buy {share} {code} in {price}')
        
    def sell_share(self, share, code, target_datetime, type='Close'):
        if code not in self.holding:
            return
        if self.holding_details[code]['Share'] < share:
            return
        while not self.is_valid_day(code, target_datetime):
            target_datetime -= timedelta(days=1)
        price_info = self.stock_record[code].get_price_info(target_datetime, target_datetime + timedelta(days=1))
        price = price_info[type].iloc[0]
        self.cash += price * share
        self.holding[code] = self.holding[code][share:]
        self._update_holding_details(code, target_datetime)
        print(f'Date: {target_datetime.strftime('%Y-%m-%d')}, sell {share} {code} in {price}')

    def get_cash(self):
        return self.cash
    
    def get_holding(self):
        return self.holding
    
    def get_holding_code(self):
        return self.holding.keys()
    
    def get_holding_share_number(self, code):
        return 0 if code not in self.holding else self.holding_details[code]['Share']
    
    def print_holding_current_details(self, code, target_datetime=datetime.now(), type='Close'):
        while not self.is_valid_day(code, target_datetime):
            target_datetime -= timedelta(days=1)
        price = self.stock_record[code].get_price_info(target_datetime, target_datetime + timedelta(days=1))[type].iloc[0]
        current_cost = round(price * self.holding_details[code]['Share'], 2)
        total_cost = round(self.holding_details[code]['Average'] * self.holding_details[code]['Share'], 2)
        total_profit = round((price - self.holding_details[code]['Average']) * self.holding_details[code]['Share'], 2)
        total_profit_in_percentage = round((total_profit / total_cost) * 100, 2)
        print(f'Code: {code}, Average: {self.holding_details[code]['Average']}, Share: {self.holding_details[code]['Share']}, Current_Price: {price}, Current_Cost: {current_cost}, Total_Cost: {total_cost}, Total_Profit: {total_profit}, Total_Profit_in_Percentage: {total_profit_in_percentage}')

    def print_profolio(self):
        print(f"Cash: {self.cash}, Holding_Details: {self.holding_details}")

    def is_valid_day(self, code, target_datetime):
        if code not in self.stock_record:
            self.stock_record[code] = Stock(code=code)
        return len(self.stock_record[code].get_price_info(target_datetime, target_datetime + timedelta(days=1))) > 0
    
    # def splited_ratio(self, code, start_time, end_time):
    #     info = self.stock_record[code].get_price_info(start_time, end_time)
    #     splits = 1
    #     for _, row in info.iterrows():
    #         if row['Stock Splits'] != 0.0:
    #             splits *= row['Stock Splits']
    #     return splits

    def _update_holding_details(self, code, digits=2):
        if code not in self.holding_details:
            self.holding_details[code] = {}
        self.holding_details[code]['Share'] = len(self.holding[code])
        if self.holding_details[code]['Share'] == 0:
            self.holding_details[code]['Average'] = 0
        else:
            self.holding_details[code]['Average'] = round(sum(self.holding[code]) / len(self.holding[code]), digits)
