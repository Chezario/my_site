from t_invest_utils import *

tickers = ['MDMG']

# # for ticker in tickers:
# #     print(get_current_price(ticker))

for element in tickers:
    print(get_figi_by_ticker(ticker=element))
