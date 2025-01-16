from datetime import datetime, timedelta
from stock import StockCenter
from trade import Trade
from profolio import Profolio

code = 'TQQQ'
start_time = datetime(2024,1,1)
end_time = datetime(2024,12,31)
current_time = datetime.now()

def main() -> None:
    """
    Simulates a trading operation using dollar-cost averaging (DCA).
    """
    profolio = Profolio(0)
    stockCenter = StockCenter()
    trade = Trade(profolio)
    
    # Perform DCA trade operation
    trade.dca(code, start_time, end_time)
    
    # Retrieve holding information
    info = profolio.get_holding_info(code)
    
    # Adjust current_time to the most recent valid trading day
    while not stockCenter.is_valid_day(code, current_time):
        current_time -= timedelta(days=1)
    
    # Print the number of shares, average price, and profit percentage
    print(f'holding {info.get_share()} {code} in {info.get_average()}, '
          f'profit: {info.get_profit_in_percentage(current_time)}%')
    
if __name__ == "__main__":
    main()