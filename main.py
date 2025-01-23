from datetime import datetime, timedelta
from stock import StockCenter
from trade import Trade
from profolio import Profolio

def dca() -> None:
    """
    Simulates a trading operation using dollar-cost averaging (DCA).
    """
    codes = ['TQQQ', 'QQQ', 'UPRO', 'VOO', 'NVDA', 'MSFT', 'AAPL', 'AMZN', 'GOOGL', 'TSLA', 'TSM']
    start_time = datetime(2024,1,1)
    holding_time = timedelta(days=365*1)

    profolio = Profolio(0)
    stockCenter = StockCenter()
    trade = Trade(profolio)
    
    end_time = start_time + holding_time
    current_time = end_time + timedelta(days=10)

    # Perform DCA trade operation
    for code in codes:
        trade.dca(code, start_time, end_time, 14, 1000)
        # Retrieve holding information
        info = profolio.get_holding_info(code)
    
        # Adjust current_time to the most recent valid trading day
        while not stockCenter.is_valid_day(code, current_time):
            current_time -= timedelta(days=1)
    
        # Print the number of shares, average price, and profit percentage
        print(f'from {start_time.strftime('%Y-%m-%d')} to {end_time.strftime('%Y-%m-%d')}')
        print(f'holding {info.get_share()} {code} in {round(info.get_average(), 2)}, 'f'profit: {round(info.get_profit_in_percentage(current_time), 2)}%')
        print(f'current price: {round(stockCenter.get_stock_price(code, current_time), 2)} in {current_time.strftime('%Y-%m-%d')}')

if __name__ == "__main__":
    dca()
