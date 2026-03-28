from t_tech.invest import Client
import os

def get_stock_price(figi: str) -> float:

    TOKEN = os.getenv("INVEST_TOKEN")

    client_obj = Client(TOKEN)
    """
    Получает текущую цену акции по FIGI.

    Args:
        figi (str): FIGI инструмента (уникальный идентификатор)

    Returns:
        float: Текущая цена акции
    """

    try:
        # Создаём клиент с токеном
        with client_obj as client:
            # Получаем последнюю цену по FIGI
            response = client.market_data.get_last_prices(figi=[figi])

            if not response.last_prices:
                raise ValueError(f"Не удалось получить цену для FIGI: {figi}")

            # Цена возвращается в копейках (для RUB) или в минимальных единицах валюты
            price_in_units = response.last_prices[0].price

            # Конвертируем в рубли (делим на 100 для RUB)
            # price_rub = int(price_in_units) / 100

            return price_in_units

    except Exception as e:
        print(f"Ошибка при получении цены: {e}")
        raise
