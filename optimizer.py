"""Оптимизационный модуль приложения.

Содержит код для решения оптимизационной транспортной задачи различными
методами.
"""

import numpy as np
import pandas as pd
import six
import sys
sys.modules['sklearn.externals.six'] = six
import mlrose
from geocoding import Geocoding
from auth import auth


class Optimizer:
    """Решает оптимизационную транспортную задачу.
    """
    def __init__(self, coords_list):
        self.coords_list = coords_list

    def get_map_route(self):
        """Возвращает лучший путь обхода точек, заданных гео-координатами.
        """
        fitness_coords = mlrose.TravellingSales(coords = self.coords_list)

        problem_fit = mlrose.TSPOpt(
            length = len(coords_list),
            fitness_fn = fitness_coords,
            maximize=False
        )

        best_state, _ = mlrose.genetic_alg(
            problem_fit,
            pop_size=200,
            mutation_prob=0.2,
            max_attempts=100,
            max_iters=10,
            random_state = 2
        )

        return best_state


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
                    gc.get_coordinates(row_a),
                    gc.get_coordinates(row_b)
                )
                dist_list.append(pairs)
                coords_list.append(coords)

    print(dist_list)
    print(coords_list)

    fitness_dists = mlrose.TravellingSales(distances = dist_list)
    problem_fit = mlrose.TSPOpt(length = 8, fitness_fn = fitness_dists, maximize=False)
    best_state, best_fitness = mlrose.genetic_alg(problem_fit, mutation_prob = 0.2,
                                              max_attempts = 100, random_state = 2)
    print(best_state)
    print(best_fitness)
