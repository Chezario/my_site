from t_tech.invest import Client
import os

# Получаем токен из переменных окружения
TOKEN = os.getenv("INVEST_TOKEN")
if not TOKEN:
    raise ValueError("Токен T-Invest API не найден в переменной окружения INVEST_TOKEN")

def find_figi_by_ticker(ticker: str) -> dict:
    instrument = list()
    """
    Находит инструмент по тикеру и возвращает его данные, включая FIGI.

    Args:
        ticker (str): Тикер инструмента (например, "SBER", "GAZP")


    Returns:
        dict: Словарь с информацией об инструменте
    """
    with Client(TOKEN) as client:
        # Выполняем поиск по тикеру
        response = client.instruments.find_instrument(query=ticker)

        if not response.instruments:
            raise ValueError(f"Инструмент с тикером '{ticker}' не найден")

        # Берём первый найденный инструмент (обычно самый релевантный)
        for element in response.instruments:
            if element.isin == "RU0009029540" and element.class_code == 'TQBR':
                instrument = element
                

        return instrument.figi

# Пример использования
if __name__ == "__main__":
    try:
        result = find_figi_by_ticker("SBER")
        print(result)
    except Exception as e:
        print(f"Ошибка: {e}")

