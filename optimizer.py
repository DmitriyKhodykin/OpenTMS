"""Оптимизационный модуль приложения.

Модуль строится на основе библиотеки `mlrose`, документацию по которой
можно найти по ссылке: https://mlrose.readthedocs.io/en/stable/

Библиотека предоставляет наиболее распространенные алгоритмы рандомизированной
оптимизации и поиска, применимые к ряду задач оптимизации как дискретными,
так и с непрерывными значениями.
"""

from geocoding import Geocoding
from pricedl import GetPrice
from auth import auth

import pandas as pd
import six
import sys
sys.modules['sklearn.externals.six'] = six
import mlrose


class Optimizer:
    """Решает оптимизационную транспортную задачу.
    """

    def __init__(self, token_map: str, token_price: str,
                 orders: pd.DataFrame):
        self.access_token = token_map
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

    def __get_price_triplets(self) -> list:
        """Возвращает список кортежей с тройками:
        1) Индекс географического объекта 1,
        2) Индекс географического объекта 2,
        3) Стоимость доставки между объектами.
        """
        pass

    def map_routing(self) -> list:
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

    def price_routing(self):
        """Возвращает лучший путь обхода гео-точек исходя из стоимости
        между каждой из таких пар.
        """
        pass

    def orderby_map(self) -> pd.DataFrame:
        """Возвращает отражированный в опорядке оптимального
        обхода список географических точек для выполнения заказов.
        """
        self.orders['coordinates_list'] = self.__get_map_coordinates()
        # Получение списка обхода геоточек
        order_route = self.map_routing()
        # Ранжирование заказов в порядке исполнения
        reindex_orders = self.orders.reindex(index=order_route)

        return reindex_orders

    def orderby_price(self) -> pd.DataFrame:
        """Возвращает список заказов, отражированный в порядке
        их оптимального обхода исходя из стоимости перевозки между точками.
        """
        pass


if __name__ == "__main__":

    first_order = pd.DataFrame(
        {
            'adress': [
                'Россия, Воронежская, Воронеж, Труда, 59',
                'Россия, Воронежская, Воронеж, Баррикадная, 39',
                'Россия, Воронежская, Воронеж, Космонавтов, 10',
                'Россия, Воронежская, Воронеж, Труда, 1',
                'Россия, Воронежская, Воронеж, Ленина, 43'
            ]
        }
    )

    opt = Optimizer(auth.mapbox_token, first_order)

    ordered_map: pd.DataFrame = opt.orderby_map()

    print(ordered_map)
