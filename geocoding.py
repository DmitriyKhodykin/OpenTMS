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


class Geocoding:
    """
    Класс для работы с геокодированием сервиса MapBox.
    (получение координат точки, получение расстояния между точками)
    """

    def __init__(self, access_token: str):
        self.access_token = access_token

    def get_coordinates(self, point: str) -> list:
        """Возвращает координаты точки (широта, долгота), например,
        [38.05, 41.06]
        """

        r = requests.get(
            f'https://api.mapbox.com/geocoding/v5/mapbox.places/{point}'
            f'.json?limit=2&access_token={self.access_token}').text

        response = json.loads(r)
        geo_point = response['features'][0]['center']
        lng = geo_point[0]
        lat = geo_point[1]

        return [lat, lng]

    def distance_mapbox(self, point1: str, point2: str,
                        profile='driving-traffic') -> int:
        """Возвращает расстояние между пунктами 1 и 2 в км
            # Опции метода:
            # - driving-traffic - Исторический трафик для автомобиля
            # - driving - Самый быстрый путь для автомобиля
            # - walking - Пешеходный маршрут
            # - cycling - Веломаршрут
        """

        coords1: list = self.get_coordinates(point1)
        geo_1: str = f'{coords1[1]},{coords1[0]}'  # Понятный сервису формат
        coords2: list = self.get_coordinates(point2)
        geo_2: str = f'{coords2[1]},{coords2[0]}'

        r = requests.get(
            f'https://api.mapbox.com/directions/v5/mapbox/{profile}/{geo_1};'
            f'{geo_2}?access_token={self.access_token}').text

        response = json.loads(r)
        distance = int(response['routes'][0]['distance']) // 1000

        return distance


if __name__ == "__main__":

    # Регистрационные данные для сервиса
    MAPBOX_TOKEN = auth.mapbox_token

    # Создание экземпляра класса
    gc = Geocoding(MAPBOX_TOKEN)

    # Наименования геоточек
    CITY_A = 'Россия, Воронежская, Воронеж, Труда, 59'
    CITY_B = 'Россия, Воронежская, Воронеж, Баррикадная, 39'

    # Определение координат
    coordinates_a = gc.get_coordinates(CITY_A)
    print(f'Координаты <{CITY_A}>:', coordinates_a)
    coordinates_b = gc.get_coordinates(CITY_B)
    print(f'Координаты <{CITY_B}>:', coordinates_b)

    # Определение расстояния
    dist = gc.distance_mapbox(CITY_A, CITY_B)
    print('Расстояние между городами, км:', dist)
