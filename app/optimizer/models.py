from django.db import models


class Route(models.Model):
    """Results from optimization module.
    """
    address = models.CharField('address', max_length=256)
    latitude = models.FloatField('latitude', default=0.0)
    longitude = models.FloatField('longitude', default=0.0)
    orderby_coordinates = models.IntegerField('orderby_coordinates', default=0)

    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'
