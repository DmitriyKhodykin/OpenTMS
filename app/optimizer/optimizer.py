"""Optimization module.

Module is based on `mlrose` library,
Docs: https://mlrose.readthedocs.io/en/stable/

The library provides the most common randomized optimization
and search algorithms applicable to a range of optimization problems,
both discrete and continuous.
"""

from optimizer.geocoding import get_coordinates
from optimizer.price import price

import pandas as pd
import six
import sys
sys.modules['sklearn.externals.six'] = six
import mlrose


class Optimizer:

    def __init__(self, orders: pd.DataFrame):
        self.orders = orders

    def __get_map_coordinates(self) -> list:
        """Returns a list of geographic locations from freight orders.
        """

        coordinates_list: list = []

        try:
            for index, row in self.orders.iterrows():
                lat_lng = get_coordinates(row['address'])
                coordinates: tuple = (
                    lat_lng[0],
                    lat_lng[1]
                )
                coordinates_list.append(coordinates)
        except TypeError:
            print('error: Empty geocoding result')

        return coordinates_list

    def __get_price_triplets(self) -> list:
        """Returns a list of triplets:
        1) Geographic point index 1,
        2) Geographic point index 2,
        3) Delivery cost between points.
        """
        triplets: list = []

        # All of possible pairs
        for index_from, address_from in self.orders.iterrows():
            for index_to, address_to in self.orders.iterrows():
                if address_to['address'] != address_from['address']:
                    ltl_price = price(address_from['address'], address_to['address'])
                    triplet = (index_from, index_to, ltl_price)
                    triplets.append(triplet)

        return triplets

    def map_routing(self) -> list:
        """Returns the best path to traverse points given by geo-coordinates.
        """
        # Lat and Lon of each order
        geo_points = self.__get_map_coordinates()
        # Sales travelling instance
        fitness_coordinates = mlrose.TravellingSales(coords=geo_points)
        # Fit problem
        problem_fit = mlrose.TSPOpt(
            length=len(self.orders),
            fitness_fn=fitness_coordinates,
            maximize=False
        )
        # Best state result
        best_state, _ = mlrose.genetic_alg(
            problem_fit,
            pop_size=200,
            mutation_prob=0.2,
            max_attempts=100,
            max_iters=10,
            random_state=2
        )

        return best_state

    def price_routing(self) -> list:
        """Returns the best path to traverse geopoints based on
        the cost between each of these pairs.
        """
        triplets = self.__get_price_triplets()
        # Sales travelling instance
        fitness_prices = mlrose.TravellingSales(distances=triplets)
        # Fit problem
        problem_fit = mlrose.TSPOpt(
            length=len(self.orders),
            fitness_fn=fitness_prices,
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

    def orderby_map(self) -> pd.DataFrame:
        """Returns a list of geographic points for order fulfillment,
        ordered in the optimal traversal order.
        """
        orders = self.orders.copy()
        orders['coordinates_list'] = self.__get_map_coordinates()
        order_route = self.map_routing()
        reindex_orders = orders.reindex(index=order_route)

        return reindex_orders

    def orderby_price(self) -> pd.DataFrame:
        """Returns a list of orders ordered on the
        cost of transportation between points.
        """
        orders = self.orders.copy()
        order_route = self.price_routing()
        reindex_orders = orders.reindex(index=order_route)

        return reindex_orders


if __name__ == "__main__":

    test_order = pd.DataFrame(
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

    opt = Optimizer(test_order)

    ordered_map: pd.DataFrame = opt.orderby_map()
    print('Отранжировано по географическим координатам')
    print(ordered_map)
