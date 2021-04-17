"""Оптимизационный модуль приложения.

Модуль строится на основе библиотеки `mlrose`, документацию по которой
можно найти по ссылке: https://mlrose.readthedocs.io/en/stable/

Библиотека предоставляет наиболее распространенные алгоритмы рандомизированной
оптимизации и поиска, применимые к ряду задач оптимизации как дискретными,
так и с непрерывными значениями.
"""

from geocoding import Geocoding
from auth import auth

import pandas as pd
import six
import sys
sys.modules['sklearn.externals.six'] = six
import mlrose


class Optimizer:
    """Решает оптимизационную транспортную задачу.
    """

    def __init__(self, access_token: str, orders: pd.DataFrame):
        self.access_token = access_token
        self.orders = orders

    def __get_map_coordinates(self) -> list:
        """Возвращает список координат географических точек
        из заказов на перевозку.
        """
        # Определение координат точек
        coordinates_list: list = []
        # Экземпляр класа геокодировщика
        gc = Geocoding(self.access_token)
        # Последовательное прямое геокодирование адресов
        for index, row in self.orders.iterrows():
            lat_lng = gc.get_coordinates(row['adress'])
            coordinates: tuple = (
                lat_lng[0],
                lat_lng[1]
            )
            coordinates_list.append(coordinates)

        return coordinates_list

    def get_map_route(self) -> list:
        """Возвращает лучший путь обхода точек, заданных гео-координатами.
        """
        # Получение списка геоточек (широта и долгота) каждого заказа
        geo_points = self.__get_map_coordinates()
        # Инициализация класса для задачи коммивояжера
        fitness_coordinates = mlrose.TravellingSales(coords=geo_points)
        # Формализация задачи
        problem_fit = mlrose.TSPOpt(
            length=len(geo_points),
            fitness_fn=fitness_coordinates,
            maximize=False
        )
        # Применение оптимизационного алгоритма с гипер-параметрами
        best_state, _ = mlrose.genetic_alg(
            problem_fit,
            pop_size=200,
            mutation_prob=0.2,
            max_attempts=100,
            max_iters=10,
            random_state=2
        )

        return best_state

    def get_orderby_map(self) -> pd.DataFrame:
        """Возвращает отражированный в опорядке оптимального
        обхода список географических точек для выполнения заказов.
        """
        self.orders['coordinates_list']  = self.__get_map_coordinates()
        # Получение списка обхода геоточек
        order_route = self.get_map_route()
        # Ранжирование заказов в порядке исполнения
        reindex_orders = self.orders.reindex(index=order_route)

        return reindex_orders


if __name__ == "__main__":

    first_order = pd.DataFrame(
        {
            'adress': [
                'Россия, Москва, Волоколамское шоссе, 3',
                'Россия, Москва, Рязанский проспект, 30',
                'Россия, Москва, Люсиновская улица, 20',
                'Россия, Москва, Ленинградское шоссе, 25',
                'Россия, Москва, Улица Свободы, 19'
            ]
        }
    )

    opt = Optimizer(auth.mapbox_token, first_order)

    result: pd.DataFrame = opt.get_orderby_map()

    print(result)
