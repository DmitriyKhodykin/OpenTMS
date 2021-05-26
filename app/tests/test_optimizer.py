"""
Unit tests for optimizer module
"""

from unittest import TestCase

import pandas as pd

from optimizer.opt.optimizer import Optimizer


class OptimizerTestCase(TestCase):
    """Test cases for opt/Optimizer class"""

    def test_map_ordering(self):
        """Test case for ordering by map"""

        test_order = pd.DataFrame(
            {
                'address': [
                    'Воронеж Труда 59',
                    'Воронеж Баррикадная 39',
                    'Воронеж Космонавтов 10',
                    'Воронеж Труда 1',
                    'Воронеж Ленина 43'
                ]
            })

        reference: list = [2, 1, 4, 3, 0]

        opt = Optimizer(test_order)
        result = list(opt.orderby_map().index)
        self.assertEqual(reference, result)
