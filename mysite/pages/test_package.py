from t_invest_utils import *

tickers = ['SBER', 'VTBR']

for ticker in tickers:
    print(get_real_price(ticker))

