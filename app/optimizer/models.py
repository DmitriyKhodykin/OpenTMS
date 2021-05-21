import pandas as pd
from django.db import models
from django.forms.models import model_to_dict
from orders.models import Orders

from optimizer.opt.optimizer import Optimizer

# def _optimization_of_orders(self):
#     """Optimization of orders list using Optimizer
#     """
#     fetch_all_orders = model_to_dict(Orders.objects.all())
#     orders = pd.DataFrame(fetch_all_orders, columns=['arrival_date', 'address',
#                                                      'cargo', 'weight', 'user'])
#     opt = Optimizer(orders)
#     result = opt.orderby_map()
#     return result


class Route(models.Model):
    """Results from optimization module
    """
    address = models.CharField('address', max_length=256)
    latitude = models.FloatField('latitude', default=0.0)
    longitude = models.FloatField('longitude', default=0.0)
    orderby_coordinates = models.IntegerField('orderby_coordinates', default=0)

    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'

    @classmethod
    def create(cls, title):
        """Create """
        pass

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        """Save Orders optimisation results into the model
        """
        pass
