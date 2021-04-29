def distance_mapbox(self, point1: str, point2: str,
                    profile='driving-traffic') -> int:
    """Возвращает расстояние между пунктами 1 и 2 в км
        # Опции метода:
        # - driving-traffic - Исторический трафик для автомобиля
        # - driving - Самый быстрый путь для автомобиля
        # - walking - Пешеходный маршрут
        # - cycling - Веломаршрут
    """

    coords1: list = self.get_coordinates()
    geo_1: str = f'{coords1[1]},{coords1[0]}'  # Понятный сервису формат
    coords2: list = self.get_coordinates()
    geo_2: str = f'{coords2[1]},{coords2[0]}'

    r = requests.get(
        f'https://api.mapbox.com/directions/v5/mapbox/{profile}/{geo_1};'
        f'{geo_2}?access_token={auth.mapbox_token}').text

    response = json.loads(r)
    distance = int(response['routes'][0]['distance']) // 1000

    return distance