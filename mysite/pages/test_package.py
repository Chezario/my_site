from t_invest_utils import *

tickers = ['T', 'SBER', 'VTBR']

# for ticker in tickers:
#     print(get_current_price(ticker))

for element in tickers:
    print(get_figi_by_ticker(ticker=element))