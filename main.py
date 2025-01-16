from datetime import datetime, timedelta
from trade import Trade
from profolio import Profolio

code = 'TQQQ'
start_time = datetime(2024,1,1)
end_time = datetime(2024,12,31)
current_time = datetime.now()

def main():
    profolio = Profolio(0)
    trade = Trade(profolio)
    trade.dca(code, start_time, end_time)
    info = profolio.get_holding_info(code)
    print(f'holding {info.get_share()} {code} in {info.get_average()}, profit: {info.get_profit_in_percentage(current_time)}%')
    
if __name__ == "__main__":
    main()