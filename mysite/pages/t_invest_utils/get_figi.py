
from t_tech.invest import Client, InstrumentIdType
import os
from .token import INVEST_TOKEN


# def get_figi_by_ticker(ticker: str) -> dict:
#     TOKEN = INVEST_TOKEN  # TOKEN = os.getenv("INVEST_TOKEN")

#     client_obj = Client(TOKEN)
    
#     with client_obj as client:
#         # Выполняем поиск по тикеру
#         response = client.instruments.find_instrument(
#             query=ticker,
#             # instrument_kind=('INSTRUMENT_TYPE_SHARE')
#         )

#         if not response.instruments:
#             raise ValueError(f"Инструмент с тикером '{ticker}' не найден")

#         # Берём первый найденный инструмент (обычно самый релевантный)
#         for element in response.instruments:
#             if element.ticker == ticker and element.class_code == 'TQBR':
#                 return element.figi

def get_figi_by_ticker(ticker: str) -> dict:
    TOKEN = INVEST_TOKEN  # TOKEN = os.getenv("INVEST_TOKEN")

    client_obj = Client(TOKEN)
    
    with client_obj as client:
        # Выполняем поиск по тикеру
        response = client.instruments.get_instrument_by(
            id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_TICKER,
            id=ticker,
            class_code="TQBR",
        )
        return response.instrument.figi

        