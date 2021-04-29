"""Модуль геокодирования.

Прямая задача геокодирования - получение координат (широта и долгота)
географической точки по ее наименованию. Для решения этой задачи используется
сервис: https://www.mapbox.com/

После регистрации в сервисе (в личном кабинете) доступен token, который
является обязательным для передачи во всех запросах к сервису.

Описание API для доступа к сервису: https://docs.mapbox.com/api/overview/
"""

import json             # Работа с JSON
import requests         # HTTP-запросы
from auth import auth   # Регистрационные данные


def geocoding(address: str) -> list:
    """Возвращает координаты точки (широта, долгота), например,
    [38.05, 41.06]
    """

    url = "https://cleaner.dadata.ru/api/v1/clean/address"

    payload = address

    headers = {
        'authorization': auth.da_token,
        'x-secret': auth.da_secret,
        'content-type': "application/json",
        'cache-control': "no-cache"
    }

    request = requests.request("POST", url, data=payload, headers=headers)

    response = json.loads(request.text, encoding='utf-8')

    print(response)

    geo_point = response[0]
    lat = geo_point["geo_lat"]
    lng = geo_point["geo_lon"]

    return [lat, lng]


if __name__ == "__main__":

    # Наименования геоточки
    ADDRESS = '[ "воронеж патриотов 11" ]'

    # Определение координат
    coordinates = geocoding(ADDRESS)
    print('Координаты точки:', coordinates)
