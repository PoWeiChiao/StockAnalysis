from datetime import datetime, timedelta
from stock import StockCenter
from trade import Trade
from profolio import Profolio
from simulator import IndexSimulator, EtfSimulator

def dca() -> None:
    """
    Simulates a trading operation using dollar-cost averaging (DCA).
    """
    codes = ['TQQQ', 'QLD', 'QQQ', 'UPRO', 'SSO', 'VOO']
    start_time = datetime(2021,1,1)
    holding_time = timedelta(days=365*1)

    profolio = Profolio(0)
    stockCenter = StockCenter()
    trade = Trade(profolio)
    
    end_time = start_time + holding_time
    current_time = end_time + timedelta(days=10)

    # Perform DCA trade operation
    for code in codes:
        trade.dca(code, start_time, end_time, 14, 1600)
        # Retrieve holding information
        info = profolio.get_holding_info(code)
    
        # Adjust current_time to the most recent valid trading day
        while not stockCenter.is_valid_day(code, current_time):
            current_time -= timedelta(days=1)
    
        # Print the number of shares, average price, and profit percentage
        print(f'from {start_time.strftime('%Y-%m-%d')} to {end_time.strftime('%Y-%m-%d')}')
        print(f'holding {info.get_share()} {code} in {round(info.get_average(), 2)}, 'f'profit: {round(info.get_profit_in_percentage(current_time), 2)}%')
        print(f'current price: {round(stockCenter.get_stock_price(code, current_time), 2)} in {current_time.strftime('%Y-%m-%d')}')
    
def leveragedSimulator() -> None:
    start = datetime(2026,1,1)
    end = datetime(2027,1,1)
    indexA = IndexSimulator(start, end)
    
    leveragedEtf1t = EtfSimulator(indexA, 1).get_etf()
    leveragedEtf2t = EtfSimulator(indexA, 2).get_etf()
    leveragedEtf3t = EtfSimulator(indexA, 3).get_etf()

    print(indexA.get_index())
    print(leveragedEtf1t)
    print(leveragedEtf2t)

if __name__ == "__main__":
    dca()
