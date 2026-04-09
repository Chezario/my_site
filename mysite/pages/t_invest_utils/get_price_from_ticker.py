from .get_figi import get_figi_by_ticker
from .get_price import get_stock_price
from .get_number import quotation_to_decimal

def get_current_price(ticker):
    figi = get_figi_by_ticker(ticker)
    price_in_units = get_stock_price(figi)
    price = quotation_to_decimal(price_in_units)
    return price