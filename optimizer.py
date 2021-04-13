"""Оптимизационный модуль приложения.

Содержит код для решения оптимизационной транспортной задачи различными
методами.
"""

import sys
import pandas as pd
import six

sys.modules['sklearn.externals.six'] = six
import mlrose
from geocoding import Geocoding
from auth import auth


class Optimizer:
    """Решает оптимизационную транспортную задачу.
    """

    def __init__(self, geo_points):
        self.geo_points = geo_points

    def get_map_route(self):
        """Возвращает лучший путь обхода точек, заданных гео-координатами.
        """
        fitness_coordinates = mlrose.TravellingSales(coords=self.geo_points)

        problem_fit = mlrose.TSPOpt(
            length=len(self.geo_points),
            fitness_fn=fitness_coordinates,
            maximize=False
        )

        best_state, _ = mlrose.genetic_alg(
            problem_fit,
            pop_size=200,
            mutation_prob=0.2,
            max_attempts=100,
            max_iters=10,
            random_state=2
        )

        return best_state


if __name__ == "__main__":

    ORDER = pd.DataFrame(
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

    # Регистрационные данные для сервиса
    MAPBOX_TOKEN: str = auth.mapbox_token

    # Определение координат точек
    coordinates_list: list = []
    gc = Geocoding(MAPBOX_TOKEN)

    for index, row in ORDER.iterrows():
        lat_lng = gc.get_coordinates(str(row))
        coordinates: tuple = (
            lat_lng[0],
            lat_lng[1]
        )

        coordinates_list.append(coordinates)

    print(coordinates_list)

    order_opt = Optimizer(coordinates_list)

    print(order_opt.get_map_route())
