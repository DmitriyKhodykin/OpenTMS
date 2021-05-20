from django.db import models


class Orders(models.Model):
    """Input from order-form data"""
    arrival_date = models.DateField('arrival_date')
    address = models.CharField('address', max_length=256)
    cargo = models.CharField('cargo', max_length=256)
    weight = models.IntegerField('weight')
    user = models.CharField('user', max_length=64)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Route(models.Model):
    """Results of the optimization module"""
    address = models.CharField('address', max_length=256)
    latitude = models.FloatField('latitude', default=0.0)
    longitude = models.FloatField('longitude', default=0.0)
    orderby_coordinates = models.IntegerField('orderby_coordinates', default=0)

    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'
