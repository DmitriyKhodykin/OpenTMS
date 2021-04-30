"""Оптимизационный модуль приложения.

Модуль строится на основе библиотеки `mlrose`, документацию по которой
можно найти по ссылке: https://mlrose.readthedocs.io/en/stable/

Библиотека предоставляет наиболее распространенные алгоритмы рандомизированной
оптимизации и поиска, применимые к ряду задач оптимизации как дискретными,
так и с непрерывными значениями.
"""

from auth import auth
from geocoding import geocoding
from price import GetPrice

import pandas as pd
import six
import sys
sys.modules['sklearn.externals.six'] = six
import mlrose


class Optimizer:
    """Решает оптимизационную транспортную задачу.
    """

    def __init__(self, orders: pd.DataFrame):
        self.orders = orders

    def __get_map_coordinates(self) -> list:
        """Возвращает список координат географических точек
        из заказов на перевозку.
        """
        # Определение координат точек
        coordinates_list: list = []
        # Экземпляр класа геокодировщика
        # Последовательное прямое геокодирование адресов
        for index, row in self.orders.iterrows():
            lat_lng = geocoding(row['address'])
            coordinates: tuple = (
                lat_lng[0],
                lat_lng[1]
            )
            coordinates_list.append(coordinates)

        return coordinates_list

    def __get_price_triplets(self, access_token) -> list:
        """Возвращает список кортежей с тройками:
        1) Индекс географического объекта 1,
        2) Индекс географического объекта 2,
        3) Стоимость доставки между объектами.
        """
        triplets: list = []
        # Инициализация класса определения цены
        price = GetPrice(access_token)
        # Перебор возможных пар географических объектов
        for index_from, address_from in self.orders.iterrows():
            for index_to, address_to in self.orders.iterrows():
                if address_to['adress'] != address_from['adress']:
                    ltl_price = price.get_ltl_price(
                        address_from['adress'], address_to['adress'], 1
                    )
                    triplet = (index_from, index_to, ltl_price)
                    triplets.append(triplet)

        return triplets

    def map_routing(self, access_token) -> list:
        """Возвращает лучший путь обхода точек, заданных гео-координатами.
        """
        # Получение списка геоточек (широта и долгота) каждого заказа
        geo_points = self.__get_map_coordinates(access_token)
        # Инициализация класса для задачи коммивояжера
        fitness_coordinates = mlrose.TravellingSales(coords=geo_points)
        # Формализация задачи
        problem_fit = mlrose.TSPOpt(
            length=len(self.orders),
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

    def price_routing(self, access_token) -> list:
        """Возвращает лучший путь обхода гео-точек исходя из стоимости
        между каждой из таких пар.
        """
        # Получение триплетов со стоимостью сборных перевозок
        triplets = self.__get_price_triplets(access_token)
        # Инициализация класса для задачи коммивояжера
        fitness_prices = mlrose.TravellingSales(distances=triplets)
        # Формализация задачи
        problem_fit = mlrose.TSPOpt(
            length=len(self.orders),
            fitness_fn=fitness_prices,
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

    def orderby_map(self, access_token) -> pd.DataFrame:
        """Возвращает отражированный в опорядке оптимального
        обхода список географических точек для выполнения заказов.
        """
        # Копируем фрейм с заказами
        orders = self.orders.copy()
        orders['coordinates_list'] = self.__get_map_coordinates(access_token)
        # Получение списка обхода геоточек
        order_route = self.map_routing(access_token)
        # Ранжирование заказов в порядке исполнения
        reindex_orders = orders.reindex(index=order_route)

        return reindex_orders

    def orderby_price(self, access_token) -> pd.DataFrame:
        """Возвращает список заказов, отражированный в порядке
        их оптимального обхода исходя из стоимости перевозки между точками.
        """
        # Копируем фрейм с заказами
        orders = self.orders.copy()
        # Получение списка обхода геоточек
        order_route = self.price_routing(access_token)
        # Ранжирование заказов в порядке исполнения
        reindex_orders = orders.reindex(index=order_route)

        return reindex_orders


if __name__ == "__main__":

    first_order = pd.DataFrame(
        {
            'address': [
                'Воронеж, Труда, 59',
                'Воронеж, Баррикадная, 39',
                'Воронеж, Космонавтов, 10',
                'Воронеж, Труда, 1',
                'Воронеж, Ленина, 43'
            ]
        }
    )

    opt = Optimizer(first_order)

    ordered_map: pd.DataFrame = opt.orderby_map(auth.mapbox_token)
    print('Отранжировано по географическим координатам')
    print(ordered_map)

    ordered_price: pd.DataFrame = opt.orderby_price(auth.dellin_token)
    print('Отранжировано по стоимости доставки')
    print(ordered_price)
