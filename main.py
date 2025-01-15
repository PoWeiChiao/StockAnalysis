from datetime import datetime
from trade import Trade

def main():
    t = Trade()

    start_time = datetime(2019, 1, 1)
    end_time = datetime(2024, 12, 31)

    t.dca(code='TQQQ', start_time=start_time, end_time=end_time)
    t.dca(code='QQQ', start_time=start_time, end_time=end_time)
    t.dca(code='UPRO', start_time=start_time, end_time=end_time)
    t.dca(code='VOO', start_time=start_time, end_time=end_time)

    t.profolio.print_profolio()
    for key in t.profolio.get_holding_code():
        t.profolio.print_holding_current_details(key)

if __name__ == "__main__":
    main()