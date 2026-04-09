
from t_tech.invest import Client
import os
from .token import INVEST_TOKEN


def get_figi_by_ticker(ticker: str) -> dict:
    TOKEN = INVEST_TOKEN  # TOKEN = os.getenv("INVEST_TOKEN")

    client_obj = Client(TOKEN)
    
    with client_obj as client:
        # Выполняем поиск по тикеру
        response = client.instruments.find_instrument(query=ticker)

        if not response.instruments:
            raise ValueError(f"Инструмент с тикером '{ticker}' не найден")

        # Берём первый найденный инструмент (обычно самый релевантный)
        for element in response.instruments:
            if element.ticker == ticker and element.class_code == 'TQBR':
                return element.figi
