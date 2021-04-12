"""Основной модуль приложения.

Дока по основному модулю
"""

import numpy as np
import pandas as pd
import six
import sys
sys.modules['sklearn.externals.six'] = six
import mlrose
from geocoding import Geocoding
from auth import auth


order = pd.DataFrame(
    {
        'city': [
            'Россия, Воронеж',
            'Россия, Саратов',
            'Россия, Москва',
            'Россия, Рязань',
            'Росиия, Казань'
        ]
    }
)

if __name__ == "__main__":

    # Регистрационные данные для сервиса
    MAPBOX_TOKEN: str = auth.mapbox_token

    # Определение расстояния между точками
    dist_list: list = []
    coords_list: list = []
    gc = Geocoding(MAPBOX_TOKEN)

    for index_a, row_a in order.iterrows():
        for index_b, row_b in order.iterrows():
            if index_a != index_b:
                distance: int = gc.distance_mapbox(row_a, row_b)
                pairs: tuple = (index_a, index_b, distance)
                coords: tuple = (
                    gc.get_coordinates(row_a) / 90,
                    gc.get_coordinates(row_b) / 90
                )
                dist_list.append(pairs)
                coords_list.append(coords)

    print(dist_list)
    print(coords_list)
