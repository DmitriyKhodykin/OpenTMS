import requests
import json


class Geocoding:
    """Класс для работы с геокодированием сервиса MapBox
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
        coords1: str = f'{coords1[1]},{coords1[0]}'  # Понятный сервису формат
        coords2: list = self.get_coordinates(point2)
        coords2: str = f'{coords2[1]},{coords2[0]}'
        r = requests.get(
            f'https://api.mapbox.com/directions/v5/mapbox/{profile}/{coords1};'
            f'{coords2}?access_token={self.access_token}').text
        response = json.loads(r)
        distance = int(response['routes'][0]['distance']) // 1000
        return distance
